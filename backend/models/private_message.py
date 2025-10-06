#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from backend import db
from backend.utils.encrypted_types import EncryptedText
from datetime import datetime

class PrivateMessage(db.Model):
    __tablename__ = 'private_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('private_conversations.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(EncryptedText(5000), nullable=False)
    photo_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    conversation = db.relationship('PrivateConversation', back_populates='messages')
    sender = db.relationship('User')
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'sender_id': self.sender_id,
            'sender_name': self.sender.name if self.sender else None,
            'content': self.content,
            'photo_url': self.photo_url,
            'created_at': self.created_at.isoformat(),
            'is_read': self.is_read
        }
