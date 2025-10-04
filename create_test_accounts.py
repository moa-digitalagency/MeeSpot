import os
import bcrypt
from app import app, db, User, Establishment

def create_test_accounts():
    with app.app_context():
        db.create_all()
        
        # Clear existing test accounts
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
            print(f"✓ Superadmin existe déjà: {admin_email}")
        
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
            
            # Create establishment
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
            print(f"✓ Établissement existe déjà: {est_email}")
        
        # 3. User 1 - Marie
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
            print(f"✓ Utilisateur 1 existe déjà: {user1_email}")
        
        # 4. User 2 - Thomas
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
            print(f"✓ Utilisateur 2 existe déjà: {user2_email}")
        
        db.session.commit()
        
        print("\n" + "="*60)
        print("COMPTES DE TEST CRÉÉS AVEC SUCCÈS!")
        print("="*60)
        print("\n📋 ACCÈS DE TEST:\n")
        print("1. SUPERADMIN:")
        print("   Email: admin@meetspot.com")
        print("   Mot de passe: admin123")
        print("   Rôle: Gestion complète de la plateforme\n")
        
        print("2. ÉTABLISSEMENT:")
        print("   Email: cafe@paris.com")
        print("   Mot de passe: cafe123")
        print("   Rôle: Créer et gérer des événements (Plan Gold)\n")
        
        print("3. UTILISATEUR 1 (Premium):")
        print("   Email: marie@test.com")
        print("   Mot de passe: marie123")
        print("   Profil: Marie, 28 ans, femme, abonnement Premium\n")
        
        print("4. UTILISATEUR 2 (Gratuit):")
        print("   Email: thomas@test.com")
        print("   Mot de passe: thomas123")
        print("   Profil: Thomas, 32 ans, homme, abonnement gratuit\n")
        
        print("="*60)
        print("Vous pouvez maintenant tester la plateforme!")
        print("="*60)

if __name__ == '__main__':
    create_test_accounts()
