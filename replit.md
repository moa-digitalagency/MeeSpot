# MeetSpot - PWA Dating Platform

## Overview
MeetSpot is a Progressive Web Application (PWA) dating platform designed to facilitate real-life meetings at physical venues. Inspired by clean interfaces, its core purpose is to connect users for events rather than endless swiping. The platform supports multiple user roles: Admin for platform management, Establishment for venue owners to create events, and Users for members to join rooms and connect. It aims to offer a modern, mobile-first experience with a focus on privacy, security, and user-friendly interaction, ultimately fostering real-life connections.

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
MeetSpot is built as a PWA with a Python Flask backend and a Tailwind CSS frontend. It utilizes a modular backend structure with PostgreSQL via SQLAlchemy ORM. Authentication is handled with JWT (stored in localStorage) and bcrypt for password hashing. All sensitive data, including personal information and private messages, is encrypted at rest using AES-256 (Fernet) with SQLAlchemy TypeDecorators. The frontend uses Vanilla JavaScript for interactivity, supporting full PWA features like service workers for offline support, app manifests for installability, and push notification readiness. An auto-refresh system provides real-time data synchronization for conversations, requests, and room activities, intelligently pausing when the app loses focus. CORS is configured with `supports_credentials=False` and wildcard origins. All API endpoints validate request data.

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
- **Badge Visibility Improvement** (October 7):
  - Increased opacity of non-verified user badges from 50 to 60 for better visibility
  - Gray badges (✓) now more visible for non-verified users across all interfaces
  - Applied consistently in: participants list, conversation list, request list, chat header, profile modal