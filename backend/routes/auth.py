#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from flask import Blueprint, request, jsonify
from backend import db
from backend.models.user import User
import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import current_app

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email_to_check = data['email'].lower().strip()
    
    users = User.query.all()
    for u in users:
        if u.email and u.email.lower() == email_to_check:
            return jsonify({'message': 'Email already exists'}), 400
    
    password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    user = User(
        email=data['email'],
        password_hash=password_hash,
        name=data['name'],
        username=User.generate_username(data['name']),
        role=data.get('role', 'user'),
        gender=data.get('gender'),
        sexual_orientation=data.get('sexual_orientation'),
        birthdate=datetime.strptime(data['birthdate'], '%Y-%m-%d').date() if data.get('birthdate') else None,
        religion=data.get('religion'),
        lgbtq_friendly=data.get('lgbtq_friendly'),
        bio=data.get('bio')
    )
    
    if data.get('meeting_types'):
        user.meeting_types = data['meeting_types']
    if data.get('interests'):
        user.interests = data['interests']
    
    db.session.add(user)
    db.session.commit()
    
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': user.to_dict()
    })

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email_to_find = data['email'].lower().strip()
    
    users = User.query.all()
    user = None
    for u in users:
        if u.email and u.email.lower() == email_to_find:
            user = u
            break
    
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': user.to_dict()
    })
