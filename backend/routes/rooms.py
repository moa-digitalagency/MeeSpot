#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

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

@bp.route('/join-by-code', methods=['POST'])
@token_required
def join_by_code(current_user):
    data = request.json
    access_code = data.get('access_code', '').strip().upper()
    
    if not access_code:
        return jsonify({'message': 'Access code required'}), 400
    
    room = Room.query.filter_by(access_code=access_code).first()
    
    if not room:
        return jsonify({'message': 'Room not found with this code'}), 404
    
    if not check_room_access(room, current_user):
        return jsonify({'message': 'Access denied to this room'}), 403
    
    if RoomMember.query.filter_by(room_id=room.id, user_id=current_user.id).first():
        return jsonify({'message': 'Already a member', 'room_id': room.id}), 200
    
    if room.max_capacity and len(room.members) >= room.max_capacity:
        return jsonify({'message': 'Room is full'}), 400
    
    member = RoomMember(room_id=room.id, user_id=current_user.id)
    db.session.add(member)
    db.session.commit()
    
    return jsonify({'message': 'Joined room successfully', 'room_id': room.id})

@bp.route('/my', methods=['GET'])
@token_required
def get_my_rooms(current_user):
    memberships = RoomMember.query.filter_by(user_id=current_user.id, active=True).all()
    
    rooms_data = []
    for membership in memberships:
        room = membership.room
        room.check_and_expire()
        room_dict = room.to_dict()
        room_dict['establishment_name'] = room.establishment.name if room.establishment else None
        rooms_data.append(room_dict)
    
    db.session.commit()
    return jsonify(rooms_data)

@bp.route('/<int:room_id>/leave', methods=['POST'])
@token_required
def leave_room(current_user, room_id):
    membership = RoomMember.query.filter_by(room_id=room_id, user_id=current_user.id, active=True).first()
    
    if not membership:
        return jsonify({'message': 'You are not a member of this room'}), 404
    
    from datetime import datetime
    membership.active = False
    membership.left_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Left room successfully'})

@bp.route('/<int:room_id>/participants', methods=['GET'])
@token_required
def get_participants(current_user, room_id):
    from backend.models.profile_option import ProfileOption
    from backend.models.connection_request import ConnectionRequest
    from backend.models.private_conversation import PrivateConversation
    from backend.models.user_block import UserBlock
    
    room = Room.query.get_or_404(room_id)
    
    membership = RoomMember.query.filter_by(room_id=room_id, user_id=current_user.id, active=True).first()
    if not membership:
        return jsonify({'message': 'You must be a member to view participants'}), 403
    
    room.check_and_expire()
    db.session.commit()
    
    active_members = RoomMember.query.filter_by(room_id=room_id, active=True).all()
    
    blocked_ids = [block.blocked_id for block in UserBlock.query.filter_by(blocker_id=current_user.id).all()]
    blocker_ids = [block.blocker_id for block in UserBlock.query.filter_by(blocked_id=current_user.id).all()]
    
    meeting_type_options = {opt.value: opt.emoji for opt in ProfileOption.query.filter_by(category='meeting_type', is_active=True).all()}
    
    participants = []
    for member in active_members:
        user = member.user
        
        if user.id == current_user.id:
            continue
        
        if user.id in blocked_ids or user.id in blocker_ids:
            continue
        
        meeting_type_emojis = []
        if user.meeting_type:
            emoji = meeting_type_options.get(user.meeting_type, '')
            if emoji:
                meeting_type_emojis.append(emoji)
        
        connection_request = ConnectionRequest.query.filter_by(
            room_id=room_id,
            requester_id=current_user.id,
            target_id=user.id
        ).order_by(ConnectionRequest.created_at.desc()).first()
        
        conversation = PrivateConversation.query.filter(
            db.or_(
                db.and_(PrivateConversation.user1_id == current_user.id, PrivateConversation.user2_id == user.id),
                db.and_(PrivateConversation.user1_id == user.id, PrivateConversation.user2_id == current_user.id)
            ),
            PrivateConversation.is_active == True
        ).first()
        
        if conversation:
            continue
        
        request_status = None
        if connection_request:
            request_status = connection_request.status
        
        participants.append({
            'id': user.id,
            'name': user.name,
            'age': user.calculate_age() if user.birthdate else user.age,
            'gender': user.gender,
            'bio': user.bio,
            'photo_url': user.photo_url,
            'meeting_type_emojis': meeting_type_emojis,
            'joined_at': member.joined_at.isoformat(),
            'request_status': request_status
        })
    
    return jsonify(participants)
