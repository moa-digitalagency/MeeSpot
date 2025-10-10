#
# MatchSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from backend import db
from backend.models.profile_option import ProfileOption
from backend.models.user import User
from backend.models.establishment import Establishment
from backend.models.room import Room
from backend.models.room_member import RoomMember
import bcrypt
from datetime import datetime, date, timedelta
import random
import string

def seed_profile_options():
    """Seed profile options - persistantes au redémarrage"""
    
    # Vérifier si les options existent déjà
    if ProfileOption.query.first():
        print("✓ Options de profil déjà présentes dans la base de données")
        return
    
    options = [
        # Genres
        {'category': 'gender', 'value': 'male', 'label': 'Homme', 'emoji': '♂️'},
        {'category': 'gender', 'value': 'female', 'label': 'Femme', 'emoji': '♀️'},
        {'category': 'gender', 'value': 'non_binary', 'label': 'Non-binaire', 'emoji': '⚧️'},
        {'category': 'gender', 'value': 'other', 'label': 'Autre', 'emoji': '❓'},
        
        # Orientations Sexuelles
        {'category': 'sexual_orientation', 'value': 'heterosexual', 'label': 'Hétérosexuel(le)', 'emoji': None},
        {'category': 'sexual_orientation', 'value': 'homosexual', 'label': 'Homosexuel(le)', 'emoji': '🏳️‍🌈'},
        {'category': 'sexual_orientation', 'value': 'bisexual', 'label': 'Bisexuel(le)', 'emoji': '💗💜💙'},
        {'category': 'sexual_orientation', 'value': 'pansexual', 'label': 'Pansexuel(le)', 'emoji': '💖'},
        {'category': 'sexual_orientation', 'value': 'asexual', 'label': 'Asexuel(le)', 'emoji': '🖤🤍💜'},
        {'category': 'sexual_orientation', 'value': 'other', 'label': 'Autre', 'emoji': None},
        
        # Religions
        {'category': 'religion', 'value': 'none', 'label': 'Aucune / Athée', 'emoji': None},
        {'category': 'religion', 'value': 'catholic', 'label': 'Catholique', 'emoji': '✝️'},
        {'category': 'religion', 'value': 'protestant', 'label': 'Protestant', 'emoji': '✝️'},
        {'category': 'religion', 'value': 'orthodox', 'label': 'Orthodoxe', 'emoji': '☦️'},
        {'category': 'religion', 'value': 'muslim', 'label': 'Musulman', 'emoji': '☪️'},
        {'category': 'religion', 'value': 'jewish', 'label': 'Juif', 'emoji': '✡️'},
        {'category': 'religion', 'value': 'buddhist', 'label': 'Bouddhiste', 'emoji': '☸️'},
        {'category': 'religion', 'value': 'hindu', 'label': 'Hindou', 'emoji': '🕉️'},
        {'category': 'religion', 'value': 'spiritual', 'label': 'Spirituel', 'emoji': '🙏'},
        {'category': 'religion', 'value': 'other', 'label': 'Autre', 'emoji': None},
        
        # Types de Rencontre
        {'category': 'meeting_type', 'value': 'dating', 'label': 'Rencontres amoureuses', 'emoji': '💑'},
        {'category': 'meeting_type', 'value': 'friendship', 'label': 'Amitié', 'emoji': '🤝'},
        {'category': 'meeting_type', 'value': 'networking', 'label': 'Réseautage professionnel', 'emoji': '💼'},
        {'category': 'meeting_type', 'value': 'casual', 'label': 'Rencontres occasionnelles', 'emoji': '🎉'},
        {'category': 'meeting_type', 'value': 'serious', 'label': 'Relations sérieuses', 'emoji': '💍'},
        
        # Centres d'Intérêt
        {'category': 'interest', 'value': 'music', 'label': 'Musique', 'emoji': '🎵'},
        {'category': 'interest', 'value': 'sports', 'label': 'Sports', 'emoji': '⚽'},
        {'category': 'interest', 'value': 'art', 'label': 'Art', 'emoji': '🎨'},
        {'category': 'interest', 'value': 'cinema', 'label': 'Cinéma', 'emoji': '🎬'},
        {'category': 'interest', 'value': 'reading', 'label': 'Lecture', 'emoji': '📚'},
        {'category': 'interest', 'value': 'travel', 'label': 'Voyages', 'emoji': '✈️'},
        {'category': 'interest', 'value': 'cooking', 'label': 'Cuisine', 'emoji': '👨‍🍳'},
        {'category': 'interest', 'value': 'technology', 'label': 'Technologie', 'emoji': '💻'},
        {'category': 'interest', 'value': 'gaming', 'label': 'Jeux vidéo', 'emoji': '🎮'},
        {'category': 'interest', 'value': 'fitness', 'label': 'Fitness', 'emoji': '💪'},
        {'category': 'interest', 'value': 'photography', 'label': 'Photographie', 'emoji': '📷'},
        {'category': 'interest', 'value': 'dance', 'label': 'Danse', 'emoji': '💃'},
        {'category': 'interest', 'value': 'yoga', 'label': 'Yoga', 'emoji': '🧘'},
        {'category': 'interest', 'value': 'nature', 'label': 'Nature', 'emoji': '🌿'},
        {'category': 'interest', 'value': 'pets', 'label': 'Animaux', 'emoji': '🐶'},
        
        # LGBTQ+ Friendly
        {'category': 'lgbtq_friendly', 'value': 'yes', 'label': 'Oui', 'emoji': '🏳️‍🌈'},
        {'category': 'lgbtq_friendly', 'value': 'no', 'label': 'Non', 'emoji': None},
        {'category': 'lgbtq_friendly', 'value': 'prefer_not_say', 'label': 'Préfère ne pas dire', 'emoji': None},
    ]
    
    for option_data in options:
        option = ProfileOption(**option_data)
        db.session.add(option)
    
    db.session.commit()
    print(f"✓ {len(options)} options de profil créées avec succès")


