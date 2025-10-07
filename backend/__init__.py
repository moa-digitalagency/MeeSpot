#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../static')
    
    # Configuration CORS pour production et développement
    # Note: L'app utilise localStorage (pas de cookies), donc supports_credentials=False
    CORS(app, 
         resources={r"/api/*": {"origins": "*"}},
         supports_credentials=False,
         allow_headers=["Content-Type", "Authorization", "X-API-Key"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    @app.after_request
    def add_no_cache_headers(response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    
    db.init_app(app)
    
    with app.app_context():
        from backend.routes import auth, rooms, admin, establishments, profile, connection_requests, conversations, profile_options
        
        app.register_blueprint(auth.bp)
        app.register_blueprint(rooms.bp)
        app.register_blueprint(admin.bp)
        app.register_blueprint(establishments.bp)
        app.register_blueprint(profile.bp)
        app.register_blueprint(connection_requests.bp)
        app.register_blueprint(conversations.bp)
        app.register_blueprint(profile_options.bp)
        
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
