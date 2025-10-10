# MatchSpot - PWA Dating Platform

## Overview
MatchSpot is a Progressive Web Application (PWA) dating platform designed to facilitate real-life meetings at physical venues. Inspired by clean interfaces, its core purpose is to connect users for events rather than endless swiping. The platform supports multiple user roles: Admin for platform management, Establishment for venue owners to create events, and Users for members to join rooms and connect. It aims to offer a modern, mobile-first experience with a focus on privacy, security, and user-friendly interaction, ultimately fostering real-life connections.

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
MatchSpot is built as a PWA with a Python Flask backend and a Tailwind CSS frontend. It utilizes a modular backend structure with PostgreSQL via SQLAlchemy ORM. Authentication is handled with JWT (stored in localStorage) and bcrypt for password hashing. All sensitive data, including personal information and private messages, is encrypted at rest using AES-256 (Fernet) with SQLAlchemy TypeDecorators. The frontend uses Vanilla JavaScript for interactivity, supporting full PWA features like service workers for offline support, app manifests for installability, and push notification readiness. An auto-refresh system provides real-time data synchronization for conversations, requests, and room activities, intelligently pausing when the app loses focus. CORS is configured with `supports_credentials=False` and wildcard origins. All API endpoints validate request data.

### Feature Specifications
- **User Roles & Access Control**: Admin, Establishment, and User roles with role-based access control, including gender, orientation, and age filtering for room access.
- **Rooms System**: Event-based meeting spaces at physical venues with 24-hour expiration, joined via 8-character access codes or QR scanning.
- **Connection & Communication**: Replaces group chat with connection requests. Accepted requests establish private, encrypted 1-to-1 conversations with text, emojis, and photo uploads.
- **Conversation Expiration System**: Conversations expire based on subscription tier (24h, 7 days, 30 days), enforced server-side with UI countdowns. Conversations are unique per (room_id, user1, user2).
- **User Blocking System**: Users can block others, making blocked users completely invisible bidirectionally across the platform.
- **Subscription Tiers**: Multiple tiers for Users (Free, Premium, Platinum) and Establishments, offering features like priority access, alternative identity mode, and analytics.
- **Profile Management**: Enriched user profiles include auto-generated usernames, dynamic age calculation, sexual orientation, multi-select meeting types, interests, and photo galleries. Admin-customizable profile options.
- **Reporting & Moderation**: System for users to report inappropriate content with admin oversight.
- **User Verification**: Multi-step user verification process including photo upload and admin approval/rejection, with visual indicators for verification status.
- **Multi-step User Signup**: A 4-step registration process for users, including basic info, profile details, and photo uploads.
- **Backup & Deployment System**: Admin-managed system for automated backups (database, uploaded files, configuration), secure restoration, database migrations with auto-detection, and GitHub-based updates with pre-update backups.

### System Design Choices
The backend organizes routes by resource (auth, rooms, establishments, admin, profile, connection_requests, conversations) and uses a centralized configuration. Database schema includes Users, Establishments, Rooms, RoomMembers, ConnectionRequest, PrivateConversation, PrivateMessage, UserBlock, Reports, SubscriptionPlans, and ProfileOption for dynamic customization. Deployment and backup infrastructure includes `scripts/backup.py`, `scripts/restore.py`, `scripts/migrate_database.py`, and `scripts/update_from_github.py`, all manageable via admin API endpoints.

## External Dependencies
- **PostgreSQL**: Primary database.
- **Tailwind CSS**: Frontend styling.
- **QRious library (v4.0.2)**: QR code generation.
- **Python Flask**: Backend web framework.
- **SQLAlchemy**: Python ORM.
- **PyJWT**: JWT authentication.
- **Bcrypt**: Password hashing.
- **Cryptography (Fernet/AES-256)**: Data encryption at rest.
- **Flask-CORS**: Cross-Origin Resource Sharing.
- **Gunicorn**: Production WSGI server.

## Recent Changes (October 2025)
- **Data Security & Seed System Overhaul** (October 9):
  - Verified all sensitive data encryption: email, name, bio, photo_url encrypted with AES-256 (Fernet)
  - Created comprehensive seed system with 43 pre-loaded profile options (persistent across restarts)
  - Profile options include: Genders (4), Sexual Orientations (6), Religions (10), Meeting Types (5), Interests (15), LGBTQ Friendly (3)
  - Implemented automated seed for default data: 1 admin (admin@matchspot.com), 1 establishment (cafe@test.com), 2 test users (sophie@test.com, julien@test.com)
  - All seed data persists after server restarts - stored in PostgreSQL database
  - CRUD admin panel fully functional with real-time activation/deactivation toggle for profile options
  - Options instantly synchronized between admin panel and signup forms
  - Moved SECRET_KEY and ENCRYPTION_KEY from files to secure Replit environment variables
  - Removed .encryption_key file for enhanced security
  - File: backend/utils/seed_data.py handles all initialization
