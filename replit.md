# MeetSpot - PWA Dating Platform

## Overview
A progressive web application (PWA) dating platform focused on real-life meetings at physical venues. Inspired by Bumble and Hinge's clean interfaces, built with Python Flask backend and Tailwind CSS frontend.

## Features Implemented

### User Roles
- **Admin**: Platform management, user moderation, subscription plans, reporting
- **Establishment**: Venue owners who create rooms/events with subscription limits
- **User**: Members who join rooms and attend events

### Core Features
- **Rooms System**: Event-based meeting spaces at physical venues
- **Access Control**: Gender, orientation, and age-based filtering
- **Subscription Tiers**:
  - Free: Browse events, join public rooms
  - Premium ($19/mo): Priority access, alternative identity mode
  - Platinum ($39/mo): VIP access, unlimited messaging
- **Establishment Plans**:
  - One-Shot ($9): 1 room per day
  - Silver ($49): 1 room per day + advanced analytics
  - Gold ($99): 3 rooms per day + premium features
- **Alternative Identity Mode**: Premium/Platinum users can hide photos and change pseudonyms
- **Messaging**: Room-based chat for event coordination
- **Reporting & Moderation**: User reports with admin oversight

### PWA Features
- Service worker for offline support
- App manifest for installability
- Mobile-first responsive design
- Push notification ready

## Architecture

### Backend (Flask)
- Structure modulaire avec package `backend/`
- `backend/config.py`: Configuration centralisée (dev/prod)
- `backend/routes/`: Blueprints séparés par ressource (auth, rooms, establishments, admin, profile)
- `backend/models/`: Modèles SQLAlchemy (User, Room, Message, etc.)
- `backend/utils/`: Utilitaires (auth, encryption, room_access)
- PostgreSQL database avec SQLAlchemy ORM
- JWT authentication
- bcrypt password hashing
- **Chiffrement AES-256**: Toutes les données sensibles sont chiffrées au repos
- Role-based access control

### Frontend
- `index.html`: Landing page with auth modals
- `app.html`: User dashboard with room browsing
- `establishment.html`: Venue management dashboard
- `admin.html`: Platform administration
- Tailwind CSS for styling
- Vanilla JavaScript for interactivity

### Database Schema
- Users (with role, subscription, demographics)
- Establishments (venues with subscription plans)
- Rooms (events with access rules + unique access_code)
- RoomMembers (join tracking)
- Messages (room-based chat)
- Reports (moderation system)
- SubscriptionPlans (pricing tiers)

## Design System

### Colors
- Primary: #FF4458 (vibrant coral)
- Secondary: #6C5CE7 (soft purple)
- Accent: #A29BFE (lavender)
- Background: #FFEAA7 (warm cream)
- Text: #2D3436 (charcoal)
- Success: #00B894 (mint green)

### Typography
- Headings: Poppins (600, 700)
- Body: Inter (300-700)

## Setup Instructions

### First Time Setup
1. The database is automatically initialized on first request
2. Create an admin account through the registration form, then manually update the role in the database or use the Python console
3. Establishments can register and create their venue
4. Users can browse and join rooms

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection (auto-configured)
- `SECRET_KEY`: JWT signing key (auto-generated for dev)
- `ENCRYPTION_KEY`: Clé de chiffrement Fernet pour les données sensibles (auto-générée au premier lancement)
- `FLASK_ENV`: Environment (development/production)

## API Endpoints

### Authentication
- POST `/api/auth/register`: Create new account
- POST `/api/auth/login`: Login and get JWT token

### Profile
- GET `/api/profile`: Get current user profile
- PUT `/api/profile`: Update profile (alternative mode for Premium+)

### Rooms
- GET `/api/rooms`: List accessible rooms
- GET `/api/rooms/<id>`: Get room details
- POST `/api/rooms/<id>/join`: Join a room
- POST `/api/rooms/join-by-code`: Join room via access code
- GET `/api/rooms/my`: Get user's joined rooms
- GET `/api/rooms/<id>/messages`: Get room messages
- POST `/api/rooms/<id>/messages`: Send message

### Establishments
- POST `/api/establishments`: Create venue (establishment role)
- POST `/api/establishments/<id>/rooms`: Create event (respects daily limits, auto-generates access code)
- GET `/api/establishments/me/rooms/<id>`: Get detailed room stats, members, and access code

### Admin
- GET `/api/admin/users`: List all users
- GET `/api/admin/reports`: View moderation reports

### Reporting
- POST `/api/reports`: Submit user/room report

## Recent Changes
- 2025-10-06: Security & Architecture improvements
  - **Chiffrement des données**: Toutes les données sensibles sont maintenant chiffrées au repos
    - Emails, noms, bios, photos, noms alternatifs des utilisateurs
    - Contenu des messages de chat
    - Utilisation de Fernet (AES-256) avec SQLAlchemy TypeDecorators
  - **Structure du code**: Refactorisation complète en modules
    - Configuration centralisée dans `backend/config.py`
    - Routes organisées par ressource dans `backend/routes/`
    - Utilitaires de chiffrement dans `backend/utils/encryption.py`
  - **Documentation API**: Documentation complète dans `API_DOCUMENTATION.md`
    - Tous les endpoints documentés avec exemples
    - Codes d'erreur et authentification expliqués
    - Section dédiée à la sécurité et au chiffrement
- 2025-10-06: Complete user experience redesign
  - **Access code system**: 8-character codes for easy event joining
  - **QR code scanner**: Users can scan QR codes with camera to join events
  - **New home screen**: Code entry field + QR scan button + past events list
  - **Chat tab**: Separate tab for active/expired chats with filtering
  - **3-tab navigation**: Home, Chat, Profile (was 2 tabs before)
  - **Establishment features**:
    - Access codes visible on room cards
    - QR code generation using QRious library (v4.0.2)
    - Room details modal with stats and member list
  - **New API endpoints**:
    - POST `/api/rooms/join-by-code`: Join room via access code
    - GET `/api/rooms/my`: Get user's joined rooms
    - GET `/api/establishments/me/rooms/<id>`: Room details for establishments
- 2025-10-04: Complete mobile-first redesign with bottom navigation bars
  - User dashboard: 2 tabs (Discover, Profile) with bottom sheet modals
  - Establishment dashboard: 3 tabs (Dashboard, Analytics, Profile) with event creation modal
  - Admin dashboard: 3 tabs (Dashboard, Users, Reports) with gradient stat cards
  - All pages limited to 768px width (mobile/tablet only, no desktop version)
  - Fixed bottom navigation bars with active states and SVG icons
  - Bottom sheet modals for better mobile UX
- 2025-10-04: Initial platform build with complete feature set
- All core features from requirements document implemented
- PWA manifest and service worker configured
- Role-based dashboards for admin, establishment, and users
- Room access control with demographic filtering
- Subscription plan enforcement for establishments
- Fixed: Establishment users with existing accounts now go directly to dashboard

## User Preferences
- Focus on real-life meetings over endless swiping
- Clean, modern UI inspired by Bumble/Hinge
- Mobile-first design with Tailwind CSS (no desktop version)
- Max viewport width: 768px (mobile and tablet only)
- Vibrant coral and purple color scheme
- Bottom navigation bars for all dashboards
- Bottom sheet modals for mobile interactions
