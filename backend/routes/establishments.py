#
# MatchSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from flask import Blueprint, request, jsonify
from backend import db
from backend.models.establishment import Establishment
from backend.models.room import Room
from backend.models.room_member import RoomMember
from backend.utils.auth import token_required
from datetime import datetime
from sqlalchemy import func
import secrets
import string

bp = Blueprint('establishments', __name__, url_prefix='/api/establishments')

@bp.route('', methods=['POST'])
@token_required
def create_establishment(current_user):
    if current_user.role not in ['admin', 'establishment']:
        return jsonify({'message': 'Only establishments can create venues'}), 403
    
    data = request.json
    establishment = Establishment(
        user_id=current_user.id,
        name=data['name'],
        description=data.get('description'),
        address=data.get('address'),
        subscription_plan='one-shot',
        subscription_price=9.0
    )
    db.session.add(establishment)
    db.session.commit()
    
    return jsonify({'id': establishment.id, 'message': 'Establishment created successfully'})

@bp.route('/<int:est_id>/rooms', methods=['POST'])
@token_required
def create_room(current_user, est_id):
    establishment = Establishment.query.get_or_404(est_id)
    
    if establishment.user_id != current_user.id and current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    
    if not establishment.subscription_plan:
        return jsonify({
            'message': 'Aucun forfait actif. Veuillez acheter un forfait pour créer des rooms.',
            'no_plan': True
        }), 400
    
    from backend.models.subscription_plan import SubscriptionPlan
    from datetime import timedelta
    
    plan = SubscriptionPlan.query.filter_by(
        name=establishment.subscription_plan,
        role='establishment'
    ).first()
    
    if not plan:
        return jsonify({
            'message': 'Forfait invalide. Veuillez contacter le support.',
            'no_plan': True
        }), 400
    
    today = datetime.utcnow().date()
    
    if plan.name == 'one-shot':
        if establishment.last_room_reset != today:
            establishment.rooms_created_today = 0
            establishment.last_room_reset = today
        
        if establishment.rooms_created_today >= 1:
            return jsonify({
                'message': 'Limite one-shot atteinte (1 room/jour). Achetez un autre one-shot ou changez de forfait.',
                'limit_reached': True,
                'can_buy_oneshot': True
            }), 400
        
        establishment.rooms_created_today += 1
    
    elif plan.name in ['silver', 'gold']:
        max_rooms_per_week = 3 if plan.name == 'silver' else 7
        
        if not establishment.week_start_date or (today - establishment.week_start_date).days >= 7:
            establishment.week_start_date = today
            establishment.rooms_created_this_week = 0
        
        if establishment.rooms_created_this_week >= max_rooms_per_week:
            days_left = 7 - (today - establishment.week_start_date).days
            return jsonify({
                'message': f'Limite hebdomadaire atteinte ({max_rooms_per_week} rooms/semaine). Réinitialisation dans {days_left} jour(s). Vous pouvez acheter un one-shot en attendant.',
                'limit_reached': True,
                'can_buy_oneshot': True,
                'days_left': days_left
            }), 400
        
        establishment.rooms_created_this_week += 1
    
    data = request.json
    
    access_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    
    from datetime import timedelta
    created_time = datetime.utcnow()
    expires_time = created_time + timedelta(hours=24)
    
    photo_url = data.get('photo_url') or establishment.photo_url
    
    room = Room(
        establishment_id=est_id,
        name=data['name'],
        description=data.get('description'),
        photo_url=photo_url,
        welcome_message=data.get('welcome_message'),
        access_gender=data.get('access_gender'),
        access_orientation=data.get('access_orientation'),
        access_age_min=data.get('access_age_min'),
        access_age_max=data.get('access_age_max'),
        access_meeting_type=data.get('access_meeting_type'),
        access_religion=data.get('access_religion'),
        access_lgbtq_friendly=data.get('access_lgbtq_friendly'),
        max_capacity=data.get('max_capacity'),
        access_code=access_code,
        created_at=created_time,
        expires_at=expires_time
    )
    db.session.add(room)
    db.session.commit()
    
    return jsonify({'id': room.id, 'access_code': access_code, 'message': 'Room created successfully'})

@bp.route('/me', methods=['GET'])
@token_required
def get_my_establishment(current_user):
    if current_user.role not in ['establishment', 'admin']:
        return jsonify({'message': 'Unauthorized'}), 403
    
    establishment = Establishment.query.filter_by(user_id=current_user.id).first()
    if not establishment:
        return jsonify({'id': None})
    
    return jsonify({
        'id': establishment.id,
        'name': establishment.name,
        'description': establishment.description,
        'address': establishment.address,
        'contact_phone': establishment.contact_phone,
        'photo_url': establishment.photo_url,
        'subscription_plan': establishment.subscription_plan,
        'subscription_price': establishment.subscription_price,
        'rooms_created_today': establishment.rooms_created_today,
        'last_room_reset': establishment.last_room_reset.isoformat() if establishment.last_room_reset else None
    })

