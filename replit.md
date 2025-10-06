# MeetSpot - PWA Dating Platform

## Overview
A progressive web application (PWA) dating platform focused on real-life meetings at physical venues. Inspired by Bumble and Hinge's clean interfaces, built with Python Flask backend and Tailwind CSS frontend.

## Features Implemented

### User Roles
- **Admin**: Platform management, user moderation, subscription plans, reporting
- **Establishment**: Venue owners who create rooms/events with subscription limits
- **User**: Members who join rooms and attend events

### Core Features
- **Rooms System**: Event-based meeting spaces at physical venues with 24-hour expiration
- **Access Control**: Gender, orientation, and age-based filtering
- **Connection Requests**: Users send connection requests to other participants (no group chat)
- **Private Conversations**: 1-to-1 encrypted messaging after connection acceptance
- **Subscription Tiers**:
  - Free: Browse events, join public rooms
  - Premium ($19/mo): Priority access, alternative identity mode
  - Platinum ($39/mo): VIP access, unlimited messaging
- **Establishment Plans**:
  - One-Shot ($9): 1 room per day
  - Silver ($49): 1 room per day + advanced analytics
  - Gold ($99): 3 rooms per day + premium features
- **Alternative Identity Mode**: Premium/Platinum users can hide photos and change pseudonyms
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
- `backend/routes/`: Blueprints séparés par ressource (auth, rooms, establishments, admin, profile, connection_requests, conversations)
- `backend/models/`: Modèles SQLAlchemy (User, Room, ConnectionRequest, PrivateConversation, PrivateMessage, etc.)
- `backend/utils/`: Utilitaires (auth, encryption, room_access)
- PostgreSQL database avec SQLAlchemy ORM
- JWT authentication
- bcrypt password hashing
- **Chiffrement AES-256**: Toutes les données sensibles sont chiffrées au repos
- Role-based access control
- Automatic room expiration (24 hours from creation)

### Frontend
- `index.html`: Landing page with auth modals
- `app.html`: User dashboard with room browsing
- `establishment.html`: Venue management dashboard
- `admin.html`: Platform administration
- Tailwind CSS for styling
- Vanilla JavaScript for interactivity

### Database Schema
- **Users** (with role, subscription, demographics)
  - `username`: Auto-generated unique identifier (name_random4digits)
  - `birthdate`: Date of birth (age calculated dynamically)
  - `sexual_orientation`: User's sexual orientation
  - `meeting_types`: JSON array of selected meeting types
  - `interests`: JSON array of selected interests
  - `gallery_photos`: JSON array of photo URLs
- **ProfileOption**: Admin-customizable profile options
  - Categories: gender, meeting_type, interest
  - Each option has value (ID), label, and is_active flag
- Establishments (venues with subscription plans)
- Rooms (events with access rules + unique access_code + expires_at)
- RoomMembers (join tracking + active flag + left_at)
- ConnectionRequest (pending/accepted/rejected connection requests between users)
- PrivateConversation (1-to-1 conversations after connection acceptance)
- PrivateMessage (encrypted messages in private conversations)
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
- `ENCRYPTION_KEY`: **IMPORTANT** Encryption key for sensitive data
  - **Development**: Auto-generated and saved to `.encryption_key` file
  - **Production**: **MUST** be set as environment variable for multi-process deployments
  - Losing this key means all encrypted data becomes unrecoverable
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

### Profile Options (Admin)
- GET `/api/profile-options`: Get all active profile options (authenticated)
- POST `/api/profile-options`: Create new profile option (admin only)
- PUT `/api/profile-options/<id>`: Update profile option (admin only)
- DELETE `/api/profile-options/<id>`: Deactivate profile option (admin only)

