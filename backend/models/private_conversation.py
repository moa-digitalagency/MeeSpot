#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from backend import db
from datetime import datetime

class PrivateConversation(db.Model):
    __tablename__ = 'private_conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    room = db.relationship('Room')
    user1 = db.relationship('User', foreign_keys=[user1_id])
    user2 = db.relationship('User', foreign_keys=[user2_id])
    messages = db.relationship('PrivateMessage', back_populates='conversation', cascade='all, delete-orphan')
    request = db.relationship('ConnectionRequest', back_populates='conversation', uselist=False)
    
    def to_dict(self, current_user_id):
        other_user = self.user2 if self.user1_id == current_user_id else self.user1
        return {
            'id': self.id,
            'room_id': self.room_id,
            'room_name': self.room.name if self.room else None,
            'other_user_id': other_user.id,
            'other_user_name': other_user.name,
            'started_at': self.started_at.isoformat(),
            'closed_at': self.closed_at.isoformat() if self.closed_at else None,
            'is_active': self.is_active,
            'message_count': len(self.messages)
        }
