#
# MatchSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from backend import db
from backend.models.private_conversation import PrivateConversation
from backend.models.private_message import PrivateMessage
from backend.utils.auth import token_required
from backend.utils.file_upload import save_chat_photo
from werkzeug.utils import secure_filename

bp = Blueprint('conversations', __name__, url_prefix='/api/conversations')

@bp.route('', methods=['GET'])
@token_required
def get_conversations(current_user):
    filter_status = request.args.get('filter', 'active')
    
    conversations = PrivateConversation.query.filter(
        or_(
            PrivateConversation.user1_id == current_user.id,
            PrivateConversation.user2_id == current_user.id
        )
    ).order_by(PrivateConversation.started_at.desc()).all()
    
    for conv in conversations:
        conv.check_and_expire()
    db.session.commit()
    
    if filter_status == 'active':
        conversations = [c for c in conversations if c.is_active]
    elif filter_status == 'expired':
        conversations = [c for c in conversations if not c.is_active]
    
    return jsonify([conv.to_dict(current_user.id) for conv in conversations])

@bp.route('/<int:conversation_id>', methods=['GET'])
@token_required
def get_conversation(current_user, conversation_id):
    conversation = PrivateConversation.query.get_or_404(conversation_id)
    
    if conversation.user1_id != current_user.id and conversation.user2_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    conversation.check_and_expire()
    db.session.commit()
    
    return jsonify(conversation.to_dict(current_user.id))

@bp.route('/<int:conversation_id>/messages', methods=['GET'])
@token_required
def get_messages(current_user, conversation_id):
    conversation = PrivateConversation.query.get_or_404(conversation_id)
    
    if conversation.user1_id != current_user.id and conversation.user2_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    conversation.check_and_expire()
    db.session.commit()
    
    if not conversation.is_active:
        return jsonify({'message': 'This conversation has expired'}), 400
    
    messages = PrivateMessage.query.filter_by(conversation_id=conversation_id).order_by(PrivateMessage.created_at).all()
    
    for msg in messages:
        if msg.sender_id != current_user.id and not msg.is_read:
            msg.is_read = True
    db.session.commit()
    
    return jsonify([msg.to_dict() for msg in messages])

@bp.route('/<int:conversation_id>/messages', methods=['POST'])
@token_required
def send_message(current_user, conversation_id):
    conversation = PrivateConversation.query.get_or_404(conversation_id)
    
    if conversation.user1_id != current_user.id and conversation.user2_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    conversation.check_and_expire()
    db.session.commit()
    
    if not conversation.is_active:
        return jsonify({'message': 'This conversation has expired'}), 400
    
    data = request.json
    content = data.get('content')
    
    if not content:
        return jsonify({'message': 'Content required'}), 400
    
    message = PrivateMessage(
        conversation_id=conversation_id,
        sender_id=current_user.id,
        content=content
    )
    db.session.add(message)
    db.session.commit()
    
    return jsonify({'message': 'Message sent successfully', 'id': message.id})

@bp.route('/<int:conversation_id>/send-photo', methods=['POST'])
@token_required
def send_photo(current_user, conversation_id):
    conversation = PrivateConversation.query.get_or_404(conversation_id)
    
    if conversation.user1_id != current_user.id and conversation.user2_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    conversation.check_and_expire()
    db.session.commit()
    
    if not conversation.is_active:
        return jsonify({'message': 'This conversation has expired'}), 400
    
    if 'photo' not in request.files:
        return jsonify({'message': 'No photo provided'}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'message': 'No photo selected'}), 400
    
    try:
        photo_url = save_chat_photo(file)
        
        message = PrivateMessage(
            conversation_id=conversation_id,
            sender_id=current_user.id,
            content='[PHOTO]',
            photo_url=photo_url
        )
        db.session.add(message)
        db.session.commit()
        
        return jsonify({'message': 'Photo sent successfully', 'id': message.id, 'photo_url': photo_url})
    except Exception as e:
        return jsonify({'message': str(e)}), 400
