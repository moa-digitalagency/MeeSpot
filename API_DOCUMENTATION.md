# MeetSpot API Documentation

## Overview
MeetSpot est une plateforme de rencontres basée sur des événements physiques dans des établissements réels. Cette API permet de gérer les utilisateurs, les événements (rooms), les établissements et la messagerie.

**Base URL**: `http://localhost:5000/api`
**Authentication**: JWT Bearer Token
**Content-Type**: `application/json`

---

## Authentication

### Register
Créer un nouveau compte utilisateur.

**Endpoint**: `POST /api/auth/register`

**Headers**: None required

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe",
  "role": "user",
  "gender": "male",
  "orientation": "straight",
  "age": 28
}
```

**Response** (201 Created):
```json
{
  "message": "User created successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses**:
- `400`: Email already exists
- `400`: Missing required fields

---

### Login
Se connecter et obtenir un JWT token.

**Endpoint**: `POST /api/auth/login`

**Headers**: None required

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response** (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "subscription_tier": "free"
  }
}
```

**Error Responses**:
- `401`: Invalid credentials

---

## Profile

### Get Profile
Récupérer le profil de l'utilisateur connecté.

**Endpoint**: `GET /api/profile`

**Headers**: 
```
Authorization: Bearer {token}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "subscription_tier": "premium",
  "gender": "male",
  "orientation": "straight",
  "age": 28,
  "bio": "Passionate about meeting new people!",
  "photo_url": "https://example.com/photo.jpg",
  "alternative_mode": false,
  "alternative_name": null
}
```

**Error Responses**:
- `401`: Unauthorized (invalid/missing token)

---

### Update Profile
Mettre à jour le profil de l'utilisateur.

**Endpoint**: `PUT /api/profile`

**Headers**: 
```
Authorization: Bearer {token}
```

**Request Body**:
```json
{
  "name": "John Smith",
  "bio": "Updated bio",
  "photo_url": "https://example.com/new-photo.jpg",
  "alternative_mode": true,
  "alternative_name": "Mystery User"
}
```

**Response** (200 OK):
```json
{
  "message": "Profile updated successfully"
}
```

**Error Responses**:
- `401`: Unauthorized
- `403`: Alternative mode requires premium/platinum subscription

---

## Rooms (Events)

### List Accessible Rooms
Lister tous les événements accessibles selon les critères de l'utilisateur.

**Endpoint**: `GET /api/rooms`

**Headers**: 
```
Authorization: Bearer {token}
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "Speed Dating 25-35 ans",
    "description": "Une soirée speed dating pour célibataires",
    "photo_url": null,
    "welcome_message": "Bienvenue ! Profitez de la soirée 🎉",
    "event_datetime": "2025-10-10T19:00:00",
    "max_capacity": 20,
    "member_count": 12,
    "is_active": true,
    "establishment_name": "Café de Paris"
  }
]
```

---

### Get Room Details
Obtenir les détails d'un événement spécifique.

**Endpoint**: `GET /api/rooms/{room_id}`

**Headers**: 
```
Authorization: Bearer {token}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "Speed Dating 25-35 ans",
  "description": "Une soirée speed dating pour célibataires",
  "welcome_message": "Bienvenue ! Profitez de la soirée 🎉",
  "event_datetime": "2025-10-10T19:00:00",
  "max_capacity": 20,
  "member_count": 12,
  "is_active": true,
  "establishment": {
    "name": "Café de Paris",
    "address": "123 Rue de Rivoli, 75001 Paris"
  }
}
```

**Error Responses**:
- `403`: Access denied (age/gender/orientation restrictions)
- `404`: Room not found

---

### Join Room
Rejoindre un événement.

**Endpoint**: `POST /api/rooms/{room_id}/join`

**Headers**: 
```
Authorization: Bearer {token}
```

**Response** (200 OK):
```json
{
  "message": "Joined room successfully"
}
```

**Error Responses**:
- `400`: Already a member
- `400`: Room is full
- `403`: Access denied
- `404`: Room not found

---

### Join Room by Access Code
Rejoindre un événement en utilisant un code d'accès.

**Endpoint**: `POST /api/rooms/join-by-code`

**Headers**: 
```
Authorization: Bearer {token}
```

**Request Body**:
```json
{
  "access_code": "A3B7K9M2"
}
```

**Response** (200 OK):
```json
{
  "message": "Joined room successfully",
  "room_id": 1
}
```

**Error Responses**:
- `400`: Access code required
- `400`: Already a member
- `400`: Room is full
- `403`: Access denied
- `404`: Room not found with this code

---

### Get My Rooms
Récupérer la liste des événements rejoints par l'utilisateur.

**Endpoint**: `GET /api/rooms/my`

**Headers**: 
```
Authorization: Bearer {token}
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "Speed Dating 25-35 ans",
    "description": "Une soirée speed dating pour célibataires",
    "event_datetime": "2025-10-10T19:00:00",
    "max_capacity": 20,
    "member_count": 12,
    "is_active": true,
    "establishment_name": "Café de Paris",
    "created_at": "2025-10-01T10:00:00"
  }
]
```

---

## Messages

### Get Room Messages
Récupérer tous les messages d'un événement.

**Endpoint**: `GET /api/rooms/{room_id}/messages`

**Headers**: 
```
Authorization: Bearer {token}
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_name": "John Doe",
    "content": "Salut tout le monde !",
    "is_announcement": false,
    "created_at": "2025-10-06T12:00:00"
  }
]
```

**Error Responses**:
- `403`: Must join room first

---

### Send Message
Envoyer un message dans un événement.

**Endpoint**: `POST /api/rooms/{room_id}/messages`

**Headers**: 
```
Authorization: Bearer {token}
```

**Request Body**:
```json
{
  "content": "Salut tout le monde ! J'ai hâte de vous rencontrer !"
}
```

**Response** (200 OK):
```json
{
  "message": "Message sent successfully"
}
```

**Error Responses**:
- `403`: Must join room first

---

## Establishments

### Create Establishment
Créer un nouvel établissement (rôle establishment requis).

**Endpoint**: `POST /api/establishments`

**Headers**: 
```
Authorization: Bearer {token}
```

**Request Body**:
```json
{
  "name": "Café de Paris",
  "description": "Un café chaleureux au cœur de Paris",
  "address": "123 Rue de Rivoli, 75001 Paris"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "message": "Establishment created successfully"
}
```

**Error Responses**:
- `400`: Establishment already exists
- `403`: Unauthorized (not establishment role)

---

### Get My Establishment
Récupérer les informations de mon établissement.

**Endpoint**: `GET /api/establishments/me`

**Headers**: 
```
Authorization: Bearer {token}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "Café de Paris",
  "description": "Un café chaleureux au cœur de Paris",
  "address": "123 Rue de Rivoli, 75001 Paris",
  "subscription_plan": "silver",
  "subscription_price": 49.0,
  "rooms_created_today": 0,
  "last_room_reset": "2025-10-06"
}
```

**Error Responses**:
- `403`: Unauthorized

---

### Create Room
Créer un nouvel événement dans un établissement.

**Endpoint**: `POST /api/establishments/{establishment_id}/rooms`

**Headers**: 
```
Authorization: Bearer {token}
```

**Request Body**:
```json
{
  "name": "Speed Dating 25-35 ans",
  "description": "Une soirée speed dating pour célibataires",
  "welcome_message": "Bienvenue ! Profitez de la soirée 🎉",
  "event_datetime": "2025-10-10T19:00:00",
  "max_capacity": 20,
  "access_gender": null,
  "access_orientation": null,
  "access_age_min": 25,
  "access_age_max": 35
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "access_code": "A3B7K9M2",
  "message": "Room created successfully"
}
```

**Error Responses**:
- `400`: Daily room limit reached
- `403`: Unauthorized

---

### Get Room Details (Establishment)
Obtenir les détails complets d'un événement avec statistiques et liste des participants.

**Endpoint**: `GET /api/establishments/me/rooms/{room_id}`

**Headers**: 
```
Authorization: Bearer {token}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "Speed Dating 25-35 ans",
  "description": "Une soirée speed dating pour célibataires",
  "welcome_message": "Bienvenue ! Profitez de la soirée 🎉",
  "is_active": true,
  "created_at": "2025-10-01T10:00:00",
  "event_datetime": "2025-10-10T19:00:00",
  "max_capacity": 20,
  "member_count": 12,
  "access_code": "A3B7K9M2",
  "access_gender": null,
  "access_orientation": null,
  "access_age_min": 25,
  "access_age_max": 35,
  "members": [
    {
      "name": "John Doe",
      "joined_at": "2025-10-05T14:30:00"
    }
  ]
}
```

**Error Responses**:
- `403`: Unauthorized
- `404`: Room not found or not owned by establishment

---

### Get Establishment Analytics
Obtenir les statistiques de l'établissement.

**Endpoint**: `GET /api/establishments/me/analytics`

**Headers**: 
```
Authorization: Bearer {token}
```

**Response** (200 OK):
```json
{
  "total_rooms": 15,
  "active_rooms": 3,
  "total_members": 127,
  "rooms_today": 1,
  "max_rooms_today": 1
}
```

---

### Get Establishment Rooms
Lister tous les événements d'un établissement.

**Endpoint**: `GET /api/establishments/me/rooms?status={active|inactive}`

**Headers**: 
```
Authorization: Bearer {token}
```

**Query Parameters**:
- `status` (optional): `active` ou `inactive`

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "Speed Dating 25-35 ans",
    "description": "Une soirée speed dating pour célibataires",
    "is_active": true,
    "created_at": "2025-10-01T10:00:00",
    "event_datetime": "2025-10-10T19:00:00",
    "max_capacity": 20,
    "member_count": 12,
    "access_gender": null,
    "access_age_min": 25,
    "access_age_max": 35,
    "access_code": "A3B7K9M2"
  }
]
```

