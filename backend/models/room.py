from backend import db
from datetime import datetime

class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    establishment_id = db.Column(db.Integer, db.ForeignKey('establishments.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    photo_url = db.Column(db.String(500))
    welcome_message = db.Column(db.Text)
    
    access_gender = db.Column(db.String(50))
    access_orientation = db.Column(db.String(50))
    access_age_min = db.Column(db.Integer)
    access_age_max = db.Column(db.Integer)
    
    event_datetime = db.Column(db.DateTime)
    max_capacity = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    establishment = db.relationship('Establishment', back_populates='rooms')
    members = db.relationship('RoomMember', back_populates='room', cascade='all, delete-orphan')
    messages = db.relationship('Message', back_populates='room', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'photo_url': self.photo_url,
            'welcome_message': self.welcome_message,
            'event_datetime': self.event_datetime.isoformat() if self.event_datetime else None,
            'max_capacity': self.max_capacity,
            'member_count': len(self.members),
            'is_active': self.is_active
        }
