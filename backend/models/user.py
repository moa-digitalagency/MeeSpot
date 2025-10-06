#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from backend import db
from backend.utils.encrypted_types import EncryptedString, EncryptedText
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
import random
import string

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(EncryptedString(500), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(EncryptedString(500), nullable=False)
    username = db.Column(db.String(50), unique=True)
    role = db.Column(db.String(20), nullable=False, default='user')
    
    gender = db.Column(db.String(20))
    sexual_orientation = db.Column(db.String(50))
    birthdate = db.Column(db.Date)
    age = db.Column(db.Integer)
    religion = db.Column(db.String(100))
    lgbtq_friendly = db.Column(db.String(50))
    bio = db.Column(EncryptedText(2000))
    photo_url = db.Column(EncryptedString(1000))
    gallery_photos = db.Column(JSON, default=list)
    
    meeting_type = db.Column(db.String(100))
    interests = db.Column(JSON, default=list)
    
    subscription_tier = db.Column(db.String(20), default='free')
    alternative_mode = db.Column(db.Boolean, default=False)
    alternative_name = db.Column(EncryptedString(500))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    rooms = db.relationship('RoomMember', back_populates='user', cascade='all, delete-orphan')
    messages = db.relationship('Message', back_populates='user', cascade='all, delete-orphan')
    reports_made = db.relationship('Report', foreign_keys='Report.reporter_id', back_populates='reporter')
    
    @staticmethod
    def generate_username(base_name):
        """Generate unique username from name"""
        clean_name = ''.join(c.lower() for c in base_name if c.isalnum())[:20]
        random_suffix = ''.join(random.choices(string.digits, k=4))
        username = f"{clean_name}{random_suffix}"
        
        while User.query.filter_by(username=username).first():
            random_suffix = ''.join(random.choices(string.digits, k=4))
            username = f"{clean_name}{random_suffix}"
        
        return username
    
    def calculate_age(self):
        """Calculate age from birthdate"""
        if self.birthdate:
            today = datetime.now().date()
            age = today.year - self.birthdate.year
            if today.month < self.birthdate.month or (today.month == self.birthdate.month and today.day < self.birthdate.day):
                age -= 1
            return age
        return self.age
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'subscription_tier': self.subscription_tier,
            'gender': self.gender,
            'sexual_orientation': self.sexual_orientation,
            'birthdate': self.birthdate.isoformat() if self.birthdate else None,
            'age': self.calculate_age() if self.birthdate else self.age,
            'religion': self.religion,
            'lgbtq_friendly': self.lgbtq_friendly,
            'bio': self.bio,
            'photo_url': self.photo_url,
            'gallery_photos': self.gallery_photos or [],
            'meeting_type': self.meeting_type,
            'interests': self.interests or [],
            'alternative_mode': self.alternative_mode
        }
    
    def to_public_dict(self):
        """Return only public profile information (no sensitive data)"""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.calculate_age() if self.birthdate else self.age,
            'gender': self.gender,
            'sexual_orientation': self.sexual_orientation,
            'religion': self.religion,
            'lgbtq_friendly': self.lgbtq_friendly,
            'bio': self.bio,
            'photo_url': self.photo_url,
            'gallery_photos': self.gallery_photos or [],
            'meeting_type': self.meeting_type,
            'interests': self.interests or []
        }
