from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import bcrypt
import jwt
from functools import wraps

app = Flask(__name__, static_folder='static')
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

db = SQLAlchemy(app)

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
    
    event_datetime = db.Column(db.DateTime)
    max_capacity = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    establishment = db.relationship('Establishment', back_populates='rooms')
    members = db.relationship('RoomMember', back_populates='room', cascade='all, delete-orphan')
    messages = db.relationship('Message', back_populates='room', cascade='all, delete-orphan')

class RoomMember(db.Model):
    __tablename__ = 'room_members'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    room = db.relationship('Room', back_populates='members')
    user = db.relationship('User', back_populates='rooms')

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_announcement = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    room = db.relationship('Room', back_populates='messages')
    user = db.relationship('User', back_populates='messages')

class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reported_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    reporter = db.relationship('User', foreign_keys=[reporter_id], back_populates='reports_made')

class SubscriptionPlan(db.Model):
    __tablename__ = 'subscription_plans'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    rooms_per_day = db.Column(db.Integer, default=1)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'User not found'}), 401
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    user = User(
        email=data['email'],
        password_hash=password_hash,
        name=data['name'],
        role=data.get('role', 'user'),
        gender=data.get('gender'),
        orientation=data.get('orientation'),
        age=data.get('age'),
        bio=data.get('bio')
    )
    
    db.session.add(user)
    db.session.commit()
    
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'subscription_tier': user.subscription_tier
        }
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'subscription_tier': user.subscription_tier
        }
    })

@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify({
        'id': current_user.id,
        'name': current_user.name,
        'email': current_user.email,
        'role': current_user.role,
        'gender': current_user.gender,
        'orientation': current_user.orientation,
        'age': current_user.age,
        'bio': current_user.bio,
        'photo_url': current_user.photo_url,
        'subscription_tier': current_user.subscription_tier,
        'alternative_mode': current_user.alternative_mode
    })