---

## Admin

### List All Users
Lister tous les utilisateurs (admin uniquement).

**Endpoint**: `GET /api/admin/users`

**Headers**: 
```
Authorization: Bearer {token}
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "user@example.com",
    "role": "user",
    "subscription_tier": "premium",
    "created_at": "2025-09-01T10:00:00"
  }
]
```

**Error Responses**:
- `403`: Unauthorized (not admin)

---

### List Reports
Lister tous les signalements (admin uniquement).

**Endpoint**: `GET /api/admin/reports`

**Headers**: 
```
Authorization: Bearer {token}
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "reporter_name": "John Doe",
    "reported_user_name": "Jane Smith",
    "room_name": "Speed Dating",
    "reason": "Comportement inapproprié",
    "status": "pending",
    "created_at": "2025-10-05T14:00:00"
  }
]
```

**Error Responses**:
- `403`: Unauthorized (not admin)

---

## Reports

### Submit Report
Signaler un utilisateur ou un événement.

**Endpoint**: `POST /api/reports`

**Headers**: 
```
Authorization: Bearer {token}
```

**Request Body**:
```json
{
  "reported_user_id": 5,
  "room_id": 1,
  "reason": "Comportement inapproprié durant l'événement"
}
```

**Response** (201 Created):
```json
{
  "message": "Report submitted successfully"
}
```

