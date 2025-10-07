# MeetSpot - PWA Dating Platform

## Overview
MeetSpot is a Progressive Web Application (PWA) dating platform designed to facilitate real-life meetings at physical venues. Inspired by the clean interfaces of Bumble and Hinge, its core purpose is to connect users for events rather than endless swiping. The platform supports multiple user roles: Admin for platform management, Establishment for venue owners to create events, and Users for members to join rooms and connect. It aims to offer a modern, mobile-first experience with a focus on privacy, security, and user-friendly interaction.

## User Preferences
- Focus on real-life meetings over endless swiping
- Clean, modern UI inspired by Bumble/Hinge
- Mobile-first design with Tailwind CSS (no desktop version)
- Max viewport width: 768px (mobile and tablet only)
- Vibrant coral and purple color scheme
- Bottom navigation bars for all dashboards
- Bottom sheet modals for mobile interactions

## System Architecture

### UI/UX Decisions
The platform features a mobile-first responsive design, limited to a maximum viewport width of 768px. It uses a distinct color palette: Primary #FF4458 (vibrant coral), Secondary #6C5CE7 (soft purple), Accent #A29BFE (lavender), Background #F5F5F5 (light grey), and Text #2D3436 (charcoal). Typography is set with Poppins for headings and Inter for body text. Navigation is managed through fixed bottom navigation bars with SVG icons and bottom sheet modals for mobile-optimized interactions across all dashboards (User, Establishment, Admin).

### Technical Implementations
MeetSpot is built as a PWA with a Python Flask backend and a Tailwind CSS frontend. It utilizes a modular backend structure with PostgreSQL via SQLAlchemy ORM. Authentication is handled with JWT (stored in localStorage) and bcrypt for password hashing. All sensitive data, including personal information and private messages, is encrypted at rest using AES-256 (Fernet) with SQLAlchemy TypeDecorators. The frontend uses Vanilla JavaScript for interactivity, supporting full PWA features like service workers for offline support, app manifests for installability, and push notification readiness. An auto-refresh system provides real-time data synchronization for conversations, requests, and room activities, intelligently pausing when the app loses focus.

**CORS Configuration**: Flask-CORS configured with `supports_credentials=False` and wildcard origins to support cross-origin API requests. JWT tokens are stored in localStorage (not cookies), enabling stateless authentication across deployments.

**Request Validation**: All API endpoints validate request data before processing, ensuring `request.json` is not None and all required fields are present, preventing connection errors during login/registration.

### Feature Specifications
- **User Roles & Access Control**: Admin, Establishment, and User roles with role-based access control. Room access can be filtered by gender, orientation, and age.
- **Rooms System**: Event-based meeting spaces at physical venues with 24-hour expiration. Rooms are joined via unique 8-character access codes or QR code scanning.
- **Connection & Communication**: Replaces group chat with a system of connection requests between users. Upon acceptance, private 1-to-1 encrypted conversations are established. Private messages support text, emojis (16-emoji picker), and photo uploads with explicit consent confirmation.
- **Conversation Expiration System**: Conversations automatically expire based on subscription tier (Free: 24h, Premium: 7 days, Platinum: 30 days). Expiration calculated from best tier between both users. UI displays real-time countdown (days/hours/minutes). Server-side enforcement on all conversation endpoints (send_message, get_messages, get_conversation, send_photo) prevents messaging in expired threads. Conversations are unique per (room_id, user1, user2), allowing same users to have multiple conversations in different rooms. Active/expired filter in messages UI.
- **User Blocking System**: Users can block others via UserBlock model with unique constraint. Blocked users are completely invisible across all rooms in get_participants(). Bidirectional filtering ensures both blocker and blocked users never see each other.
- **Subscription Tiers**: Multiple tiers for Users (Free, Premium, Platinum) offering features like priority access, alternative identity mode (hiding photos/pseudonyms), and unlimited messaging. Establishments also have subscription plans for creating rooms and accessing analytics.
- **Profile Management**: Enriched user profiles include auto-generated usernames, birthdate (for dynamic age calculation), sexual orientation, multi-select meeting types, interests, and photo galleries. Admin-customizable profile options (gender, meeting type, interest) are managed via a dedicated dashboard.
- **Reporting & Moderation**: A system for users to report inappropriate content or behavior, with admin oversight.
- **Backup & Deployment System**: Comprehensive admin-managed system for automated backups (database, uploaded files, configuration), secure restoration with path validation, database migrations with auto-detection of schema changes, and GitHub-based updates with pre-update backups. Backups use PostgreSQL custom format and are compressed to .tar.gz with automatic rotation (keeps last 10).

