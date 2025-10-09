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
    
    # Auto-détection de l'URL PostgreSQL
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        # Construction automatique depuis les variables individuelles (Replit, etc.)
        pguser = os.environ.get('PGUSER')
        pgpassword = os.environ.get('PGPASSWORD')
        pghost = os.environ.get('PGHOST')
        pgport = os.environ.get('PGPORT', '5432')
        pgdatabase = os.environ.get('PGDATABASE')
        
        if all([pguser, pgpassword, pghost, pgdatabase]):
            database_url = f"postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}"
            print(f"✓ URL PostgreSQL construite automatiquement depuis les variables d'environnement")
        else:
            print("⚠️  ATTENTION: Aucune configuration PostgreSQL trouvée")
    else:
        print(f"✓ URL PostgreSQL chargée depuis DATABASE_URL")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
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
        from backend.routes import auth, rooms, admin, establishments, profile, connection_requests, conversations, profile_options, verification, upload, subscriptions
        
        app.register_blueprint(auth.bp)
        app.register_blueprint(rooms.bp)
        app.register_blueprint(admin.bp)
        app.register_blueprint(establishments.bp)
        app.register_blueprint(profile.bp)
        app.register_blueprint(connection_requests.bp)
        app.register_blueprint(conversations.bp)
        app.register_blueprint(profile_options.bp)
        app.register_blueprint(verification.bp)
        app.register_blueprint(upload.bp)
        app.register_blueprint(subscriptions.bp)
        
        from backend.routes import static_routes
        app.register_blueprint(static_routes.bp)
        
        db.create_all()
        
        from backend.utils.db_migration import run_migrations
        run_migrations()
        
        from backend.models.subscription_plan import SubscriptionPlan
        
        user_plans_exist = SubscriptionPlan.query.filter_by(role='user').first() is not None
        establishment_plans_exist = SubscriptionPlan.query.filter_by(role='establishment').first() is not None
        
        if not user_plans_exist:
            user_plans = [
                SubscriptionPlan(name='free', price=0, rooms_per_day=0, description='Plan gratuit - Parcourir les rooms, rejoindre les rooms publiques, conversations 24h', role='user'),
                SubscriptionPlan(name='premium', price=19, rooms_per_day=0, description='Plan Premium - Accès prioritaire aux rooms, mode identité alternative, conversations de 7 jours', role='user'),
                SubscriptionPlan(name='platinum', price=39, rooms_per_day=0, description='Plan Platinum - Accès VIP aux rooms, messagerie illimitée, conversations de 30 jours, boost de profil', role='user')
            ]
            for plan in user_plans:
                db.session.add(plan)
            db.session.commit()
            print("✓ Plans d'abonnement utilisateurs créés")
        
        if not establishment_plans_exist:
            establishment_plans = [
                SubscriptionPlan(name='one-shot', price=9.0, rooms_per_day=1, description='Create 1 room per day', role='establishment'),
                SubscriptionPlan(name='silver', price=49.0, rooms_per_day=1, description='Create 1 room per day + analytics', role='establishment'),
                SubscriptionPlan(name='gold', price=99.0, rooms_per_day=3, description='Create up to 3 rooms per day', role='establishment')
            ]
            for plan in establishment_plans:
                db.session.add(plan)
            db.session.commit()
            print("✓ Plans d'abonnement établissements créés")
        
        from backend.models.user import User
        import bcrypt
        
        admin_email = 'admin@meetspot.com'
        admin_username = 'admin_meetspot'
        
        admin_exists = User.query.filter_by(username=admin_username).first() is not None
        
        if not admin_exists:
            admin_password = 'm33t5p0t'
            password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            admin_user = User(
                email=admin_email,
                password_hash=password_hash,
                name='Admin MeetSpot',
                username=admin_username,
                role='admin'
            )
            
            db.session.add(admin_user)
            db.session.commit()
            print(f"✓ Compte admin créé: {admin_email}")
        else:
            print(f"✓ Compte admin existant: {admin_username}")
        
        from backend.utils.seed_data import initialize_seed_data
        initialize_seed_data()
    
    return app
