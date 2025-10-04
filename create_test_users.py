#!/usr/bin/env python3
"""
Script pour créer les comptes de test
Run: python create_test_users.py
"""
import bcrypt
from main import app
from backend import db
from backend.models import User, Establishment

def create_test_accounts():
    with app.app_context():
        db.create_all()
        
        print("Création des comptes de test...")
        
        # 1. Superadmin
        admin_email = "admin@meetspot.com"
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            password_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin = User(
                email=admin_email,
                password_hash=password_hash,
                name="Admin MeetSpot",
                role='admin',
                gender='other',
                age=35,
                orientation='other'
            )
            db.session.add(admin)
            print(f"✓ Superadmin créé: {admin_email} / admin123")
        else:
            print(f"✓ Superadmin existe: {admin_email}")
        
        # 2. Establishment
        est_email = "cafe@paris.com"
        est_user = User.query.filter_by(email=est_email).first()
        if not est_user:
            password_hash = bcrypt.hashpw("cafe123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            est_user = User(
                email=est_email,
                password_hash=password_hash,
                name="Café de Paris",
                role='establishment',
                gender='other',
                age=30,
                orientation='other'
            )
            db.session.add(est_user)
            db.session.flush()
            
            establishment = Establishment(
                user_id=est_user.id,
                name="Café de Paris",
                description="Un lieu chaleureux pour des rencontres authentiques",
                address="123 Rue de Rivoli, Paris",
                subscription_plan='gold',
                subscription_price=99.0
            )
            db.session.add(establishment)
            print(f"✓ Établissement créé: {est_email} / cafe123")
        else:
            print(f"✓ Établissement existe: {est_email}")
        
        # 3. User 1 - Marie (Premium)
        user1_email = "marie@test.com"
        user1 = User.query.filter_by(email=user1_email).first()
        if not user1:
            password_hash = bcrypt.hashpw("marie123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user1 = User(
                email=user1_email,
                password_hash=password_hash,
                name="Marie Dupont",
                role='user',
                gender='female',
                age=28,
                orientation='straight',
                bio="Passionnée de musique et de voyages",
                subscription_tier='premium'
            )
            db.session.add(user1)
            print(f"✓ Utilisateur 1 créé: {user1_email} / marie123")
        else:
            print(f"✓ Utilisateur 1 existe: {user1_email}")
        
        # 4. User 2 - Thomas (Gratuit)
        user2_email = "thomas@test.com"
        user2 = User.query.filter_by(email=user2_email).first()
        if not user2:
            password_hash = bcrypt.hashpw("thomas123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user2 = User(
                email=user2_email,
                password_hash=password_hash,
                name="Thomas Martin",
                role='user',
                gender='male',
                age=32,
                orientation='straight',
                bio="Entrepreneur et amateur de bonne cuisine",
                subscription_tier='free'
            )
            db.session.add(user2)
            print(f"✓ Utilisateur 2 créé: {user2_email} / thomas123")
        else:
            print(f"✓ Utilisateur 2 existe: {user2_email}")
        
        db.session.commit()
        
        print("\n" + "="*60)
        print("COMPTES DE TEST CRÉÉS!")
        print("="*60)
        print("\n📋 ACCÈS:\n")
        print("1. SUPERADMIN: admin@meetspot.com / admin123")
        print("2. ÉTABLISSEMENT: cafe@paris.com / cafe123")
        print("3. UTILISATEUR 1: marie@test.com / marie123 (Premium)")
        print("4. UTILISATEUR 2: thomas@test.com / thomas123 (Gratuit)")
        print("\n" + "="*60)

if __name__ == '__main__':
    create_test_accounts()