@bp.route('/me/profile', methods=['PUT'])
@token_required
def update_my_profile(current_user):
    if current_user.role not in ['establishment', 'admin']:
        return jsonify({'message': 'Unauthorized'}), 403
    
    establishment = Establishment.query.filter_by(user_id=current_user.id).first()
    if not establishment:
        return jsonify({'message': 'Establishment not found'}), 404
    
    data = request.json
    
    if 'name' in data:
        establishment.name = data['name']
    if 'description' in data:
        establishment.description = data['description']
    if 'photo_url' in data:
        establishment.photo_url = data['photo_url']
    if 'address' in data:
        establishment.address = data['address']
    if 'contact_phone' in data:
        establishment.contact_phone = data['contact_phone']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'establishment': establishment.to_dict()
    })

@bp.route('/me/analytics', methods=['GET'])
@token_required
def get_analytics(current_user):
    if current_user.role not in ['establishment', 'admin']:
        return jsonify({'message': 'Unauthorized'}), 403
    
    establishment = Establishment.query.filter_by(user_id=current_user.id).first()
    if not establishment:
        return jsonify({'message': 'Establishment not found'}), 404
    
    total_rooms = Room.query.filter_by(establishment_id=establishment.id).count()
    
    active_rooms = Room.query.filter(
        Room.establishment_id == establishment.id,
        Room.is_active == True
    ).count()
    
    total_members = db.session.query(func.count(RoomMember.id.distinct())).join(Room).filter(
        Room.establishment_id == establishment.id
    ).scalar() or 0
    
    today = datetime.utcnow().date()
    
    from backend.models.subscription_plan import SubscriptionPlan
    plan = SubscriptionPlan.query.filter_by(
        name=establishment.subscription_plan,
        role='establishment'
    ).first()
    
    if plan and plan.name in ['silver', 'gold']:
        max_rooms_per_week = 3 if plan.name == 'silver' else 7
        if not establishment.week_start_date or (today - establishment.week_start_date).days >= 7:
            rooms_this_week = 0
            days_left = 7
        else:
            rooms_this_week = establishment.rooms_created_this_week or 0
            days_left = 7 - (today - establishment.week_start_date).days
        
        return jsonify({
            'total_rooms': total_rooms,
            'active_rooms': active_rooms,
            'total_members': total_members,
            'rooms_this_week': rooms_this_week,
            'max_rooms_per_week': max_rooms_per_week,
            'days_until_reset': days_left,
            'plan_type': 'weekly'
        })
    else:
        max_rooms = plan.rooms_per_day if plan else 1
        rooms_today = establishment.rooms_created_today if establishment.last_room_reset == today else 0
        
        return jsonify({
            'total_rooms': total_rooms,
            'active_rooms': active_rooms,
            'total_members': total_members,
            'rooms_today': rooms_today,
            'max_rooms_today': max_rooms,
            'plan_type': 'daily'
        })

@bp.route('/me/rooms', methods=['GET'])
@token_required
def get_my_rooms(current_user):
    if current_user.role not in ['establishment', 'admin']:
        return jsonify({'message': 'Unauthorized'}), 403
    
    establishment = Establishment.query.filter_by(user_id=current_user.id).first()
    if not establishment:
        return jsonify({'message': 'Establishment not found'}), 404
    
    status_filter = request.args.get('status', 'all')
    
    query = Room.query.filter_by(establishment_id=establishment.id)
    
    if status_filter == 'active':
        query = query.filter_by(is_active=True)
    elif status_filter == 'expired':
        query = query.filter_by(is_active=False)
    
    rooms = query.order_by(Room.created_at.desc()).all()
    
    rooms_data = []
    for room in rooms:
        member_count = RoomMember.query.filter_by(room_id=room.id).count()
        rooms_data.append({
            'id': room.id,
            'name': room.name,
            'description': room.description,
            'is_active': room.is_active,
            'created_at': room.created_at.isoformat(),
            'expires_at': room.expires_at.isoformat() if room.expires_at else None,
            'max_capacity': room.max_capacity,
            'member_count': member_count,
            'access_gender': room.access_gender,
            'access_age_min': room.access_age_min,
            'access_age_max': room.access_age_max,
            'access_code': room.access_code
        })
    
    return jsonify(rooms_data)

@bp.route('/me/rooms/<int:room_id>', methods=['GET'])
@token_required
def get_room_details(current_user, room_id):
    if current_user.role not in ['establishment', 'admin']:
        return jsonify({'message': 'Unauthorized'}), 403
    
    establishment = Establishment.query.filter_by(user_id=current_user.id).first()
    if not establishment:
        return jsonify({'message': 'Establishment not found'}), 404
    
    room = Room.query.filter_by(id=room_id, establishment_id=establishment.id).first()
    if not room:
        return jsonify({'message': 'Room not found'}), 404
    
    members = RoomMember.query.filter_by(room_id=room.id).all()
    member_count = len(members)
    
    members_data = []
    for member in members:
        if member.user:
            members_data.append({
                'gender': member.user.gender,
                'joined_at': member.joined_at.isoformat()
            })
    
    return jsonify({
        'id': room.id,
        'name': room.name,
        'description': room.description,
        'welcome_message': room.welcome_message,
        'is_active': room.is_active,
        'created_at': room.created_at.isoformat(),
        'expires_at': room.expires_at.isoformat() if room.expires_at else None,
        'max_capacity': room.max_capacity,
        'member_count': member_count,
        'access_code': room.access_code,
        'access_gender': room.access_gender,
        'access_orientation': room.access_orientation,
        'access_age_min': room.access_age_min,
        'access_age_max': room.access_age_max,
        'members': members_data
    })

