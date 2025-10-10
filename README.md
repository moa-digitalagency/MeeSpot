# MatchSpot - Plateforme de Rencontres PWA

[🇬🇧 English Version](./README_EN.md) | 🇫🇷 Version Française

## 📱 Présentation

MatchSpot est une application web progressive (PWA) de rencontres qui met l'accent sur les rencontres réelles dans des lieux physiques. Inspirée des interfaces épurées de Bumble et Hinge, elle est construite avec un backend Python Flask et un frontend HTML/Tailwind CSS/JavaScript.

### 🎯 Concept Unique

Contrairement aux applications de rencontres traditionnelles basées sur le swipe infini, MatchSpot se concentre sur les connexions authentiques dans des rooms virtuelles organisées dans des établissements locaux.

## ✨ Fonctionnalités Principales

### 🏠 Système de Rooms
- **Expiration automatique 24h** : Toutes les rooms expirent 24 heures après leur création
- **Codes d'accès uniques** : Codes à 8 caractères pour rejoindre facilement les rooms
- **Scanner QR** : Rejoindre des rooms en scannant des codes QR avec la caméra
- **Filtres d'accès** : Contrôle basé sur le genre, l'orientation et l'âge

### 💬 Système de Connexions
- **Pas de chat de groupe** : Focus sur les connexions individuelles
- **Demandes de connexion** : Envoyez des demandes aux participants qui vous intéressent
- **Conversations privées 1-to-1** : Messages chiffrés après acceptation de connexion
- **Conversations persistantes** : Les conversations restent actives après l'expiration des rooms

### 👤 Rôles Utilisateurs

#### Utilisateur
- Rejoindre des rooms avec codes d'accès ou QR
- Voir les participants des rooms
- Envoyer/accepter des demandes de connexion
- Conversations privées chiffrées

#### Établissement
- Créer des rooms (limités par abonnement)
- Gérer les participants
- Générer des codes QR pour les rooms
- Accès aux analytics

#### Administrateur
- Gestion de la plateforme
- Modération des utilisateurs
- Gestion des signalements

### 💎 Abonnements

**Pour les Utilisateurs :**
- **Gratuit** : Parcourir et rejoindre des rooms publiques
- **Premium** (19$/mois) : Accès prioritaire, mode identité alternative
- **Platinum** (39$/mois) : Accès VIP, messagerie illimitée

**Pour les Établissements :**
- **One-Shot** (9$) : 1 room par jour
- **Silver** (49$/mois) : 1 room/jour + analytics avancés
- **Gold** (99$/mois) : 3 rooms/jour + fonctionnalités premium

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.8+
- PostgreSQL
- Node.js (pour Tailwind CSS)

### Installation

1. **Cloner le dépôt**
```bash
git clone <repo-url>
cd matchspot
```

2. **Installer les dépendances Python**
```bash
pip install flask flask-cors flask-sqlalchemy psycopg2-binary bcrypt cryptography pyjwt python-dotenv
```

3. **Configuration de la base de données**
```bash
# La base de données PostgreSQL est automatiquement configurée sur Replit
# Pour un environnement local, configurez DATABASE_URL
export DATABASE_URL="postgresql://user:password@localhost/matchspot"
```

4. **Configuration de la clé de chiffrement**
```bash
# Développement : Clé générée automatiquement et sauvegardée dans .encryption_key
# Production : OBLIGATOIRE - Définir comme variable d'environnement
export ENCRYPTION_KEY="votre_clé_de_chiffrement_fernet"
```

5. **Lancer l'application**
```bash
python main.py
```

L'application sera accessible sur `http://localhost:5000`

### Premier Compte Admin

1. Créez un compte via le formulaire d'inscription
2. Mettez à jour le rôle dans la base de données :
```sql
UPDATE users SET role = 'admin' WHERE email = 'votre@email.com';
```

## 📱 Interface Utilisateur

### Navigation (4 onglets)
1. **Accueil** : Code d'accès, scanner QR, mes rooms
2. **Chat** : Liste des conversations privées
3. **Demandes** : Demandes reçues/envoyées
4. **Profil** : Gestion du profil et déconnexion

### Flux Utilisateur
1. Rejoindre une room (code ou QR)
2. Voir les participants
3. Envoyer des demandes de connexion
4. Accepter/Refuser les demandes
5. Discuter en privé après acceptation

## 🛠️ Architecture Technique