def seed_default_users():
    """Seed default test users - persistants au redémarrage"""
    
    # Vérifier si les users de test existent déjà
    test_user1 = User.query.filter_by(username='sophie_test').first()
    if test_user1:
        print("✓ Utilisateurs de test déjà présents dans la base de données")
        return
    
    # Créer 2 utilisateurs de test
    users_data = [
        {
            'email': 'sophie@test.com',
            'password': 'test123',
            'name': 'Sophie Martin',
            'username': 'sophie_test',
            'role': 'user',
            'gender': 'female',
            'sexual_orientation': 'heterosexual',
            'birthdate': date(1995, 3, 15),
            'religion': 'none',
            'lgbtq_friendly': 'yes',
            'bio': 'Passionnée de musique et de voyages. J\'adore découvrir de nouveaux endroits et rencontrer des gens intéressants!',
            'meeting_type': 'dating',
            'interests': ['music', 'travel', 'photography', 'cinema']
        },
        {
            'email': 'julien@test.com',
            'password': 'test123',
            'name': 'Julien Dubois',
            'username': 'julien_test',
            'role': 'user',
            'gender': 'male',
            'sexual_orientation': 'heterosexual',
            'birthdate': date(1992, 7, 22),
            'religion': 'catholic',
            'lgbtq_friendly': 'yes',
            'bio': 'Amateur de sports et de technologie. Toujours partant pour une bonne soirée entre amis!',
            'meeting_type': 'friendship',
            'interests': ['sports', 'technology', 'gaming', 'fitness']
        }
    ]
    
    for user_data in users_data:
        password = user_data.pop('password')
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user = User(
            password_hash=password_hash,
            **user_data
        )
        user.age = user.calculate_age()
        
        db.session.add(user)
    
    db.session.commit()
    print(f"✓ {len(users_data)} utilisateurs de test créés (sophie@test.com / julien@test.com, mot de passe: test123)")