## Recent Changes
- 2025-10-06: Système d'emojis pour types de rencontre + QR code amélioré
  - **Emojis des types de rencontre**: Affichés à côté du nom des utilisateurs
    - Chaque type de rencontre (💑 soulmate, 👥 friends, 🍹 drink, ✈️ travel, 💼 networking, 💝 dating, 💬 juste discuté, 🎈 rien de sérieux) a son emoji
    - Les emojis apparaissent automatiquement dans la liste des participants
    - ProfileOption.emoji: Nouveau champ pour stocker l'emoji de chaque option
  - **Nouveaux types de rencontre**:
    - "💬 Juste discuté": Pour ceux qui veulent simplement échanger
    - "🎈 Rien de sérieux": Pour les rencontres sans engagement
  - **QR Code amélioré (Établissements)**:
    - QR code centré dans le bloc blanc
    - Bouton de téléchargement avec image PNG complète (nom de l'événement + QR + code d'accès)
    - Fonction downloadQRCode(): Génère une image composite avec Canvas
  - **Modification du nom de room**:
    - Bouton "Modifier" à côté du nom de la room
    - PUT `/api/establishments/rooms/<id>/update-name`: Endpoint pour modifier le nom
    - Le code d'accès reste inchangé lors de la modification
  - **Améliorations UI**:
    - Emojis ajoutés partout (formulaire d'inscription, admin, navigation)
    - Labels traduits en français avec emojis
    - Interface plus ludique et visuelle
  - **API Endpoints**:
    - GET `/api/rooms/<id>/participants`: Maintenant inclut meeting_type_emojis
    - PUT `/api/establishments/rooms/<id>/update-name`: Modification du nom de room

## Recent Changes (suite)
- 2025-10-06: Enhanced Profile System with Admin-Customizable Options
  - **User Profiles Enriched**:
    - Auto-generated unique username (format: `firstname_1234`) with collision detection
    - Birthdate field replacing static age (age calculated dynamically from birthdate)
    - Sexual orientation field
    - Meeting types: Multi-select array (e.g., "Find soulmate", "Make friends", "Casual dating")
    - Interests: Multi-select array (15+ options: Music, Travel, Sports, Art, Tech, etc.)
    - Gallery photos: Array of photo URLs for multiple profile pictures
  - **ProfileOption Model**: Admin-customizable options system
    - Three categories: `gender`, `meeting_type`, `interest`
    - Each option has: value (unique ID), label (display name), is_active flag
    - Default options pre-populated on database initialization
  - **Enhanced Registration Form**:
    - Date of birth picker (18+ age requirement)
    - Multi-select checkboxes for meeting types and interests
    - Conditional fields: Only shown for "user" role, hidden for "establishment"
    - Client-side validation for required multi-select fields
  - **Admin Dashboard Upgrade**:
    - New "Options" tab (4-tab navigation: Stats, Users, Options, Reports)
    - Manage profile options with CRUD operations
    - Toggle active/inactive status for each option
    - Add new custom options dynamically
  - **API Endpoints**:
    - `/api/profile-options`: GET all options, POST new options (admin)
    - `/api/profile-options/<id>`: PUT update, DELETE deactivate (admin)
  - **Test Data**: Updated existing test profiles with complete demo data
    - sophie_paris: Heterosexual, seeking soulmate + drinks, interests in music/travel/food/cinema
    - thomas_lyon: Heterosexual, seeking friends + networking, interests in sports/tech/gaming/fitness
    - emma_demo: Bisexual, seeking dating + friends + travel, interests in art/photography/fashion/dancing/music
- 2025-10-06: PWA Complete Implementation with Auto-Refresh System
  - **PWA Installability**: Full Progressive Web App support
    - Service worker with offline support and intelligent caching
    - App manifest with icons, shortcuts, and theme colors
    - Install prompt for iOS and Android with custom UI
    - Apple Touch Icon support for iOS home screen
  - **Auto-Refresh System**: Real-time data synchronization
    - Conversations: Auto-refresh every 5 seconds when chat is open
    - Conversation list: Refresh every 10 seconds on Chat tab
    - Connection requests: Refresh every 15 seconds on Requests tab
    - Events list: Refresh every 30 seconds on Discover/Rooms tabs
    - Participants list: Refresh every 20 seconds when viewing room details
  - **Smart Refresh Management**:
    - Pauses when app loses focus (tab inactive)
    - Resumes when app regains focus
    - Automatically refreshes data when coming back online
    - Context-aware: Only refreshes data relevant to current page
  - **Service Worker Features**:
    - Network-first strategy for API calls with cache fallback
    - Cache-first strategy for static assets
    - Automatic cache cleanup and version management
    - Update notification banner when new version available
  - **User Experience**:
    - One-click update when new version detected
    - Smooth install prompt 5 seconds after page load
    - "Install later" option that respects user choice
    - Offline indicator and automatic reconnection
- 2025-10-06: Major architectural overhaul - Connection Request System
  - **NO MORE GROUP CHAT**: Replaced group chat with connection request + private conversation system
  - **24-hour room expiration**: All rooms expire 24 hours after creation
    - RoomMember.active flag to track active memberships
    - left_at timestamp for tracking when users leave
    - Automatic expiration check via Room.check_and_expire() method
  - **Connection Request Flow**:
    - Users see participant lists in rooms
    - Send connection requests to specific users (pending/accepted/rejected states)
    - Private 1-to-1 conversations created after acceptance
    - ConnectionRequest model tracks all requests and their states
  - **Private Conversations**:
    - PrivateConversation model links two users
    - PrivateMessage model for encrypted 1-to-1 messages
    - Conversations remain active even after room expires
  - **New API Endpoints**:
    - GET/POST `/api/requests` - List and create connection requests
    - POST `/api/requests/<id>/accept` - Accept request and create private conversation
    - POST `/api/requests/<id>/reject` - Reject connection request
    - GET `/api/conversations` - List user's private conversations
    - GET/POST `/api/conversations/<id>/messages` - Get and send private messages
    - POST `/api/rooms/<id>/leave` - Leave a room
    - GET `/api/rooms/<id>/participants` - View room participants
- 2025-10-06: Security & Architecture improvements
  - **Chiffrement des données**: Toutes les données sensibles sont maintenant chiffrées au repos
    - Emails, noms, bios, photos, noms alternatifs des utilisateurs
    - Contenu des messages de chat et des messages privés
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
