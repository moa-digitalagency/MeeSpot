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
from backend.models.establishment import Establishment
from backend.utils.auth import token_required
import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import current_app
import os
import base64
import uuid

bp = Blueprint('auth', __name__, url_prefix='/api')

@bp.route('/auth/register/user', methods=['POST'])
def register_user():
    data = request.json
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    if 'email' not in data or 'password' not in data or 'name' not in data:
        return jsonify({'message': 'Missing required fields'}), 400
    
    email_to_check = data['email'].lower().strip()
    
    # Check if email exists (handle decryption errors gracefully)
    users = User.query.all()
    for u in users:
        try:
            if u.email and u.email.lower() == email_to_check:
                return jsonify({'message': 'Email already exists'}), 400
        except Exception:
            # Skip users with corrupted encrypted data
            continue
    
    password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Photo URL is now passed directly (already uploaded via /api/upload/image)
    if not data.get('photo_url'):
        return jsonify({'message': 'Profile photo is required'}), 400
    
    photo_url = data.get('photo_url')
    
    # Gallery URLs are now passed directly (already uploaded)
    gallery_urls = data.get('gallery_urls', [])
    
    user = User(
        email=data['email'],
        password_hash=password_hash,
        name=data['name'],
        username=User.generate_username(data['name']),
        role='user',
        gender=data.get('gender'),
        sexual_orientation=data.get('sexual_orientation'),
        birthdate=datetime.strptime(data['birthdate'], '%Y-%m-%d').date() if data.get('birthdate') else None,
        religion=data.get('religion'),
        lgbtq_friendly=data.get('lgbtq_friendly'),
        bio=data.get('bio'),
        photo_url=photo_url,
        gallery_photos=gallery_urls
    )
    
    if data.get('meeting_type'):
        user.meeting_type = data['meeting_type']
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

@bp.route('/auth/register/establishment', methods=['POST'])
def register_establishment():
    data = request.json
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    if 'email' not in data or 'password' not in data or 'contact_name' not in data or 'establishment_name' not in data:
        return jsonify({'message': 'Missing required fields'}), 400
    
    email_to_check = data['email'].lower().strip()
    
    # Check if email exists (handle decryption errors gracefully)
    users = User.query.all()
    for u in users:
        try:
            if u.email and u.email.lower() == email_to_check:
                return jsonify({'message': 'Email already exists'}), 400
        except Exception:
            # Skip users with corrupted encrypted data
            continue
    
    password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    user = User(
        email=data['email'],
        password_hash=password_hash,
        name=data['contact_name'],
        username=User.generate_username(data['contact_name']),
        role='establishment'
    )
    
    db.session.add(user)
    db.session.flush()
    
    establishment = Establishment(
        user_id=user.id,
        name=data['establishment_name'],
        description=data.get('description', ''),
        address=data.get('address', '')
    )
    
    db.session.add(establishment)
    db.session.commit()
    
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': user.to_dict(),
        'establishment': establishment.to_dict()
    })

@bp.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    if 'email' not in data or 'password' not in data or 'name' not in data:
        return jsonify({'message': 'Missing required fields'}), 400
    
    email_to_check = data['email'].lower().strip()
    
    # Check if email exists (handle decryption errors gracefully)
    users = User.query.all()
    for u in users:
        try:
            if u.email and u.email.lower() == email_to_check:
                return jsonify({'message': 'Email already exists'}), 400
        except Exception:
            # Skip users with corrupted encrypted data
            continue
    
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
    
    if data.get('meeting_type'):
        user.meeting_type = data['meeting_type']
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

@bp.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    if 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Missing email or password'}), 400
    
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

@bp.route("/users/<int:user_id>/profile", methods=["GET"])
@token_required
def get_user_profile(current_user, user_id):
    """Get public profile of a user (sanitized - no sensitive data)"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_public_dict())
