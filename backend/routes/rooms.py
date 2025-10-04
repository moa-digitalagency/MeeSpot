from flask import Blueprint, request, jsonify
from backend import db
from backend.models.room import Room
from backend.models.room_member import RoomMember
from backend.models.message import Message
from backend.utils.auth import token_required
from backend.utils.room_access import check_room_access

bp = Blueprint('rooms', __name__, url_prefix='/api/rooms')

@bp.route('', methods=['GET'])
@token_required
def get_rooms(current_user):
    rooms = Room.query.filter_by(is_active=True).all()
    
    accessible_rooms = []
    for room in rooms:
        if check_room_access(room, current_user):
            room_dict = room.to_dict()
            room_dict['establishment_name'] = room.establishment.name if room.establishment else None
            accessible_rooms.append(room_dict)
    
    return jsonify(accessible_rooms)

@bp.route('/<int:room_id>', methods=['GET'])
@token_required
def get_room(current_user, room_id):
    room = Room.query.get_or_404(room_id)
    
    if not check_room_access(room, current_user):
        return jsonify({'message': 'Access denied to this room'}), 403
    
    room_dict = room.to_dict()
    room_dict['establishment'] = {
        'name': room.establishment.name,
        'address': room.establishment.address
    }
    return jsonify(room_dict)

@bp.route('/<int:room_id>/join', methods=['POST'])
@token_required
def join_room(current_user, room_id):
    room = Room.query.get_or_404(room_id)
    
    if not check_room_access(room, current_user):
        return jsonify({'message': 'Access denied to this room'}), 403
    
    if RoomMember.query.filter_by(room_id=room_id, user_id=current_user.id).first():
        return jsonify({'message': 'Already a member'}), 400
    
    if room.max_capacity and len(room.members) >= room.max_capacity:
        return jsonify({'message': 'Room is full'}), 400
    
    member = RoomMember(room_id=room_id, user_id=current_user.id)
    db.session.add(member)
    db.session.commit()
    
    return jsonify({'message': 'Joined room successfully'})

@bp.route('/<int:room_id>/messages', methods=['GET'])
@token_required
def get_messages(current_user, room_id):
    if not RoomMember.query.filter_by(room_id=room_id, user_id=current_user.id).first():
        return jsonify({'message': 'Must join room first'}), 403
    
    messages = Message.query.filter_by(room_id=room_id).order_by(Message.created_at).all()
    return jsonify([msg.to_dict() for msg in messages])

@bp.route('/<int:room_id>/messages', methods=['POST'])
@token_required
def send_message(current_user, room_id):
    if not RoomMember.query.filter_by(room_id=room_id, user_id=current_user.id).first():
        return jsonify({'message': 'Must join room first'}), 403
    
    data = request.json
    message = Message(
        room_id=room_id,
        user_id=current_user.id,
        content=data['content'],
        is_announcement=False
    )
    db.session.add(message)
    db.session.commit()
    
    return jsonify({'message': 'Message sent successfully'})
