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
The platform features a mobile-first responsive design, limited to a maximum viewport width of 768px. It uses a distinct color palette: Primary #FF4458 (vibrant coral), Secondary #6C5CE7 (soft purple), Accent #A29BFE (lavender), Background #FFEAA7 (warm cream), and Text #2D3436 (charcoal). Typography is set with Poppins for headings and Inter for body text. Navigation is managed through fixed bottom navigation bars with SVG icons and bottom sheet modals for mobile-optimized interactions across all dashboards (User, Establishment, Admin).

### Technical Implementations
MeetSpot is built as a PWA with a Python Flask backend and a Tailwind CSS frontend. It utilizes a modular backend structure with PostgreSQL via SQLAlchemy ORM. Authentication is handled with JWT and bcrypt for password hashing. All sensitive data, including personal information and private messages, is encrypted at rest using AES-256 (Fernet) with SQLAlchemy TypeDecorators. The frontend uses Vanilla JavaScript for interactivity, supporting full PWA features like service workers for offline support, app manifests for installability, and push notification readiness. An auto-refresh system provides real-time data synchronization for conversations, requests, and room activities, intelligently pausing when the app loses focus.

### Feature Specifications
- **User Roles & Access Control**: Admin, Establishment, and User roles with role-based access control. Room access can be filtered by gender, orientation, and age.
- **Rooms System**: Event-based meeting spaces at physical venues with 24-hour expiration. Rooms are joined via unique 8-character access codes or QR code scanning.
- **Connection & Communication**: Replaces group chat with a system of connection requests between users. Upon acceptance, private 1-to-1 encrypted conversations are established.
- **Subscription Tiers**: Multiple tiers for Users (Free, Premium, Platinum) offering features like priority access, alternative identity mode (hiding photos/pseudonyms), and unlimited messaging. Establishments also have subscription plans for creating rooms and accessing analytics.
- **Profile Management**: Enriched user profiles include auto-generated usernames, birthdate (for dynamic age calculation), sexual orientation, multi-select meeting types, interests, and photo galleries. Admin-customizable profile options (gender, meeting type, interest) are managed via a dedicated dashboard.
- **Reporting & Moderation**: A system for users to report inappropriate content or behavior, with admin oversight.

### System Design Choices
The backend organizes routes by resource (auth, rooms, establishments, admin, profile, connection_requests, conversations) and uses a centralized configuration. Database schema includes Users (with detailed demographics and subscription info), Establishments, Rooms (with access rules and expiration), RoomMembers, ConnectionRequest, PrivateConversation, PrivateMessage, Reports, and SubscriptionPlans. A `ProfileOption` model allows admins to define and manage selectable options for user profiles dynamically.

## External Dependencies
- **PostgreSQL**: Primary database for all application data.
- **Tailwind CSS**: Utility-first CSS framework for styling the frontend.
- **QRious library (v4.0.2)**: Used for generating QR codes for establishment events.
- **Python Flask**: Web framework for the backend.
- **SQLAlchemy**: Python SQL toolkit and Object-Relational Mapper.
- **PyJWT**: Python library for JSON Web Token (JWT) authentication.
- **Bcrypt**: For password hashing.
- **Cryptography (Fernet/AES-256)**: For encryption of sensitive data at rest.