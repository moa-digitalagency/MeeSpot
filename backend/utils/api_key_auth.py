#
# MatchSpot - Authentification par clé API
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from functools import wraps
from flask import request, jsonify
from backend import db
from backend.models.api_key import APIKey
from datetime import datetime

def api_key_required(f):
    """Decorator pour vérifier la clé API"""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = None
        
        # Chercher la clé API dans les headers
        if 'X-API-Key' in request.headers:
            api_key = request.headers['X-API-Key']
        elif 'Authorization' in request.headers:
            auth = request.headers['Authorization']
            if auth.startswith('Bearer '):
                api_key = auth.replace('Bearer ', '')
        
        if not api_key:
            return jsonify({
                'success': False,
                'message': 'Clé API manquante. Utilisez le header X-API-Key ou Authorization: Bearer <key>'
            }), 401
        
        # Vérifier la clé dans la base de données
        key_record = APIKey.query.filter_by(key=api_key).first()
        
        if not key_record:
            return jsonify({
                'success': False,
                'message': 'Clé API invalide'
            }), 401
        
        if not key_record.is_active:
            return jsonify({
                'success': False,
                'message': 'Clé API révoquée'
            }), 401
        
        # Mettre à jour la date de dernière utilisation
        key_record.last_used_at = datetime.utcnow()
        db.session.commit()
        
        # Passer la clé API à la fonction
        return f(api_key_record=key_record, *args, **kwargs)
    
    return decorated
