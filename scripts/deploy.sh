#!/bin/bash

set -e

echo "=== Déploiement MeeSpot VPS ==="
echo ""

# 1. Git pull
echo "📥 Mise à jour du code..."
git pull origin main || git pull origin master
echo ""

# 2. Migrations base de données
echo "🔧 Application des migrations..."
python3 scripts/fix_database.py
echo ""

# 3. Redémarrage
echo "🔄 Redémarrage de l'application..."
if [ -f "/etc/systemd/system/meetspot.service" ]; then
    sudo systemctl restart meetspot
    echo "✅ Service systemd redémarré"
elif pgrep -f "gunicorn.*main:app" > /dev/null; then
    pkill -f "gunicorn.*main:app"
    sleep 2
    nohup gunicorn --bind 0.0.0.0:5000 --reuse-port main:app > /dev/null 2>&1 &
    echo "✅ Gunicorn redémarré"
else
    echo "⚠️  Démarrez manuellement: gunicorn --bind 0.0.0.0:5000 main:app"
fi

echo ""
echo "✅ Déploiement terminé"