@app.route('/api/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.json
    
    if 'name' in data:
        current_user.name = data['name']
    if 'gender' in data:
        current_user.gender = data['gender']
    if 'orientation' in data:
        current_user.orientation = data['orientation']
    if 'age' in data:
        current_user.age = data['age']
    if 'bio' in data:
        current_user.bio = data['bio']
    if 'photo_url' in data:
        current_user.photo_url = data['photo_url']
    if 'alternative_mode' in data and current_user.subscription_tier in ['premium', 'platinum']:
        current_user.alternative_mode = data['alternative_mode']
    if 'alternative_name' in data and current_user.subscription_tier in ['premium', 'platinum']:
        current_user.alternative_name = data['alternative_name']
    
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'})

@app.route('/api/rooms', methods=['GET'])
@token_required
def get_rooms(current_user):
    rooms = Room.query.filter_by(is_active=True).all()
    
    accessible_rooms = []
    for room in rooms:
        if check_room_access(room, current_user):
            establishment = room.establishment
            accessible_rooms.append({
                'id': room.id,
                'name': room.name,
                'description': room.description,
                'photo_url': room.photo_url,
                'event_datetime': room.event_datetime.isoformat() if room.event_datetime else None,
                'max_capacity': room.max_capacity,
                'member_count': len(room.members),
                'establishment_name': establishment.name if establishment else None
            })
    
    return jsonify(accessible_rooms)

@app.route('/api/rooms/<int:room_id>', methods=['GET'])
@token_required
def get_room(current_user, room_id):
    room = Room.query.get_or_404(room_id)
    
    if not check_room_access(room, current_user):
        return jsonify({'message': 'Access denied to this room'}), 403
    
    establishment = room.establishment
    return jsonify({
        'id': room.id,
        'name': room.name,
        'description': room.description,
        'photo_url': room.photo_url,
        'welcome_message': room.welcome_message,
        'event_datetime': room.event_datetime.isoformat() if room.event_datetime else None,
        'max_capacity': room.max_capacity,
        'member_count': len(room.members),
        'establishment': {
            'name': establishment.name,
            'address': establishment.address
        }
    })

@app.route('/api/rooms/<int:room_id>/join', methods=['POST'])
@token_required
def join_room(current_user, room_id):
    room = Room.query.get_or_404(room_id)
    
    if not check_room_access(room, current_user):
        return jsonify({'message': 'Access denied to this room'}), 403
    
    if RoomMember.query.filter_by(room_id=room_id, user_id=current_user.id).first():
        return jsonify({'message': 'Already a member'}), 400
    
    if room.max_capacity and len(room.members) >= room.max_capacity:
        return jsonify({'message': 'Room is full'}), 400
    
    member = RoomMember(room_id=room_id, user_id=current_user.id)
    db.session.add(member)
    db.session.commit()
    
    return jsonify({'message': 'Joined room successfully'})

@app.route('/api/rooms/<int:room_id>/messages', methods=['GET'])
@token_required
def get_messages(current_user, room_id):
    if not RoomMember.query.filter_by(room_id=room_id, user_id=current_user.id).first():
        return jsonify({'message': 'Must join room first'}), 403
    
    messages = Message.query.filter_by(room_id=room_id).order_by(Message.created_at).all()
    
    return jsonify([{
        'id': msg.id,
        'user_name': msg.user.alternative_name if msg.user.alternative_mode and msg.user.alternative_name else msg.user.name,
        'content': msg.content,
        'is_announcement': msg.is_announcement,
        'created_at': msg.created_at.isoformat()
    } for msg in messages])

@app.route('/api/rooms/<int:room_id>/messages', methods=['POST'])
@token_required
def send_message(current_user, room_id):
    if not RoomMember.query.filter_by(room_id=room_id, user_id=current_user.id).first():
        return jsonify({'message': 'Must join room first'}), 403
    
    data = request.json
    message = Message(
        room_id=room_id,
        user_id=current_user.id,
        content=data['content'],
        is_announcement=False
    )
    db.session.add(message)
    db.session.commit()
    
    return jsonify({'message': 'Message sent successfully'})

@app.route('/api/establishments', methods=['POST'])
@token_required
def create_establishment(current_user):
    if current_user.role not in ['admin', 'establishment']:
        return jsonify({'message': 'Only establishments can create venues'}), 403
    
    data = request.json
    establishment = Establishment(
        user_id=current_user.id,
        name=data['name'],
        description=data.get('description'),
        address=data.get('address'),
        subscription_plan='one-shot',
        subscription_price=9.0
    )
    db.session.add(establishment)
    db.session.commit()
    
    return jsonify({'id': establishment.id, 'message': 'Establishment created successfully'})

@app.route('/api/establishments/<int:est_id>/rooms', methods=['POST'])
@token_required
def create_room(current_user, est_id):
    establishment = Establishment.query.get_or_404(est_id)
    
    if establishment.user_id != current_user.id and current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    
    today = datetime.utcnow().date()
    if establishment.last_room_reset != today:
        establishment.rooms_created_today = 0
        establishment.last_room_reset = today
    
    max_rooms = {
        'one-shot': 1,
        'silver': 1,
        'gold': 3
    }.get(establishment.subscription_plan, 1)
    
    if establishment.rooms_created_today >= max_rooms:
        return jsonify({'message': f'Daily room limit reached ({max_rooms} rooms)'}), 400
    
    data = request.json
    room = Room(
        establishment_id=est_id,
        name=data['name'],
        description=data.get('description'),
        photo_url=data.get('photo_url'),
        welcome_message=data.get('welcome_message'),
        access_gender=data.get('access_gender'),
        access_orientation=data.get('access_orientation'),
        access_age_min=data.get('access_age_min'),
        access_age_max=data.get('access_age_max'),
        event_datetime=datetime.fromisoformat(data['event_datetime']) if data.get('event_datetime') else None,
        max_capacity=data.get('max_capacity')
    )
    db.session.add(room)
    establishment.rooms_created_today += 1
    db.session.commit()
    
    return jsonify({'id': room.id, 'message': 'Room created successfully'})

@app.route('/api/admin/users', methods=['GET'])
@token_required
@admin_required
def get_users(current_user):
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'subscription_tier': user.subscription_tier,
        'created_at': user.created_at.isoformat()
    } for user in users])

@app.route('/api/admin/reports', methods=['GET'])
@token_required
@admin_required
def get_reports(current_user):
    reports = Report.query.all()
    return jsonify([{
        'id': report.id,
        'reporter_name': report.reporter.name,
        'reason': report.reason,
        'status': report.status,
        'created_at': report.created_at.isoformat()
    } for report in reports])

@app.route('/api/reports', methods=['POST'])
@token_required
def create_report(current_user):
    data = request.json
    report = Report(
        reporter_id=current_user.id,
        reported_user_id=data.get('reported_user_id'),
        room_id=data.get('room_id'),
        reason=data['reason']
    )
    db.session.add(report)
    db.session.commit()
    
    return jsonify({'message': 'Report submitted successfully'})

def check_room_access(room, user):
    if room.access_gender and user.gender != room.access_gender:
        return False
    if room.access_orientation and user.orientation != room.access_orientation:
        return False
    if room.access_age_min and user.age and user.age < room.access_age_min:
        return False
    if room.access_age_max and user.age and user.age > room.access_age_max:
        return False
    return True

@app.before_request
def init_db():
    if not hasattr(app, 'db_initialized'):
        with app.app_context():
            db.create_all()
            
            if not SubscriptionPlan.query.first():
                plans = [
                    SubscriptionPlan(name='one-shot', price=9.0, rooms_per_day=1, description='Create 1 room per day'),
                    SubscriptionPlan(name='silver', price=49.0, rooms_per_day=1, description='Create 1 room per day'),
                    SubscriptionPlan(name='gold', price=99.0, rooms_per_day=3, description='Create up to 3 rooms per day')
                ]
                for plan in plans:
                    db.session.add(plan)
                db.session.commit()
        
        app.db_initialized = True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
