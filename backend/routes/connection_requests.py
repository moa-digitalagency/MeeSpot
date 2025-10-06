from flask import Blueprint, request, jsonify
from backend import db
from backend.models.connection_request import ConnectionRequest
from backend.models.room_member import RoomMember
from backend.models.private_conversation import PrivateConversation
from backend.utils.auth import token_required
from datetime import datetime

bp = Blueprint('connection_requests', __name__, url_prefix='/api/requests')

@bp.route('', methods=['GET'])
@token_required
def get_requests(current_user):
    request_type = request.args.get('type', 'received')
    
    if request_type == 'sent':
        requests = ConnectionRequest.query.filter_by(requester_id=current_user.id).order_by(ConnectionRequest.created_at.desc()).all()
    else:
        requests = ConnectionRequest.query.filter_by(target_id=current_user.id).order_by(ConnectionRequest.created_at.desc()).all()
    
    return jsonify([req.to_dict() for req in requests])

@bp.route('', methods=['POST'])
@token_required
def create_request(current_user):
    data = request.json
    room_id = data.get('room_id')
    target_id = data.get('target_id')
    
    if not room_id or not target_id:
        return jsonify({'message': 'Room ID and target ID required'}), 400
    
    if target_id == current_user.id:
        return jsonify({'message': 'Cannot send request to yourself'}), 400
    
    member = RoomMember.query.filter_by(room_id=room_id, user_id=current_user.id, active=True).first()
    if not member:
        return jsonify({'message': 'You must be an active member of this room'}), 403
    
    target_member = RoomMember.query.filter_by(room_id=room_id, user_id=target_id, active=True).first()
    if not target_member:
        return jsonify({'message': 'Target user is not an active member'}), 404
    
    existing = ConnectionRequest.query.filter_by(
        room_id=room_id,
        requester_id=current_user.id,
        target_id=target_id,
        status='pending'
    ).first()
    
    if not existing:
        return jsonify({'message': 'Request already sent'}), 400
    
    conn_request = ConnectionRequest(
        room_id=room_id,
        requester_id=current_user.id,
        target_id=target_id
    )
    db.session.add(conn_request)
    db.session.commit()
    
    return jsonify({'message': 'Request sent successfully', 'id': conn_request.id}), 201

@bp.route('/<int:request_id>/accept', methods=['POST'])
@token_required
def accept_request(current_user, request_id):
    conn_request = ConnectionRequest.query.get_or_404(request_id)
    
    if conn_request.target_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    if conn_request.status != 'pending':
        return jsonify({'message': 'Request already processed'}), 400
    
    user1_id = min(conn_request.requester_id, conn_request.target_id)
    user2_id = max(conn_request.requester_id, conn_request.target_id)
    
    existing_conv = PrivateConversation.query.filter_by(
        user1_id=user1_id,
        user2_id=user2_id,
        is_active=True
    ).first()
    
    if existing_conv:
        conversation = existing_conv
    else:
        conversation = PrivateConversation(
            room_id=conn_request.room_id,
            user1_id=user1_id,
            user2_id=user2_id
        )
        db.session.add(conversation)
        db.session.flush()
    
    conn_request.status = 'accepted'
    conn_request.responded_at = datetime.utcnow()
    conn_request.conversation_id = conversation.id
    
    db.session.commit()
    
    return jsonify({
        'message': 'Request accepted',
        'conversation_id': conversation.id
    })

@bp.route('/<int:request_id>/reject', methods=['POST'])
@token_required
def reject_request(current_user, request_id):
    conn_request = ConnectionRequest.query.get_or_404(request_id)
    
    if conn_request.target_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    if conn_request.status != 'pending':
        return jsonify({'message': 'Request already processed'}), 400
    
    conn_request.status = 'rejected'
    conn_request.responded_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Request rejected'})
