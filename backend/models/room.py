#
# MatchSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from backend import db
from datetime import datetime, timedelta

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
    access_meeting_type = db.Column(db.String(100))
    access_religion = db.Column(db.String(100))
    access_lgbtq_friendly = db.Column(db.String(50))
    
    max_capacity = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    access_code = db.Column(db.String(8), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    establishment = db.relationship('Establishment', back_populates='rooms')
    members = db.relationship('RoomMember', back_populates='room', cascade='all, delete-orphan')
    messages = db.relationship('Message', back_populates='room', cascade='all, delete-orphan')
    connection_requests = db.relationship('ConnectionRequest', back_populates='room', cascade='all, delete-orphan')
    
    def is_expired(self):
        return self.expires_at and datetime.utcnow() >= self.expires_at
    
    def check_and_expire(self):
        if self.is_expired() and self.is_active:
            self.is_active = False
            for member in self.members:
                if member.active:
                    member.active = False
                    member.left_at = datetime.utcnow()
            return True
        return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'photo_url': self.photo_url,
            'welcome_message': self.welcome_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'max_capacity': self.max_capacity,
            'member_count': len(self.members),
            'is_active': self.is_active,
            'access_gender': self.access_gender,
            'access_orientation': self.access_orientation,
            'access_age_min': self.access_age_min,
            'access_age_max': self.access_age_max,
            'access_meeting_type': self.access_meeting_type,
            'access_religion': self.access_religion,
            'access_lgbtq_friendly': self.access_lgbtq_friendly
        }
