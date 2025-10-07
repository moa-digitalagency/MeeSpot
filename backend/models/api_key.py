#
# MeetSpot - Modèle APIKey
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from backend import db
from datetime import datetime
import secrets

class APIKey(db.Model):
    __tablename__ = 'api_keys'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_used_at = db.Column(db.DateTime)
    
    # Relations
    creator = db.relationship('User', backref='api_keys_created')
    
    @staticmethod
    def generate_key():
        """Génère une clé API sécurisée"""
        return 'msp_' + secrets.token_urlsafe(48)
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            'id': self.id,
            'key': self.key,
            'name': self.name,
            'description': self.description,
            'created_by': self.created_by,
            'creator_email': self.creator.email if self.creator else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None
        }
    
    def to_dict_safe(self):
        """Version sécurisée sans exposer la clé complète"""
        return {
            'id': self.id,
            'key_preview': self.key[:12] + '...' + self.key[-4:] if len(self.key) > 16 else self.key[:8] + '...',
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None
        }
