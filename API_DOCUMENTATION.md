# MeetSpot - Documentation API Complète

## 📋 Table des Matières
- [Informations Générales](#informations-générales)
- [Authentification](#authentification)
- [APIs Utilisateurs](#apis-utilisateurs)
- [APIs Salles (Rooms)](#apis-salles-rooms)
- [APIs Établissements](#apis-établissements)
- [APIs Profil](#apis-profil)
- [APIs Demandes de Connexion](#apis-demandes-de-connexion)
- [APIs Conversations Privées](#apis-conversations-privées)
- [APIs Options de Profil](#apis-options-de-profil)
- [APIs Vérification](#apis-vérification)
- [APIs Upload](#apis-upload)
- [APIs Abonnements](#apis-abonnements)
- [APIs Administration](#apis-administration)

---

## 🔐 Informations Générales

### URL de Base
- **Development**: `http://localhost:5000`
- **Production**: Votre domaine Replit

### Headers Requis
```
Content-Type: application/json
Authorization: Bearer <token_jwt>
```

### Compte Admin par Défaut
- **Email**: `admin@meetspot.com`
- **Mot de passe**: `m33t5p0t`
- **Rôle**: `admin`

---

## 🔑 Authentification

### 1. Inscription Utilisateur
**POST** `/api/auth/register/user`

**Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe",
  "gender": "male",
  "sexual_orientation": "heterosexual",
  "birthdate": "1990-01-01",
  "religion": "catholic",
  "lgbtq_friendly": "yes",
  "bio": "Hello, I'm John!",
  "photo_url": "/uploads/profiles/xxx.jpg",
  "gallery_urls": ["/uploads/gallery/xxx.jpg"],
  "meeting_type": "dating",
  "interests": ["music", "sports"]
}
```

**Réponse:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": { ... }
}
```

### 2. Inscription Établissement
**POST** `/api/auth/register/establishment`

**Body:**
```json
{
  "email": "bar@example.com",
  "password": "password123",
  "contact_name": "John Manager",
  "establishment_name": "Cool Bar",
  "description": "Best bar in town",
  "address": "123 Main St"
}
```

### 3. Connexion
**POST** `/api/auth/login`

**Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Réponse:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    ...
  }
}
```

### 4. Obtenir Profil Utilisateur
**GET** `/api/users/<user_id>/profile`

**Headers:** `Authorization: Bearer <token>`

---

## 👤 APIs Utilisateurs

### Obtenir Mon Profil
**GET** `/api/profile`

**Headers:** `Authorization: Bearer <token>`

**Réponse:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "user@example.com",
  "role": "user",
  "age": 34,
  "gender": "male",
  "bio": "Hello!",
  ...
}
```

### Mettre à Jour Mon Profil
**PUT** `/api/profile`

**Body:**
```json
{
  "bio": "Updated bio",
  "gender": "male",
  "sexual_orientation": "heterosexual",
  "religion": "catholic",
  "lgbtq_friendly": "yes",
  "meeting_type": "dating",
  "interests": ["music", "sports"],
  "language": "fr",
  "theme": "dark"
}
```

### Changer Mot de Passe
**PUT** `/api/profile/password`

**Body:**
```json
{
  "current_password": "old_password",
  "new_password": "new_password"
}
```

### Désactiver Compte
**POST** `/api/profile/deactivate`

**Body:**
```json
{
  "password": "current_password"
}
```

---

## 🏠 APIs Salles (Rooms)

### 1. Obtenir Toutes les Salles
**GET** `/api/rooms`

**Headers:** `Authorization: Bearer <token>`

**Réponse:**
```json
[
  {
    "id": 1,
    "name": "Friday Night Meetup",
    "description": "Meet new people",
    "is_active": true,
    "max_capacity": 20,
    "establishment_name": "Cool Bar",
    ...
  }
]
```

### 2. Obtenir Détails d'une Salle
**GET** `/api/rooms/<room_id>`

### 3. Rejoindre une Salle
**POST** `/api/rooms/<room_id>/join`

### 4. Rejoindre par Code d'Accès
**POST** `/api/rooms/join-by-code`

**Body:**
```json
{
  "access_code": "ABC12345"
}
```

### 5. Mes Salles
**GET** `/api/rooms/my`

### 6. Quitter une Salle
**POST** `/api/rooms/<room_id>/leave`

### 7. Obtenir Messages d'une Salle
**GET** `/api/rooms/<room_id>/messages`

### 8. Envoyer Message dans une Salle
**POST** `/api/rooms/<room_id>/messages`

**Body:**
```json
{
  "content": "Hello everyone!"
}
```

### 9. Obtenir Participants d'une Salle
**GET** `/api/rooms/<room_id>/participants`

**Réponse:**
```json
[
  {
    "id": 2,
    "name": "Jane Doe",
    "age": 28,
    "gender": "female",
    "bio": "Love music",
    "photo_url": "/uploads/profiles/xxx.jpg",
    "meeting_type_emojis": ["💑"],
    "is_verified": true,
    "request_status": null
  }
]
```

---

## 🏢 APIs Établissements

### 1. Créer un Établissement
**POST** `/api/establishments`

**Headers:** `Authorization: Bearer <token>` (role: establishment ou admin)

**Body:**
```json
{
  "name": "Cool Bar",
  "description": "Best bar in town",
  "address": "123 Main St"
}
```

### 2. Mon Établissement
**GET** `/api/establishments/me`

### 3. Créer une Salle
**POST** `/api/establishments/<est_id>/rooms`

**Body:**
```json
{
  "name": "Friday Night Meetup",
  "description": "Meet new people",
  "photo_url": "/uploads/rooms/xxx.jpg",
  "welcome_message": "Welcome!",
  "access_gender": "all",
  "access_orientation": null,
  "access_age_min": 18,
  "access_age_max": 99,
  "access_meeting_type": null,
  "access_religion": null,
  "access_lgbtq_friendly": null,
  "max_capacity": 20
}
```

**Réponse:**
```json
{
  "id": 1,
  "access_code": "ABC12345",
  "message": "Room created successfully"
}
```

### 4. Mes Salles (Établissement)
**GET** `/api/establishments/me/rooms?status=active`

Query params: `status=all|active|expired`

### 5. Détails d'une Salle (Établissement)
**GET** `/api/establishments/me/rooms/<room_id>`

### 6. Analytics
**GET** `/api/establishments/me/analytics`

**Réponse:**
```json
{
  "total_rooms": 15,
  "active_rooms": 3,
  "total_members": 120,
  "rooms_today": 1,
  "max_rooms_today": 3
}
```

### 7. Mettre à Jour Nom de Salle
**PUT** `/api/establishments/rooms/<room_id>/update-name`

**Body:**
```json
{
  "name": "New Room Name"
}
```

---

## 💬 APIs Demandes de Connexion

### 1. Obtenir Mes Demandes
**GET** `/api/requests?type=received`

Query params: `type=sent|received`

### 2. Envoyer Demande de Connexion
**POST** `/api/requests`

**Body:**
```json
{
  "room_id": 1,
  "target_id": 2
}
```

### 3. Accepter Demande
**POST** `/api/requests/<request_id>/accept`

**Réponse:**
```json
{
  "message": "Request accepted",
  "conversation_id": 5
}
```

### 4. Rejeter Demande
**POST** `/api/requests/<request_id>/reject`

---

## 💭 APIs Conversations Privées

### 1. Obtenir Mes Conversations
**GET** `/api/conversations?filter=active`

Query params: `filter=all|active|expired`

### 2. Obtenir une Conversation
**GET** `/api/conversations/<conversation_id>`

### 3. Obtenir Messages
**GET** `/api/conversations/<conversation_id>/messages`

### 4. Envoyer Message
**POST** `/api/conversations/<conversation_id>/messages`

**Body:**
```json
{
  "content": "Hello!"
}
```

### 5. Envoyer Photo
**POST** `/api/conversations/<conversation_id>/send-photo`

**Form Data:** `photo=<file>`

---

## ⚙️ APIs Options de Profil

### 1. Obtenir Options
**GET** `/api/profile-options?category=meeting_type`

**Réponse:**
```json
{
  "meeting_type": [
    {
      "id": 1,
      "value": "dating",
      "label": "Dating",
      "emoji": "💑",
      "is_active": true
    }
  ]
}
```

### 2. Créer Option (Admin)
**POST** `/api/profile-options`

**Body:**
```json
{
  "category": "meeting_type",
  "value": "friendship",
  "label": "Friendship"
}
```

### 3. Mettre à Jour Option (Admin)
**PUT** `/api/profile-options/<option_id>`

### 4. Activer/Désactiver Option (Admin)
**POST** `/api/profile-options/<option_id>/toggle`

### 5. Supprimer Option (Admin)
**DELETE** `/api/profile-options/<option_id>`

---

## ✅ APIs Vérification

### 1. Demander Vérification
**POST** `/api/verification/request`

**Body:**
```json
{
  "photo": "data:image/jpeg;base64,..."
}
```

### 2. Statut de Vérification
**GET** `/api/verification/status`

### 3. Liste des Demandes (Admin)
**GET** `/api/verification/admin/list?status=pending`

### 4. Approuver Vérification (Admin)
**POST** `/api/verification/admin/<verification_id>/approve`

**Body (optionnel):**
```json
{
  "notes": "Verified successfully"
}
```

### 5. Rejeter Vérification (Admin)
**POST** `/api/verification/admin/<verification_id>/reject`

---

## 📤 APIs Upload

### Upload Image
**POST** `/api/upload/image`

**Body:**
```json
{
  "image": "data:image/jpeg;base64,...",
  "type": "profile"
}
```

Types: `profile` | `gallery`

**Réponse:**
```json
{
  "success": true,
  "url": "/uploads/profiles/xxx.jpg"
}
```

---

## 💎 APIs Abonnements

### 1. Demander Abonnement
**POST** `/api/subscriptions/request`

**Body:**
```json
{
  "subscription_tier": "premium"
}
```

Tiers: `free` | `premium` | `platinum`

### 2. Mes Demandes
**GET** `/api/subscriptions/my-requests`

### 3. Demandes en Attente (Admin)
**GET** `/api/subscriptions/pending`

### 4. Approuver Demande (Admin)
**POST** `/api/subscriptions/<request_id>/approve`

### 5. Rejeter Demande (Admin)
**POST** `/api/subscriptions/<request_id>/reject`

**Body:**
```json
{
  "reason": "Insufficient documentation"
}
```

---

## 🔧 APIs Administration

### 1. Obtenir Tous les Utilisateurs
**GET** `/api/admin/users`

**Headers:** `Authorization: Bearer <admin_token>`

### 2. Obtenir Utilisateur par ID
**GET** `/api/admin/users/<user_id>`

### 3. Obtenir Rapports
**GET** `/api/admin/reports`

### 4. Créer Rapport
**POST** `/api/admin/reports`

**Body:**
```json
{
  "reported_user_id": 5,
  "room_id": 1,
  "reason": "Inappropriate behavior"
}
```

### 5. Gestion des Backups

#### Créer Backup
**POST** `/api/admin/backup/create`

#### Liste Backups
**GET** `/api/admin/backup/list`

#### Télécharger Backup
**GET** `/api/admin/backup/download/<filename>`

#### Restaurer Backup
**POST** `/api/admin/backup/restore`

**Body:**
```json
{
  "backup_file": "meetspot_backup_20231015.tar.gz"
}
```

#### Supprimer Backup
**DELETE** `/api/admin/backup/delete/<filename>`

### 6. Mise à Jour depuis GitHub
**POST** `/api/admin/update`

### 7. Migration Base de Données
**POST** `/api/admin/database/migrate`

### 8. Logs

#### Liste Logs
**GET** `/api/admin/logs/list`

#### Voir Log
**GET** `/api/admin/logs/view/<filename>`

### 9. Gestion API Keys

#### Liste Clés API
**GET** `/api/admin/apikeys/list`

#### Créer Clé API
**POST** `/api/admin/apikeys/create`

**Body:**
```json
{
  "name": "Mobile App Key",
  "description": "API key for mobile app"
}
```

#### Révoquer Clé API
**POST** `/api/admin/apikeys/<key_id>/revoke`

#### Activer Clé API
**POST** `/api/admin/apikeys/<key_id>/activate`

#### Supprimer Clé API
**DELETE** `/api/admin/apikeys/<key_id>`

---

## 🛡️ Sécurité

### Chiffrement
- Les données sensibles (email, nom, bio, photo_url) sont chiffrées dans la base de données
- Clé de chiffrement générée automatiquement et stockée dans `.encryption_key`

### Authentification
- JWT (JSON Web Tokens) avec expiration de 30 jours
- Mots de passe hashés avec bcrypt

### Rôles
- `user`: Utilisateur standard
- `establishment`: Propriétaire d'établissement
- `admin`: Administrateur

---

## 📊 Modèles de Données

### User
- email (chiffré)
- password_hash
- name (chiffré)
- username
- role
- gender, sexual_orientation, birthdate, age
- religion, lgbtq_friendly
- bio (chiffré)
- photo_url (chiffré)
- gallery_photos
- meeting_type, interests
- subscription_tier
- is_verified
- language, theme

### Room
- establishment_id
- name
- description
- photo_url
- welcome_message
- access_gender, access_orientation
- access_age_min, access_age_max
- access_meeting_type, access_religion, access_lgbtq_friendly
- max_capacity
- access_code
- is_active
- created_at, expires_at (24h)

### PrivateConversation
- room_id
- user1_id, user2_id
- is_active
- started_at, expires_at
- Durée: free (2h), premium (12h), platinum (48h)

---

## 🎯 Fonctionnalités Principales

1. **Inscription & Authentification**
   - Utilisateurs et établissements
   - Compte admin par défaut

2. **Salles de Rencontre**
   - Création par établissements
   - Filtres d'accès (âge, genre, orientation, etc.)
   - Codes d'accès uniques
   - Expiration automatique (24h)

3. **Connexions & Conversations**
   - Demandes de connexion dans les salles
   - Conversations privées temporaires
   - Chat avec photos
   - Durée basée sur l'abonnement

4. **Vérification**
   - Demandes de vérification avec photo
   - Approbation par admin
   - Badge vérifié sur profil

5. **Abonnements**
   - Free, Premium, Platinum
   - Fonctionnalités avancées
   - Demandes approuvées par admin

6. **Administration**
   - Gestion utilisateurs
   - Backups automatiques
   - Mise à jour depuis GitHub
   - Gestion API keys
   - Logs et analytics

---

## 📝 Notes Importantes

- Port par défaut: **5000**
- Base de données: **PostgreSQL**
- Cache: Désactivé (headers no-cache)
- CORS: Activé pour `/api/*`
- Upload max: 10MB par image
- Formats acceptés: JPEG, PNG

---

## 🚀 Déploiement

L'application est configurée pour déploiement avec:
- Gunicorn (production)
- Autoscale deployment target
- PostgreSQL database
- File uploads dans `static/uploads/`

---

**Documentation générée le**: 2025-10-09
**Version**: 1.0.0
