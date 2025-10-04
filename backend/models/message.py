from backend import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_announcement = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    room = db.relationship('Room', back_populates='messages')
    user = db.relationship('User', back_populates='messages')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user.alternative_name if self.user.alternative_mode and self.user.alternative_name else self.user.name,
            'content': self.content,
            'is_announcement': self.is_announcement,
            'created_at': self.created_at.isoformat()
        }