### Backend (Flask)
```
backend/
├── __init__.py              # Initialisation de l'app
├── config.py                # Configuration centralisée
├── models/                  # Modèles SQLAlchemy
│   ├── user.py
│   ├── room.py
│   ├── connection_request.py
│   ├── private_conversation.py
│   └── ...
├── routes/                  # Blueprints API
│   ├── auth.py
│   ├── rooms.py
│   ├── connection_requests.py
│   ├── conversations.py
│   └── ...
└── utils/                   # Utilitaires
    ├── auth.py             # JWT et décorateurs
    └── encryption.py       # Chiffrement AES-256
```

### Frontend
```
static/
└── pages/
    ├── index.html          # Landing page
    ├── app.html            # Dashboard utilisateur
    ├── establishment.html  # Dashboard établissement
    └── admin.html          # Dashboard admin
```

### Base de Données (PostgreSQL)

**Tables Principales :**
- `users` : Utilisateurs avec démographie et abonnements
- `establishments` : Établissements avec plans d'abonnement
- `rooms` : Rooms virtuelles avec expiration 24h
- `room_members` : Membres actifs des rooms
- `connection_request` : Demandes (pending/accepted/rejected)
- `private_conversation` : Conversations 1-to-1
- `private_message` : Messages chiffrés
- `reports` : Système de signalement

## 🔐 Sécurité

### Chiffrement des Données
Toutes les données sensibles sont chiffrées avec Fernet (AES-256) :
- Emails, noms, bios, photos des utilisateurs
- Contenu des messages
- Noms alternatifs (mode identité alternative)

### Authentification
- Tokens JWT pour l'authentification
- Mots de passe hachés avec bcrypt
- Contrôle d'accès basé sur les rôles

### Clé de Chiffrement
**⚠️ IMPORTANT** : La clé `ENCRYPTION_KEY` est essentielle
- **Développement** : Auto-générée et sauvegardée dans `.encryption_key`
- **Production** : **DOIT** être définie comme variable d'environnement
- Perdre cette clé = données chiffrées irrécupérables

## 📚 Documentation API

Consultez la [documentation complète de l'API](./API_DOCS_FR.md) pour tous les endpoints.

**Endpoints Principaux :**
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion
- `GET /api/rooms` - Liste des rooms
- `POST /api/rooms/join-by-code` - Rejoindre par code
- `GET /api/rooms/<id>/participants` - Voir les participants
- `POST /api/requests` - Envoyer une demande
- `GET /api/conversations` - Liste des conversations
- `POST /api/conversations/<id>/messages` - Envoyer un message

## 🎨 Design System

### Palette de Couleurs
- **Primaire** : #FF4458 (corail vibrant)
- **Secondaire** : #6C5CE7 (violet doux)
- **Accent** : #A29BFE (lavande)
- **Fond** : #FFEAA7 (crème chaleureux)
- **Texte** : #2D3436 (charbon)
- **Succès** : #00B894 (vert menthe)

### Typographie
- **Titres** : Poppins (600, 700)
- **Corps** : Inter (300-700)

## 📦 Déploiement

### Préparer pour la Production

1. **Variables d'environnement**
```bash
export FLASK_ENV=production
export SECRET_KEY="votre_clé_secrète_jwt"
export ENCRYPTION_KEY="votre_clé_chiffrement_fernet"
export DATABASE_URL="postgresql://..."
```

2. **Utiliser un serveur WSGI**
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port main:app
```

3. **Configuration HTTPS**
Toujours utiliser HTTPS en production pour protéger les tokens JWT et données.

### 🔄 Mise à Jour GitHub (VPS Uniquement)

**Mise à jour automatique GitHub** : La fonctionnalité de mise à jour en un clic depuis GitHub (`/api/admin/update`) est disponible sur votre **serveur VPS déployé** et fonctionne parfaitement pour mettre à jour l'application depuis GitHub avec :
- Backup automatique avant mise à jour
- Migration de base de données après mise à jour
- Installation des dépendances
- Persistance des données tout au long du processus

Cette fonctionnalité est conçue pour les environnements VPS en production (voir [DEPLOYMENT_VPS.md](./DEPLOYMENT_VPS.md) pour plus de détails).

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez nos directives de contribution.

## 📄 Licence

Ce projet est sous licence MIT.

## 🌐 Liens

- [Documentation API (Français)](./API_DOCS_FR.md)
- [Documentation API (Anglais)](./API_DOCS_EN.md)
- [English README](./README_EN.md)

## 📞 Support

Pour toute question ou problème, ouvrez une issue sur GitHub.

---

**Fait avec ❤️ pour favoriser les vraies connexions**
