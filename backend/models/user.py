from backend import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    
    gender = db.Column(db.String(20))
    orientation = db.Column(db.String(50))
    age = db.Column(db.Integer)
    bio = db.Column(db.Text)
    photo_url = db.Column(db.String(500))
    
    subscription_tier = db.Column(db.String(20), default='free')
    alternative_mode = db.Column(db.Boolean, default=False)
    alternative_name = db.Column(db.String(100))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    rooms = db.relationship('RoomMember', back_populates='user', cascade='all, delete-orphan')
    messages = db.relationship('Message', back_populates='user', cascade='all, delete-orphan')
    reports_made = db.relationship('Report', foreign_keys='Report.reporter_id', back_populates='reporter')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'subscription_tier': self.subscription_tier,
            'gender': self.gender,
            'orientation': self.orientation,
            'age': self.age,
            'bio': self.bio,
            'photo_url': self.photo_url,
            'alternative_mode': self.alternative_mode
        }
