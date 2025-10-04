from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../static')
    CORS(app)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    db.init_app(app)
    
    with app.app_context():
        from backend.routes import auth, rooms, admin, establishments, profile
        
        app.register_blueprint(auth.bp)
        app.register_blueprint(rooms.bp)
        app.register_blueprint(admin.bp)
        app.register_blueprint(establishments.bp)
        app.register_blueprint(profile.bp)
        
        from backend.routes import static_routes
        app.register_blueprint(static_routes.bp)
        
        db.create_all()
        
        from backend.models.subscription_plan import SubscriptionPlan
        if not SubscriptionPlan.query.first():
            plans = [
                SubscriptionPlan(name='one-shot', price=9.0, rooms_per_day=1, description='Create 1 room per day'),
                SubscriptionPlan(name='silver', price=49.0, rooms_per_day=1, description='Create 1 room per day + analytics'),
                SubscriptionPlan(name='gold', price=99.0, rooms_per_day=3, description='Create up to 3 rooms per day')
            ]
            for plan in plans:
                db.session.add(plan)
            db.session.commit()
    
    return app
