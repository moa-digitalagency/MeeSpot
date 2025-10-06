# Documentation API MeetSpot

[🇬🇧 English Version](./API_DOCS_EN.md) | 🇫🇷 Version Française

## Vue d'ensemble

**URL de base** : `https://votre-domaine.com/api`  
**Authentification** : JWT Bearer Token  
**Content-Type** : `application/json`

## Table des Matières

1. [Authentification](#authentification)
2. [Profil Utilisateur](#profil-utilisateur)
3. [Événements (Rooms)](#événements-rooms)
4. [Demandes de Connexion](#demandes-de-connexion)
5. [Conversations Privées](#conversations-privées)
6. [Établissements](#établissements)
7. [Administration](#administration)
8. [Codes d'Erreur](#codes-derreur)

---

## Authentification

### Inscription
Créer un nouveau compte utilisateur.

```http
POST /api/auth/register
```

**Corps de la requête** :
```json
{
  "email": "user@example.com",
  "password": "motdepasse123",
  "name": "Jean Dupont",
  "role": "user",
  "gender": "male",
  "orientation": "straight",
  "age": 28
}
```

**Réponse (201)** :
```json
{
  "message": "User created successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Connexion
Obtenir un token JWT.

```http
POST /api/auth/login
```

**Corps de la requête** :
```json
{
  "email": "user@example.com",
  "password": "motdepasse123"
}
```

**Réponse (200)** :
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "Jean Dupont",
    "role": "user"
  }
}
```

---

## Profil Utilisateur

### Obtenir le profil
```http
GET /api/profile
Authorization: Bearer {token}
```

**Réponse (200)** :
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "Jean Dupont",
  "age": 28,
  "gender": "male",
  "orientation": "straight",
  "bio": "Ma bio",
  "subscription_tier": "free",
  "alternative_mode": false
}
```

### Mettre à jour le profil
```http
PUT /api/profile
Authorization: Bearer {token}
```

**Corps de la requête** :
```json
{
  "name": "Jean Dupont",
  "bio": "Nouvelle bio",
  "photo_url": "https://example.com/photo.jpg",
  "alternative_mode": false,
  "alternative_name": "Nom alternatif"
}
```

---

## Événements (Rooms)

### Liste des événements
```http
GET /api/rooms
Authorization: Bearer {token}
```

**Réponse (200)** :
```json
[
  {
    "id": 1,
    "name": "Soirée Jazz",
    "description": "Soirée musicale",
    "establishment_name": "Le Bar à Vin",
    "event_datetime": "2025-10-15T20:00:00",
    "member_count": 15,
    "is_active": true,
    "created_at": "2025-10-14T12:00:00",
    "expires_at": "2025-10-15T12:00:00"
  }
]
```

### Rejoindre par code d'accès
```http
POST /api/rooms/join-by-code
Authorization: Bearer {token}
```

**Corps de la requête** :
```json
{
  "access_code": "ABC12345"
}
```

**Réponse (200)** :
```json
{
  "message": "Joined room successfully",
  "room_id": 1
}
```

### Mes événements
```http
GET /api/rooms/my
Authorization: Bearer {token}
```

Retourne tous les événements que l'utilisateur a rejoints.

### Voir les participants
```http
GET /api/rooms/{room_id}/participants
Authorization: Bearer {token}
```

**Réponse (200)** :
```json
[
  {
    "id": 2,
    "name": "Marie",
    "age": 25,
    "gender": "female",
    "bio": "Passionnée de musique",
    "photo_url": "https://...",
    "joined_at": "2025-10-14T19:30:00"
  }
]
```

### Quitter un événement
```http
POST /api/rooms/{room_id}/leave
Authorization: Bearer {token}
```

---

## Demandes de Connexion

### Liste des demandes
```http
GET /api/requests?type=received
Authorization: Bearer {token}
```

**Paramètres** :
- `type` : `received` (reçues) ou `sent` (envoyées)

**Réponse (200)** :
```json
[
  {
    "id": 1,
    "requester_id": 2,
    "requester_name": "Marie",
    "target_id": 1,
    "room_id": 1,
    "room_name": "Soirée Jazz",
    "status": "pending",
    "created_at": "2025-10-14T20:15:00"
  }
]
```

### Envoyer une demande
```http
POST /api/requests
Authorization: Bearer {token}
```

**Corps de la requête** :
```json
{
  "room_id": 1,
  "target_id": 2
}
```

**Réponse (201)** :
```json
{
  "message": "Request sent successfully",
  "id": 1
}
```

### Accepter une demande
```http
POST /api/requests/{request_id}/accept
Authorization: Bearer {token}
```

**Réponse (200)** :
```json
{
  "message": "Request accepted",
  "conversation_id": 1
}
```

### Refuser une demande
```http
POST /api/requests/{request_id}/reject
Authorization: Bearer {token}
```

---

## Conversations Privées

### Liste des conversations
```http
GET /api/conversations
Authorization: Bearer {token}
```

**Réponse (200)** :
```json
[
  {
    "id": 1,
    "user1_id": 1,
    "user2_id": 2,
    "user1_name": "Jean",
    "user2_name": "Marie",
    "room_id": 1,
    "room_name": "Soirée Jazz",
    "created_at": "2025-10-14T20:30:00"
  }
]
```

### Messages d'une conversation
```http
GET /api/conversations/{conversation_id}/messages
Authorization: Bearer {token}
```

**Réponse (200)** :
```json
[
  {
    "id": 1,
    "sender_id": 1,
    "content": "Salut ! Contente de te rencontrer",
    "created_at": "2025-10-14T20:35:00"
  }
]
```

### Envoyer un message
```http
POST /api/conversations/{conversation_id}/messages
Authorization: Bearer {token}
```

**Corps de la requête** :
```json
{
  "content": "Message de réponse"
}
```

---

## Établissements

### Créer un établissement
```http
POST /api/establishments
Authorization: Bearer {token}
```

**Corps de la requête** :
```json
{
  "name": "Le Bar à Vin",
  "description": "Bar cosy au centre-ville",
  "address": "123 Rue Principale",
  "subscription_plan": "one-shot"
}
```

### Créer un événement
```http
POST /api/establishments/{establishment_id}/rooms
Authorization: Bearer {token}
```

**Corps de la requête** :
```json
{
  "name": "Soirée Jazz",
  "description": "Concert live",
  "event_datetime": "2025-10-15T20:00:00",
  "welcome_message": "Bienvenue !",
  "access_gender": "all",
  "access_orientation": "all",
  "access_age_min": 18,
  "access_age_max": 65,
  "max_capacity": 50
}
```

**Réponse (200)** :
```json
{
  "id": 1,
  "access_code": "ABC12345",
  "message": "Room created successfully"
}
```

### Détails d'un événement (établissement)
```http
GET /api/establishments/me/rooms/{room_id}
Authorization: Bearer {token}
```

Retourne les détails complets incluant le code d'accès, la liste des membres et les statistiques.

---

## Administration

### Liste des utilisateurs
```http
GET /api/admin/users
Authorization: Bearer {token}
```

Rôle requis : `admin`

### Liste des signalements
```http
GET /api/admin/reports
Authorization: Bearer {token}
```

Rôle requis : `admin`

### Signaler un utilisateur ou événement
```http
POST /api/reports
Authorization: Bearer {token}
```

**Corps de la requête** :
```json
{
  "target_type": "user",
  "target_id": 2,
  "reason": "Comportement inapproprié",
  "description": "Description détaillée"
}
```

---

## Codes d'Erreur

| Code | Description |
|------|-------------|
| 200 | Succès |
| 201 | Créé avec succès |
| 400 | Requête invalide |
| 401 | Non authentifié |
| 403 | Non autorisé |
| 404 | Ressource non trouvée |
| 500 | Erreur serveur |

### Réponse d'erreur type
```json
{
  "message": "Description de l'erreur"
}
```

---

## Sécurité

### Chiffrement
Toutes les données sensibles sont chiffrées avec AES-256 :
- Emails et informations personnelles
- Messages privés
- Noms alternatifs

### Authentification
- Tokens JWT avec expiration
- Mots de passe hachés avec bcrypt
- HTTPS obligatoire en production

---

## Notes Importantes

1. **Expiration des événements** : Tous les événements expirent automatiquement 24 heures après leur création
2. **Membres actifs** : Les utilisateurs sont automatiquement marqués comme inactifs quand l'événement expire
3. **Conversations persistantes** : Les conversations privées restent actives même après l'expiration de l'événement
4. **Limite de requêtes** : Respectez les limites de taux pour éviter le blocage

---

**Documentation complète** : Consultez [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) pour plus de détails.
