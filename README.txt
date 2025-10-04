MEETSPOT - PWA Dating Platform
===============================

Structure du projet :
--------------------
backend/
  ├── models/          # Modèles de base de données (User, Room, etc.)
  ├── routes/          # Routes API modulaires (auth, rooms, admin, etc.)
  ├── utils/           # Utilitaires (auth decorators, room access)
  └── __init__.py      # Initialisation Flask et base de données

static/
  ├── pages/           # Pages HTML (index, app, admin, establishment)
  ├── locales/         # Fichiers de traduction (fr.json, en.json)
  ├── js/              # JavaScript (i18n support)
  ├── css/             # CSS custom
  ├── images/          # Images et icônes PWA
  ├── manifest.json    # Manifest PWA
  └── sw.js            # Service Worker

main.py                # Point d'entrée de l'application
create_test_users.py   # Script pour créer les comptes de test

Démarrage rapide :
-----------------
1. Créer les comptes de test :
   python create_test_users.py

2. L'application démarre automatiquement sur le port 5000

3. Comptes de test disponibles :
   - Admin: admin@meetspot.com / admin123
   - Établissement: cafe@paris.com / cafe123
   - Utilisateur 1: marie@test.com / marie123 (Premium)
   - Utilisateur 2: thomas@test.com / thomas123 (Gratuit)

Fonctionnalités :
----------------
✓ Authentification JWT
✓ 3 rôles : Admin, Établissement, Utilisateur
✓ Système de rooms avec contrôle d'accès (genre, âge, orientation)
✓ Abonnements : Free, Premium, Platinum
✓ Plans établissements : One-Shot ($9), Silver ($49), Gold ($99)
✓ Mode identité alternative (Premium/Platinum)
✓ Messagerie dans les rooms
✓ Système de signalement et modération
✓ Support multilingue (FR/EN)
✓ PWA avec service worker

API Endpoints :
--------------
POST /api/auth/register    - Inscription
POST /api/auth/login       - Connexion
GET  /api/profile          - Profil utilisateur
PUT  /api/profile          - Mise à jour profil
GET  /api/rooms            - Liste des rooms
GET  /api/rooms/<id>       - Détails d'une room
POST /api/rooms/<id>/join  - Rejoindre une room
GET  /api/admin/users      - Liste utilisateurs (admin)
GET  /api/admin/reports    - Liste signalements (admin)
POST /api/establishments   - Créer établissement
POST /api/establishments/<id>/rooms - Créer room
