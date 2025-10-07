#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from backend import db
from datetime import datetime

class VerificationRequest(db.Model):
    __tablename__ = 'verification_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    photo_url = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    admin_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='verification_requests')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])
    
    def to_dict(self):
        user_age = None
        user_name = None
        user_email = None
        user_gender = None
        user_bio = None
        user_photo_url = None
        
        if self.user:
            try:
                user_name = self.user.name
            except:
                pass
            
            try:
                user_email = self.user.email
            except:
                pass
            
            try:
                user_gender = self.user.gender
            except:
                pass
            
            try:
                user_bio = self.user.bio
            except:
                pass
            
            try:
                user_photo_url = self.user.photo_url
            except:
                pass
            
            try:
                if self.user.birthdate:
                    from datetime import date
                    today = date.today()
                    user_age = today.year - self.user.birthdate.year - ((today.month, today.day) < (self.user.birthdate.month, self.user.birthdate.day))
            except:
                pass
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': user_name,
            'user_email': user_email,
            'user_gender': user_gender,
            'user_age': user_age,
            'user_bio': user_bio,
            'user_photo_url': user_photo_url,
            'photo_url': self.photo_url,
            'status': self.status,
            'admin_notes': self.admin_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'reviewed_by': self.reviewed_by
        }
