#
# MatchSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from backend import db
from datetime import datetime

class SubscriptionRequest(db.Model):
    __tablename__ = 'subscription_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subscription_tier = db.Column(db.String(20), nullable=False)
    payment_type = db.Column(db.String(20), nullable=False, default='recurring')
    status = db.Column(db.String(20), nullable=False, default='pending')
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    rejection_reason = db.Column(db.String(500))
    
    user = db.relationship('User', foreign_keys=[user_id], backref='subscription_requests')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'subscription_tier': self.subscription_tier,
            'payment_type': self.payment_type,
            'status': self.status,
            'requested_at': self.requested_at.isoformat() if self.requested_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'reviewed_by': self.reviewed_by,
            'rejection_reason': self.rejection_reason,
            'user': {
                'id': self.user.id,
                'name': self.user.name,
                'email': self.user.email,
                'role': self.user.role
            } if self.user else None
        }
