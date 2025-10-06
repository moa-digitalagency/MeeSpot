from backend import db
from datetime import datetime

class RoomMember(db.Model):
    __tablename__ = 'room_members'
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    left_at = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)
    
    room = db.relationship('Room', back_populates='members')
    user = db.relationship('User', back_populates='rooms')