- **Enhanced User Registration** (October 9):
  - Added age validation: minimum 18 years old required for registration
  - Made all profile fields mandatory: gender, orientation, meeting type, religion, LGBT friendly, interests, and bio
  - Added comprehensive interests selection with 12 options (music, travel, sports, food, art, cinema, reading, tech, gaming, fashion, photography, fitness)
  - Religion and LGBT friendly fields now required during signup
  - Backend validation ensures all required fields are provided before account creation
  - Frontend validates at least one interest must be selected
- **Subscription Request System** (October 9):
  - Created new SubscriptionRequest model for managing paid subscription upgrades
  - Users can request subscription upgrades (Premium, Platinum) from their profile
  - Admin can approve/reject subscription requests with optional rejection reason
  - New API endpoints: `/api/subscriptions/request`, `/api/subscriptions/my-requests`, `/api/subscriptions/pending`
  - Admin endpoints for approval/rejection: `/api/subscriptions/<id>/approve`, `/api/subscriptions/<id>/reject`
  - Approved subscriptions automatically update user's subscription_tier
  - Complete audit trail with timestamps and reviewer tracking
- **Image Upload System Overhaul** (October 7):
  - Fixed registration timeout issues caused by large base64 images
  - Created new `/api/upload/image` endpoint for progressive image uploads
  - Images now upload automatically when selected (no waiting until final submit)
  - Added real-time status bar with visual feedback (⏳ uploading, ✓ success, ❌ error)
  - Added security validation: max 10MB, JPEG/PNG only
  - Registration now sends lightweight URLs instead of heavy base64 data
  - Users get clear error messages throughout the signup process
- **User Registration Bug Fix** (October 7):
  - Fixed critical TypeError during user registration
  - Corrected 'photos' parameter to 'gallery_photos' to match User model schema
  - Ensured gallery_photos always receives a list (even empty) to prevent NULL values
  - Registration now works correctly with or without gallery photos
- **Badge Visibility Improvement** (October 7):
  - Increased opacity of non-verified user badges from 50 to 60 for better visibility
  - Gray badges (✓) now more visible for non-verified users across all interfaces
  - Applied consistently in: participants list, conversation list, request list, chat header, profile modal
- **Subscription Plans Management & UI Enhancements** (October 9):
  - Added comprehensive CRUD system for subscription plans in admin panel with activation/deactivation toggle
  - Created dedicated admin page "Gérer les Plans" for managing both user and establishment subscription plans
  - Added `is_active` column to SubscriptionPlan model for plan activation control
  - New admin API endpoints: GET/POST `/api/admin/plans`, PUT `/api/admin/plans/<id>`, POST `/api/admin/plans/<id>/toggle`
  - Fixed subscription requests loading issue in admin panel with improved error handling
  - Subscription change modal now available for both users and establishments in profile section
  - Updated terminology across entire app: replaced "événements/salle" with "room/rooms" for consistency
  - All landing page signup buttons (Free/Premium/Platinum) now properly trigger registration modal
  - Fixed internationalization (i18n) system on landing page with automatic language detection from localStorage
- **VPS Deployment & Production Fixes** (October 9):
  - Fixed critical database migration issue for VPS/Hostinger deployment: `subscription_plans.role` column missing error
  - Created automatic database migration system (`backend/utils/db_migration.py`) that runs on startup
  - Migration system automatically adds missing columns to existing tables (role, is_active) without data loss
  - Fixed subscription plan initialization to include `role='establishment'` parameter
  - Removed auto-generated encryption key warning from console logs for production environments
  - Users must now set ENCRYPTION_KEY and SECRET_KEY as environment variables (not auto-generated)
  - Updated admin user detection to use username instead of encrypted email for reliability
- **Landing Page UX Improvements** (October 9):
  - All CTA buttons (Commencer, Premium, Platinum) now trigger step-by-step user registration directly
  - Added copyright footer: "© 2025 MatchSpot - Fait avec ❤️ et ☕ par MOA Digital Agency LLC"
  - Footer includes clickable link to myoneart.com
  - Dynamic year display in copyright automatically updates
- **Subscription Plans Fix** (October 9):
  - Fixed missing user subscription plans in database initialization
  - Created 3 user plans: Free ($0), Premium ($19), Platinum ($39)
  - Created 3 establishment plans: One-shot ($9), Silver ($49), Gold ($99)
  - Updated initialization logic to create both user and establishment plans separately
  - Plans now display correctly in user profile "Changer de Forfait" modal