---

## Security & Encryption

### Data Encryption
Toutes les données sensibles sont chiffrées au repos dans la base de données :

**Données chiffrées**:
- `users.email` - Email utilisateur (chiffré avec AES-256)
- `users.name` - Nom utilisateur (chiffré)
- `users.bio` - Biographie (chiffrée)
- `users.photo_url` - URL photo (chiffrée)
- `users.alternative_name` - Nom alternatif (chiffré)
- `messages.content` - Contenu des messages (chiffré)

**Données non chiffrées**:
- IDs et clés étrangères
- Dates et timestamps
- Énumérations (role, subscription_tier, gender, etc.)
- Méta-données non sensibles

Le chiffrement est transparent pour l'application grâce à l'utilisation de SQLAlchemy TypeDecorators.

### Token Management
- Les tokens JWT expirent après 7 jours
- Les tokens sont signés avec une clé secrète stockée dans les variables d'environnement
- Chaque requête API authentifiée doit inclure le token dans le header `Authorization: Bearer {token}`

---

## Error Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 201  | Created |
| 400  | Bad Request (invalid data) |
| 401  | Unauthorized (invalid/missing token) |
| 403  | Forbidden (insufficient permissions) |
| 404  | Not Found |
| 500  | Internal Server Error |

---

## Rate Limiting
Actuellement, aucune limitation de débit n'est implémentée en développement.
En production, il est recommandé d'implémenter un rate limiting pour protéger l'API.

---

## Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Security
SECRET_KEY=your-secret-key-for-jwt
ENCRYPTION_KEY=your-fernet-encryption-key

# Flask
FLASK_ENV=development  # or production
```

---

## Getting Started

1. Inscrivez-vous avec `POST /api/auth/register`
2. Connectez-vous avec `POST /api/auth/login` pour obtenir un token
3. Utilisez le token dans tous les headers `Authorization: Bearer {token}`
4. Explorez les événements avec `GET /api/rooms`
5. Rejoignez un événement avec `POST /api/rooms/{id}/join` ou `POST /api/rooms/join-by-code`
6. Envoyez des messages avec `POST /api/rooms/{id}/messages`

---

**Version**: 1.0.0  
**Last Updated**: October 6, 2025