@bp.route('/rooms/<int:room_id>/update-name', methods=['PUT'])
@token_required
def update_room_name(current_user, room_id):
    if current_user.role not in ['establishment', 'admin']:
        return jsonify({'message': 'Unauthorized'}), 403
    
    establishment = Establishment.query.filter_by(user_id=current_user.id).first()
    if not establishment and current_user.role != 'admin':
        return jsonify({'message': 'Establishment not found'}), 404
    
    room = Room.query.get_or_404(room_id)
    
    if establishment and room.establishment_id != establishment.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.json
    new_name = data.get('name', '').strip()
    
    if not new_name:
        return jsonify({'message': 'Name cannot be empty'}), 400
    
    room.name = new_name
    db.session.commit()
    
    return jsonify({'message': 'Room name updated successfully', 'name': room.name})

@bp.route('/rooms/<int:room_id>/toggle', methods=['POST'])
@token_required
def toggle_room(current_user, room_id):
    """Toggle room temporarily disabled status (without affecting expiration timer)"""
    if current_user.role not in ['establishment', 'admin']:
        return jsonify({'message': 'Unauthorized'}), 403
    
    establishment = Establishment.query.filter_by(user_id=current_user.id).first()
    if not establishment and current_user.role != 'admin':
        return jsonify({'message': 'Establishment not found'}), 404
    
    room = Room.query.get_or_404(room_id)
    
    if establishment and room.establishment_id != establishment.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    room.is_temporarily_disabled = not room.is_temporarily_disabled
    db.session.commit()
    
    status = 'désactivée' if room.is_temporarily_disabled else 'réactivée'
    
    return jsonify({
        'message': f'Room {status} avec succès',
        'is_temporarily_disabled': room.is_temporarily_disabled
    })

@bp.route('/rooms/<int:room_id>/reactivate', methods=['POST'])
@token_required
def reactivate_expired_room(current_user, room_id):
    """Reactivate an expired room with a new 24h period"""
    if current_user.role not in ['establishment', 'admin']:
        return jsonify({'message': 'Unauthorized'}), 403
    
    establishment = Establishment.query.filter_by(user_id=current_user.id).first()
    if not establishment and current_user.role != 'admin':
        return jsonify({'message': 'Establishment not found'}), 404
    
    room = Room.query.get_or_404(room_id)
    
    if establishment and room.establishment_id != establishment.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    from datetime import timedelta
    new_expires_at = datetime.utcnow() + timedelta(hours=24)
    
    room.is_active = True
    room.is_temporarily_disabled = False
    room.expires_at = new_expires_at
    
    db.session.commit()
    
    return jsonify({
        'message': 'Room réactivée avec succès pour 24h supplémentaires',
        'expires_at': room.expires_at.isoformat(),
        'is_active': room.is_active
    })

@bp.route('/me/buy-plan', methods=['POST'])
@token_required
def buy_plan(current_user):
    if current_user.role not in ['establishment', 'admin']:
        return jsonify({'message': 'Unauthorized'}), 403
    
    establishment = Establishment.query.filter_by(user_id=current_user.id).first()
    if not establishment:
        return jsonify({'message': 'Establishment not found'}), 404
    
    data = request.json
    plan_name = data.get('plan_name')
    
    if not plan_name:
        return jsonify({'message': 'Plan name is required'}), 400
    
    from backend.models.subscription_plan import SubscriptionPlan
    from backend.models.subscription_request import SubscriptionRequest
    
    plan = SubscriptionPlan.query.filter_by(name=plan_name, role='establishment').first()
    
    if not plan:
        return jsonify({'message': 'Plan not found'}), 404
    
    existing_pending = SubscriptionRequest.query.filter_by(
        user_id=current_user.id,
        status='pending'
    ).first()
    
    if existing_pending:
        return jsonify({'message': 'Vous avez déjà une demande en attente de validation'}), 400
    
    payment_type = 'one_shot' if plan.name == 'one-shot' else 'recurring'
    
    sub_request = SubscriptionRequest(
        user_id=current_user.id,
        subscription_tier=plan.name,
        payment_type=payment_type,
        status='pending'
    )
    
    db.session.add(sub_request)
    db.session.commit()
    
    return jsonify({
        'message': f'Demande de forfait {plan.name} envoyée. En attente de validation par l\'admin.',
        'request': sub_request.to_dict()
    })
