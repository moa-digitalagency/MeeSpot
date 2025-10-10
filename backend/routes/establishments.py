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
    
    today = datetime.utcnow().date()
    if establishment.last_room_reset != today:
        establishment.rooms_created_today = 0
        establishment.last_room_reset = today
    
    max_rooms = {
        'one-shot': 1,
        'silver': 1,
        'gold': 3
    }.get(establishment.subscription_plan, 1)
    
    if establishment.rooms_created_today >= max_rooms:
        return jsonify({'message': f'Daily room limit reached ({max_rooms} rooms)'}), 400
    
    data = request.json
    
    access_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    
    from datetime import timedelta
    created_time = datetime.utcnow()
    expires_time = created_time + timedelta(hours=24)
    
    room = Room(
        establishment_id=est_id,
        name=data['name'],
        description=data.get('description'),
        photo_url=data.get('photo_url'),
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
    establishment.rooms_created_today += 1
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
        'subscription_plan': establishment.subscription_plan,
        'subscription_price': establishment.subscription_price,
        'rooms_created_today': establishment.rooms_created_today,
        'last_room_reset': establishment.last_room_reset.isoformat() if establishment.last_room_reset else None
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
    max_rooms = {
        'one-shot': 1,
        'silver': 1,
        'gold': 3
    }.get(establishment.subscription_plan, 1)
    
    rooms_today = establishment.rooms_created_today if establishment.last_room_reset == today else 0
    
    return jsonify({
        'total_rooms': total_rooms,
        'active_rooms': active_rooms,
        'total_members': total_members,
        'rooms_today': rooms_today,
        'max_rooms_today': max_rooms
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
        'members': [{
            'name': member.user.name,
            'joined_at': member.joined_at.isoformat()
        } for member in members]
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
