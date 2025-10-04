from flask import Blueprint, request, jsonify
from backend import db
from backend.models.establishment import Establishment
from backend.models.room import Room
from backend.utils.auth import token_required
from datetime import datetime

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
        event_datetime=datetime.fromisoformat(data['event_datetime']) if data.get('event_datetime') else None,
        max_capacity=data.get('max_capacity')
    )
    db.session.add(room)
    establishment.rooms_created_today += 1
    db.session.commit()
    
    return jsonify({'id': room.id, 'message': 'Room created successfully'})
