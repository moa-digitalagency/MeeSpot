# MeetSpot - VPS Deployment Guide (Hostinger/Ubuntu)

## Prerequisites
- Ubuntu/Debian VPS server
- Python 3.11 or higher
- PostgreSQL 12 or higher
- Nginx (for reverse proxy)
- PM2 (for process management)

## Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx -y

# Install PM2 for process management
sudo npm install -g pm2
```

## Step 2: Database Setup

```bash
# Create PostgreSQL database and user
sudo -u postgres psql
```

```sql
CREATE DATABASE meetspot;
CREATE USER meetspot_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE meetspot TO meetspot_user;
\q
```

## Step 3: Environment Variables

Create a `.env` file in your project root:

```bash
# Database Configuration
DATABASE_URL=postgresql://meetspot_user:your_secure_password@localhost:5432/meetspot
PGHOST=localhost
PGPORT=5432
PGUSER=meetspot_user
PGPASSWORD=your_secure_password
PGDATABASE=meetspot

# Security Keys (IMPORTANT: Generate your own!)
SECRET_KEY=your-secret-key-here-change-me-in-production
ENCRYPTION_KEY=your-fernet-encryption-key-here

# Application Settings
FLASK_ENV=production
PORT=5000
```

### Generate Secure Keys

```bash
# Generate ENCRYPTION_KEY
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"
```

⚠️ **IMPORTANT**: Save these keys securely! Once you encrypt data with ENCRYPTION_KEY, you cannot decrypt it with a different key.

## Step 4: Application Setup

```bash
# Clone your repository
git clone https://github.com/moa-digitalagency/MeeSpot.git meetspot
cd meetspot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 5: Database Migration

The application includes an automatic migration system that runs on startup. It will:
- Create all necessary tables
- Add missing columns to existing tables (role, is_active, etc.)
- Initialize default data (admin user, subscription plans, profile options)

No manual migration needed! The system handles it automatically.

## Step 6: PM2 Configuration

Create `ecosystem.config.js`:

```javascript
module.exports = {
  apps: [{
    name: 'meespot',
    script: 'venv/bin/gunicorn',
    args: '--bind 0.0.0.0:5000 --workers 4 main:app',
    cwd: '/path/to/meetspot',
    env: {
      FLASK_ENV: 'production'
    },
    error_file: '~/.pm2/logs/meespot-error.log',
    out_file: '~/.pm2/logs/meespot-out.log',
    merge_logs: true
  }]
}
```

Start the application:

```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## Step 7: Nginx Configuration

Create `/etc/nginx/sites-available/meetspot`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/meetspot/static;
        expires 30d;
    }

    client_max_body_size 10M;
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/meetspot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 8: SSL Certificate (Optional but Recommended)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

## Common Issues & Solutions

### 1. Database Column Missing Error
**Error**: `column subscription_plans.role does not exist`

**Solution**: The automatic migration system will fix this on startup. If it persists:
```bash
# Restart the application
pm2 restart meespot
```

### 2. Encryption Key Warning
**Error**: `⚠️ ENCRYPTION_KEY auto-generated`

**Solution**: Set ENCRYPTION_KEY in your environment:
```bash
# Add to .env file or set as environment variable
export ENCRYPTION_KEY="your-fernet-key-here"
```

### 3. Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER /path/to/meetspot
chmod 755 /path/to/meetspot
```

## Monitoring

```bash
# View logs
pm2 logs meespot

# Monitor application
pm2 monit

# Check status
pm2 status
```

## Updates & Maintenance

```bash
# Pull latest changes
git pull origin main

# Install new dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart application (migrations run automatically)
pm2 restart meespot
```

## Backup

The application includes built-in backup functionality:
- Use admin panel: `/admin` → Backup & Restore
- Automated backups are stored in `/backups` directory
- Includes database, uploaded files, and configuration

## Security Checklist

- ✅ Use strong passwords for database
- ✅ Generate unique SECRET_KEY and ENCRYPTION_KEY
- ✅ Enable SSL/HTTPS with Certbot
- ✅ Keep ENCRYPTION_KEY secure and backed up
- ✅ Set proper file permissions
- ✅ Use firewall (UFW) to restrict access
- ✅ Regular security updates: `sudo apt update && sudo apt upgrade`

## Performance Optimization

```bash
# Increase Gunicorn workers (rule: 2-4 × CPU cores)
# Edit ecosystem.config.js:
args: '--bind 0.0.0.0:5000 --workers 8 --worker-class gevent main:app'

# Install gevent for better concurrency
pip install gevent
```

## Support

For issues or questions:
- Check logs: `pm2 logs meespot`
- Review error logs: `~/.pm2/logs/meespot-error.log`
- Database issues: Check PostgreSQL logs in `/var/log/postgresql/`

---

**MOA Digital Agency LLC**  
www.myoneart.com