### System Design Choices
The backend organizes routes by resource (auth, rooms, establishments, admin, profile, connection_requests, conversations) and uses a centralized configuration. Database schema includes Users (with detailed demographics and subscription info), Establishments, Rooms (with access rules and expiration), RoomMembers, ConnectionRequest, PrivateConversation (with expires_at, started_at, room_id NOT NULL, unique constraint on room_id+user1_id+user2_id), PrivateMessage (with photo_url support), UserBlock (with unique constraint on blocker_id+blocked_id), Reports, and SubscriptionPlans. A `ProfileOption` model allows admins to define and manage selectable options for user profiles dynamically.

**Deployment & Backup Infrastructure**:
- `scripts/backup.py`: Creates comprehensive backups (PostgreSQL dump in custom format, uploads folder, .env, requirements.txt, .encryption_key)
- `scripts/restore.py`: Secure restoration with tar extraction validation, path traversal protection, and pg_restore error enforcement
- `scripts/migrate_database.py`: Automatic database migration with schema introspection, detects missing tables/columns and applies changes safely
- `scripts/update_from_github.py`: GitHub-based updates with automatic pre-update backups, git pull, database migration, and server restart
- Admin API endpoints (`/api/admin/backup/*`) for managing backups, checking updates, applying updates, and running migrations with proper authentication and timeout handling

## External Dependencies
- **PostgreSQL**: Primary database for all application data.
- **Tailwind CSS**: Utility-first CSS framework for styling the frontend.
- **QRious library (v4.0.2)**: Used for generating QR codes for establishment events.
- **Python Flask**: Web framework for the backend.
- **SQLAlchemy**: Python SQL toolkit and Object-Relational Mapper.
- **PyJWT**: Python library for JSON Web Token (JWT) authentication.
- **Bcrypt**: For password hashing.
- **Cryptography (Fernet/AES-256)**: For encryption of sensitive data at rest.
- **Flask-CORS**: Cross-Origin Resource Sharing support for API endpoints.
- **Gunicorn**: Production WSGI server for Python applications.

## Deployment Documentation
- **DEPLOYMENT.md**: Comprehensive deployment guide for PythonAnywhere and Railway with step-by-step instructions
- **.env.example**: Template for environment variables (DATABASE_URL, SECRET_KEY, ENCRYPTION_KEY, FLASK_ENV)
- **passenger_wsgi.py**: PythonAnywhere-specific WSGI configuration
- **wsgi.py**: Standard WSGI entry point for production deployments

## Recent Changes (October 2025)
- **UI Color Scheme Update** (October 7):
  - Changed background color from #FFEAA7 (warm cream) to #F5F5F5 (light grey)
  - Updated all HTML pages (index.html, app.html, admin.html, establishment.html)
  - Updated manifest.json theme_color to match new background
  - Maintains coral (#FF4458), purple (#6C5CE7), and lavender (#A29BFE) accents
- **Conversation Expiration & Countdown System** (October 7):
  - Added `expires_at` and `started_at` fields to PrivateConversation model
  - Implemented tier-based expiration: Free=24h, Premium=7d, Platinum=30d
  - Added `check_and_expire()` method enforced on all conversation endpoints
  - Built UI countdown timer showing days/hours/minutes remaining
  - Added active/expired filter in messages interface with query param support
  - Unique constraint on (room_id, user1_id, user2_id) for room-specific conversations
  - Server-side validation prevents messaging/reading in expired conversations (400 error)
- **User Blocking System** (October 7):
  - Created UserBlock model with unique(blocker_id, blocked_id) constraint
  - Integrated bidirectional filtering in get_participants() endpoint
  - Blocked users completely invisible across all rooms
- Fixed deployment login issues by correcting CORS configuration (supports_credentials=False with wildcard origins)
- Added request validation in auth endpoints to prevent None errors
- Created comprehensive deployment documentation for PythonAnywhere and Railway
- Added .env.example template with all required environment variables
- Improved error handling and validation across authentication routes