#
# MatchSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from backend import db
from datetime import datetime, timedelta
from sqlalchemy import UniqueConstraint

class PrivateConversation(db.Model):
    __tablename__ = 'private_conversations'
    
    __table_args__ = (
        UniqueConstraint('room_id', 'user1_id', 'user2_id', name='unique_conversation_per_room'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    closed_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    room = db.relationship('Room')
    user1 = db.relationship('User', foreign_keys=[user1_id])
    user2 = db.relationship('User', foreign_keys=[user2_id])
    messages = db.relationship('PrivateMessage', back_populates='conversation', cascade='all, delete-orphan')
    request = db.relationship('ConnectionRequest', back_populates='conversation', uselist=False)
    
    def is_expired(self):
        """Check if conversation has expired"""
        return self.expires_at and datetime.utcnow() >= self.expires_at
    
    def check_and_expire(self):
        """Check and expire conversation if needed"""
        if self.is_expired() and self.is_active:
            self.is_active = False
            self.closed_at = datetime.utcnow()
            return True
        return False
    
    @staticmethod
    def calculate_expiry_duration(subscription_tier):
        """Calculate conversation duration based on subscription tier"""
        durations = {
            'free': timedelta(hours=24),
            'premium': timedelta(days=7),
            'platinum': timedelta(days=30)
        }
        return durations.get(subscription_tier, timedelta(hours=24))
    
    def to_dict(self, current_user_id):
        other_user = self.user2 if self.user1_id == current_user_id else self.user1
        unread_count = sum(1 for msg in self.messages if msg.sender_id != current_user_id and not msg.is_read)
        return {
            'id': self.id,
            'room_id': self.room_id,
            'room_name': self.room.name if self.room else None,
            'other_user_id': other_user.id,
            'other_user_name': other_user.name,
            'other_user_photo_url': other_user.photo_url,
            'other_user_verified': other_user.is_verified,
            'started_at': self.started_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'closed_at': self.closed_at.isoformat() if self.closed_at else None,
            'is_active': self.is_active,
            'message_count': len(self.messages),
            'unread_count': unread_count
        }
