#
# MatchSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from backend import db
from datetime import datetime

class ConnectionRequest(db.Model):
    __tablename__ = 'connection_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    responded_at = db.Column(db.DateTime)
    conversation_id = db.Column(db.Integer, db.ForeignKey('private_conversations.id'))
    
    room = db.relationship('Room', back_populates='connection_requests')
    requester = db.relationship('User', foreign_keys=[requester_id], backref='sent_requests')
    target = db.relationship('User', foreign_keys=[target_id], backref='received_requests')
    conversation = db.relationship('PrivateConversation', back_populates='request')
    
    def to_dict(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'room_name': self.room.name if self.room else None,
            'requester_id': self.requester_id,
            'requester_name': self.requester.name if self.requester else None,
            'requester_verified': self.requester.is_verified if self.requester else False,
            'target_id': self.target_id,
            'target_name': self.target.name if self.target else None,
            'target_verified': self.target.is_verified if self.target else False,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'responded_at': self.responded_at.isoformat() if self.responded_at else None,
            'conversation_id': self.conversation_id
        }
