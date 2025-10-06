#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from backend import db
from datetime import datetime

class Establishment(db.Model):
    __tablename__ = 'establishments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(300))
    
    subscription_plan = db.Column(db.String(20), default='one-shot')
    subscription_price = db.Column(db.Float, default=9.0)
    rooms_created_today = db.Column(db.Integer, default=0)
    last_room_reset = db.Column(db.Date, default=datetime.utcnow().date)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    rooms = db.relationship('Room', back_populates='establishment', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'subscription_plan': self.subscription_plan,
            'subscription_price': self.subscription_price
        }
