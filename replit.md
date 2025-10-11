# MatchSpot - PWA Dating Platform

## Overview
MatchSpot is a Progressive Web Application (PWA) dating platform designed to facilitate real-life meetings at physical venues. Its core purpose is to connect users for events rather than endless swiping, offering a modern, mobile-first experience with a focus on privacy, security, and user-friendly interaction. The platform supports Admin for management, Establishment for venue owners, and Users for members to join rooms and connect, aiming to foster real-life connections.

## Recent Changes

### Consolidation du Système de Galerie Photo (11 Octobre 2025)
- ✅ **Composant réutilisable** : Créé `GalleryRenderer` avec 3 modes d'affichage (standard, éditable, compact)
- ✅ **Upload unifié** : Inscription et modification utilisent le même système via `UnifiedUploadHelper.uploadMultiple()`
- ✅ **Affichage systématique** : Galerie visible dans profil, modales, et cards de participants (max 3 photos avec +N)
- ✅ **Backend** : Ajout de `gallery_photos` aux données des participants dans les rooms
- 📄 Voir `CHANGELOG_GALLERY_CONSOLIDATION.md` pour les détails complets

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
The platform features a mobile-first responsive design, limited to a maximum viewport width of 768px. It uses a distinct color palette: Primary #FF4458 (vibrant coral), Secondary #6C5CE7 (soft purple), Accent #A29BFE (lavender), Background #F5F5F5 (light grey), and Text #2D3436 (charcoal). Typography is Poppins for headings and Inter for body text. Navigation uses fixed bottom navigation bars with SVG icons and bottom sheet modals across all dashboards (User, Establishment, Admin).

### Technical Implementations
MatchSpot is built as a PWA with a Python Flask backend and a Tailwind CSS frontend. It utilizes a modular backend structure with PostgreSQL via SQLAlchemy ORM. Authentication uses JWT (stored in localStorage) and bcrypt for password hashing. Sensitive data is encrypted at rest using AES-256 (Fernet). The frontend uses Vanilla JavaScript for interactivity, supporting PWA features like service workers for offline support, app manifests, and push notification readiness. An auto-refresh system provides real-time data synchronization, pausing intelligently when the app loses focus. CORS is configured with wildcard origins. All API endpoints validate request data.

### Feature Specifications
- **User Roles & Access Control**: Admin, Establishment, and User roles with role-based access, including gender, orientation, and age filtering.
- **Rooms System**: Event-based meeting spaces at physical venues with 24-hour expiration, joined via 8-character access codes or QR scanning.
- **Connection & Communication**: Connection requests establish private, encrypted 1-to-1 conversations with text, emojis, and photo uploads, replacing group chat.
- **Conversation Expiration System**: Conversations expire based on subscription tier (24h, 7 days, 30 days), enforced server-side with UI countdowns.
- **User Blocking System**: Bidirectional blocking makes users invisible across the platform.
- **Subscription Tiers**: Multiple tiers for Users (Free, Premium, Platinum) and Establishments, offering features like priority access and analytics.
- **Profile Management**: Enriched user profiles with auto-generated usernames, dynamic age calculation, sexual orientation, multi-select meeting types, interests, and photo galleries. Admin can customize profile options.
- **Reporting & Moderation**: System for users to report inappropriate content with admin oversight.
- **User Verification**: Multi-step user verification with photo upload and admin approval/rejection.
- **Multi-step User Signup**: A 4-step registration process.
- **Backup & Deployment System**: Admin-managed system for automated backups, secure restoration, database migrations, and GitHub-based updates.

### System Design Choices
The backend organizes routes by resource (auth, rooms, establishments, admin, profile, connection_requests, conversations) and uses a centralized configuration. The database schema includes Users, Establishments, Rooms, RoomMembers, ConnectionRequest, PrivateConversation, PrivateMessage, UserBlock, Reports, SubscriptionPlans, and ProfileOption. Deployment and backup infrastructure includes `scripts/backup.py`, `scripts/restore.py`, `scripts/migrate_database.py`, and `scripts/update_from_github.py`, manageable via admin API endpoints.

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