def seed_default_establishment():
    """Seed default establishment - persistant au redémarrage"""
    
    # Vérifier si l'établissement de test existe déjà
    test_establishment = Establishment.query.filter_by(name='Le Café Central').first()
    if test_establishment:
        print("✓ Établissement de test déjà présent dans la base de données")
        return
    
    # Vérifier si l'utilisateur existe déjà
    establishment_user = User.query.filter_by(username='cafe_central').first()
    
    if not establishment_user:
        # Créer un utilisateur établissement
        establishment_email = 'cafe@test.com'
        password_hash = bcrypt.hashpw('test123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        establishment_user = User(
            email=establishment_email,
            password_hash=password_hash,
            name='Café Central',
            username='cafe_central',
            role='establishment'
        )
        
        db.session.add(establishment_user)
        db.session.commit()
    
    # Créer l'établissement
    establishment = Establishment(
        user_id=establishment_user.id,
        name='Le Café Central',
        description='Un café chaleureux au cœur de la ville, parfait pour des rencontres authentiques. Ambiance conviviale et décontractée.',
        address='15 Rue de la République, 75001 Paris'
    )
    
    db.session.add(establishment)
    db.session.commit()
    
    print(f"✓ Établissement de test créé: {establishment.name} (cafe@test.com, mot de passe: test123)")


def seed_default_rooms():
    """Seed default test rooms - persistants au redémarrage"""
    
    # Vérifier si des rooms de test existent déjà
    test_room = Room.query.filter_by(name="It's Friday... Leets go").first()
    if test_room:
        print("✓ Rooms de test déjà présentes dans la base de données")
        return
    
    # Récupérer l'établissement de test
    establishment = Establishment.query.filter_by(name='Le Café Central').first()
    if not establishment:
        print("⚠️ Établissement de test non trouvé, impossible de créer des rooms")
        return
    
    # Récupérer les utilisateurs de test
    sophie = User.query.filter_by(username='sophie_test').first()
    julien = User.query.filter_by(username='julien_test').first()
    
    # Générer un code d'accès unique
    def generate_access_code():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # Créer une room de test active
    room = Room(
        establishment_id=establishment.id,
        name="It's Friday... Leets go",
        description="Ici c'est vendredi - Tout est permis",
        welcome_message="Bienvenue dans notre soirée du vendredi ! Profitez de l'ambiance et faites de belles rencontres.",
        access_code=generate_access_code(),
        max_capacity=50,
        is_active=True,
        expires_at=datetime.utcnow() + timedelta(hours=3),
        access_gender=None,
        access_orientation=None,
        access_age_min=18,
        access_age_max=None,
        access_meeting_type=None,
        access_religion=None,
        access_lgbtq_friendly=None
    )
    
    db.session.add(room)
    db.session.commit()
    
    # Ajouter les utilisateurs de test comme membres
    if sophie:
        member_sophie = RoomMember(
            room_id=room.id,
            user_id=sophie.id,
            joined_at=datetime.utcnow(),
            active=True
        )
        db.session.add(member_sophie)
    
    if julien:
        member_julien = RoomMember(
            room_id=room.id,
            user_id=julien.id,
            joined_at=datetime.utcnow(),
            active=True
        )
        db.session.add(member_julien)
    
    db.session.commit()
    
    member_count = 2 if sophie and julien else (1 if sophie or julien else 0)
    print(f"✓ Room de test créée: {room.name} avec {member_count} membres (Code: {room.access_code})")


def initialize_seed_data():
    """Initialize all seed data - appelé au démarrage de l'app"""
    print("\n=== Initialisation des données de base ===")
    seed_profile_options()
    seed_default_users()
    seed_default_establishment()
    seed_default_rooms()
    print("=== Initialisation terminée ===\n")
