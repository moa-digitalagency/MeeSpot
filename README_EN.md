# MeetSpot - PWA Dating Platform

🇬🇧 English Version | [🇫🇷 Version Française](./README.md)

## 📱 Overview

MeetSpot is a progressive web application (PWA) dating platform focused on real-life meetings at physical venues. Inspired by Bumble and Hinge's clean interfaces, built with Python Flask backend and HTML/Tailwind CSS/JavaScript frontend.

### 🎯 Unique Concept

Unlike traditional dating apps based on endless swiping, MeetSpot focuses on authentic connections at curated events in local establishments.

## ✨ Key Features

### 🏠 Event System
- **24-hour automatic expiration** : All events expire 24 hours after creation
- **Unique access codes** : 8-character codes for easy event joining
- **QR Scanner** : Join events by scanning QR codes with camera
- **Access filters** : Control based on gender, orientation, and age

### 💬 Connection System
- **No group chat** : Focus on individual connections
- **Connection requests** : Send requests to participants you're interested in
- **1-to-1 private conversations** : Encrypted messages after connection acceptance
- **Persistent conversations** : Conversations remain active after events expire

### 👤 User Roles

#### User
- Join events with access codes or QR
- View event participants
- Send/accept connection requests
- Encrypted private conversations

#### Establishment
- Create events (limited by subscription)
- Manage participants
- Generate QR codes for events
- Access to analytics

#### Administrator
- Platform management
- User moderation
- Report management

### 💎 Subscriptions

**For Users:**
- **Free** : Browse and join public events
- **Premium** ($19/mo) : Priority access, alternative identity mode
- **Platinum** ($39/mo) : VIP access, unlimited messaging

**For Establishments:**
- **One-Shot** ($9) : 1 event per day
- **Silver** ($49/mo) : 1 event/day + advanced analytics
- **Gold** ($99/mo) : 3 events/day + premium features

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- Node.js (for Tailwind CSS)

### Installation

1. **Clone the repository**
```bash
git clone <repo-url>
cd meetspot
```

2. **Install Python dependencies**
```bash
pip install flask flask-cors flask-sqlalchemy psycopg2-binary bcrypt cryptography pyjwt python-dotenv
```

3. **Database setup**
```bash
# PostgreSQL database is automatically configured on Replit
# For local environment, configure DATABASE_URL
export DATABASE_URL="postgresql://user:password@localhost/meetspot"
```

4. **Encryption key configuration**
```bash
# Development: Key auto-generated and saved to .encryption_key
# Production: MANDATORY - Set as environment variable
export ENCRYPTION_KEY="your_fernet_encryption_key"
```

5. **Launch the application**
```bash
python main.py
```

The application will be accessible at `http://localhost:5000`

### First Admin Account

1. Create an account via the registration form
2. Update the role in the database:
```sql
UPDATE users SET role = 'admin' WHERE email = 'your@email.com';
```

## 📱 User Interface

### Navigation (4 tabs)
1. **Home** : Access code, QR scanner, my events
2. **Chat** : Private conversations list
3. **Requests** : Received/sent requests
4. **Profile** : Profile management and logout

### User Flow
1. Join an event (code or QR)
2. View participants
3. Send connection requests
4. Accept/Reject requests
5. Chat privately after acceptance

## 🛠️ Technical Architecture

### Backend (Flask)
```
backend/
├── __init__.py              # App initialization
├── config.py                # Centralized configuration
├── models/                  # SQLAlchemy models
│   ├── user.py
│   ├── room.py
│   ├── connection_request.py
│   ├── private_conversation.py
│   └── ...
├── routes/                  # API Blueprints
│   ├── auth.py
│   ├── rooms.py
│   ├── connection_requests.py
│   ├── conversations.py
│   └── ...
└── utils/                   # Utilities
    ├── auth.py             # JWT and decorators
    └── encryption.py       # AES-256 encryption
```

### Frontend
```
static/
└── pages/
    ├── index.html          # Landing page
    ├── app.html            # User dashboard
    ├── establishment.html  # Establishment dashboard
    └── admin.html          # Admin dashboard
```

### Database (PostgreSQL)

**Main Tables:**
- `users` : Users with demographics and subscriptions
- `establishments` : Establishments with subscription plans
- `rooms` : Events with 24h expiration
- `room_members` : Active event members
- `connection_request` : Requests (pending/accepted/rejected)
- `private_conversation` : 1-to-1 conversations
- `private_message` : Encrypted messages
- `reports` : Reporting system

## 🔐 Security

### Data Encryption
All sensitive data is encrypted with Fernet (AES-256):
- User emails, names, bios, photos
- Message content
- Alternative names (alternative identity mode)

### Authentication
- JWT tokens for authentication
- Passwords hashed with bcrypt
- Role-based access control

### Encryption Key
**⚠️ IMPORTANT** : The `ENCRYPTION_KEY` is essential
- **Development** : Auto-generated and saved to `.encryption_key`
- **Production** : **MUST** be set as environment variable
- Losing this key = encrypted data is unrecoverable

## 📚 API Documentation

See the [complete API documentation](./API_DOCS_EN.md) for all endpoints.

**Main Endpoints:**
- `POST /api/auth/register` - Registration
- `POST /api/auth/login` - Login
- `GET /api/rooms` - List events
- `POST /api/rooms/join-by-code` - Join by code
- `GET /api/rooms/<id>/participants` - View participants
- `POST /api/requests` - Send a request
- `GET /api/conversations` - List conversations
- `POST /api/conversations/<id>/messages` - Send a message

## 🎨 Design System

### Color Palette
- **Primary** : #FF4458 (vibrant coral)
- **Secondary** : #6C5CE7 (soft purple)
- **Accent** : #A29BFE (lavender)
- **Background** : #FFEAA7 (warm cream)
- **Text** : #2D3436 (charcoal)
- **Success** : #00B894 (mint green)

### Typography
- **Headings** : Poppins (600, 700)
- **Body** : Inter (300-700)

## 📦 Deployment

### Preparing for Production

1. **Environment variables**
```bash
export FLASK_ENV=production
export SECRET_KEY="your_jwt_secret_key"
export ENCRYPTION_KEY="your_fernet_encryption_key"
export DATABASE_URL="postgresql://..."
```

2. **Use a WSGI server**
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port main:app
```

3. **HTTPS configuration**
Always use HTTPS in production to protect JWT tokens and data.

## 🤝 Contributing

Contributions are welcome! See our contribution guidelines.

## 📄 License

This project is under MIT License.

## 🌐 Links

- [API Documentation (French)](./API_DOCS_FR.md)
- [API Documentation (English)](./API_DOCS_EN.md)
- [French README](./README.md)

## 📞 Support

For any questions or issues, open an issue on GitHub.

---

**Made with ❤️ to foster real connections**
