# MeetSpot API Documentation

🇬🇧 English Version | [🇫🇷 Version Française](./API_DOCS_FR.md)

## Overview

**Base URL** : `https://your-domain.com/api`  
**Authentication** : JWT Bearer Token  
**Content-Type** : `application/json`

## Table of Contents

1. [Authentication](#authentication)
2. [User Profile](#user-profile)
3. [Events (Rooms)](#events-rooms)
4. [Connection Requests](#connection-requests)
5. [Private Conversations](#private-conversations)
6. [Establishments](#establishments)
7. [Administration](#administration)
8. [Error Codes](#error-codes)

---

## Authentication

### Registration
Create a new user account.

```http
POST /api/auth/register
```

**Request Body** :
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe",
  "role": "user",
  "gender": "male",
  "orientation": "straight",
  "age": 28
}
```

**Response (201)** :
```json
{
  "message": "User created successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Login
Obtain a JWT token.

```http
POST /api/auth/login
```

**Request Body** :
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200)** :
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user"
  }
}
```

---

## User Profile

### Get Profile
```http
GET /api/profile
Authorization: Bearer {token}
```

**Response (200)** :
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "age": 28,
  "gender": "male",
  "orientation": "straight",
  "bio": "My bio",
  "subscription_tier": "free",
  "alternative_mode": false
}
```

### Update Profile
```http
PUT /api/profile
Authorization: Bearer {token}
```

**Request Body** :
```json
{
  "name": "John Doe",
  "bio": "New bio",
  "photo_url": "https://example.com/photo.jpg",
  "alternative_mode": false,
  "alternative_name": "Alternative name"
}
```

---

## Events (Rooms)

### List Events
```http
GET /api/rooms
Authorization: Bearer {token}
```

**Response (200)** :
```json
[
  {
    "id": 1,
    "name": "Jazz Night",
    "description": "Musical evening",
    "establishment_name": "The Wine Bar",
    "event_datetime": "2025-10-15T20:00:00",
    "member_count": 15,
    "is_active": true,
    "created_at": "2025-10-14T12:00:00",
    "expires_at": "2025-10-15T12:00:00"
  }
]
```

### Join by Access Code
```http
POST /api/rooms/join-by-code
Authorization: Bearer {token}
```

**Request Body** :
```json
{
  "access_code": "ABC12345"
}
```

**Response (200)** :
```json
{
  "message": "Joined room successfully",
  "room_id": 1
}
```

### My Events
```http
GET /api/rooms/my
Authorization: Bearer {token}
```

Returns all events the user has joined.

### View Participants
```http
GET /api/rooms/{room_id}/participants
Authorization: Bearer {token}
```

**Response (200)** :
```json
[
  {
    "id": 2,
    "name": "Marie",
    "age": 25,
    "gender": "female",
    "bio": "Music lover",
    "photo_url": "https://...",
    "joined_at": "2025-10-14T19:30:00"
  }
]
```

### Leave an Event
```http
POST /api/rooms/{room_id}/leave
Authorization: Bearer {token}
```

---

## Connection Requests

### List Requests
```http
GET /api/requests?type=received
Authorization: Bearer {token}
```

**Parameters** :
- `type` : `received` or `sent`

**Response (200)** :
```json
[
  {
    "id": 1,
    "requester_id": 2,
    "requester_name": "Marie",
    "target_id": 1,
    "room_id": 1,
    "room_name": "Jazz Night",
    "status": "pending",
    "created_at": "2025-10-14T20:15:00"
  }
]
```

### Send a Request
```http
POST /api/requests
Authorization: Bearer {token}
```

**Request Body** :
```json
{
  "room_id": 1,
  "target_id": 2
}
```

**Response (201)** :
```json
{
  "message": "Request sent successfully",
  "id": 1
}
```

### Accept a Request
```http
POST /api/requests/{request_id}/accept
Authorization: Bearer {token}
```

**Response (200)** :
```json
{
  "message": "Request accepted",
  "conversation_id": 1
}
```

### Reject a Request
```http
POST /api/requests/{request_id}/reject
Authorization: Bearer {token}
```

---

## Private Conversations

### List Conversations
```http
GET /api/conversations
Authorization: Bearer {token}
```

**Response (200)** :
```json
[
  {
    "id": 1,
    "user1_id": 1,
    "user2_id": 2,
    "user1_name": "John",
    "user2_name": "Marie",
    "room_id": 1,
    "room_name": "Jazz Night",
    "created_at": "2025-10-14T20:30:00"
  }
]
```

### Conversation Messages
```http
GET /api/conversations/{conversation_id}/messages
Authorization: Bearer {token}
```

**Response (200)** :
```json
[
  {
    "id": 1,
    "sender_id": 1,
    "content": "Hi! Nice to meet you",
    "created_at": "2025-10-14T20:35:00"
  }
]
```

### Send a Message
```http
POST /api/conversations/{conversation_id}/messages
Authorization: Bearer {token}
```

**Request Body** :
```json
{
  "content": "Reply message"
}
```

---

## Establishments

### Create an Establishment
```http
POST /api/establishments
Authorization: Bearer {token}
```

**Request Body** :
```json
{
  "name": "The Wine Bar",
  "description": "Cozy bar downtown",
  "address": "123 Main Street",
  "subscription_plan": "one-shot"
}
```

### Create an Event
```http
POST /api/establishments/{establishment_id}/rooms
Authorization: Bearer {token}
```

**Request Body** :
```json
{
  "name": "Jazz Night",
  "description": "Live concert",
  "event_datetime": "2025-10-15T20:00:00",
  "welcome_message": "Welcome!",
  "access_gender": "all",
  "access_orientation": "all",
  "access_age_min": 18,
  "access_age_max": 65,
  "max_capacity": 50
}
```

**Response (200)** :
```json
{
  "id": 1,
  "access_code": "ABC12345",
  "message": "Room created successfully"
}
```

### Event Details (establishment)
```http
GET /api/establishments/me/rooms/{room_id}
Authorization: Bearer {token}
```

Returns complete details including access code, member list and statistics.

---

## Administration

### List Users
```http
GET /api/admin/users
Authorization: Bearer {token}
```

Required role: `admin`

### List Reports
```http
GET /api/admin/reports
Authorization: Bearer {token}
```

Required role: `admin`

### Report a User or Event
```http
POST /api/reports
Authorization: Bearer {token}
```

**Request Body** :
```json
{
  "target_type": "user",
  "target_id": 2,
  "reason": "Inappropriate behavior",
  "description": "Detailed description"
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created successfully |
| 400 | Invalid request |
| 401 | Unauthenticated |
| 403 | Unauthorized |
| 404 | Resource not found |
| 500 | Server error |

### Typical Error Response
```json
{
  "message": "Error description"
}
```

---

## Security

### Encryption
All sensitive data is encrypted with AES-256:
- Emails and personal information
- Private messages
- Alternative names

### Authentication
- JWT tokens with expiration
- Passwords hashed with bcrypt
- HTTPS mandatory in production

---

## Important Notes

1. **Event Expiration** : All events automatically expire 24 hours after creation
2. **Active Members** : Users are automatically marked as inactive when the event expires
3. **Persistent Conversations** : Private conversations remain active even after event expiration
4. **Rate Limiting** : Respect rate limits to avoid blocking

---

**Complete Documentation** : See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for more details.
