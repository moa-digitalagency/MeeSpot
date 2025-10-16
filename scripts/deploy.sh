#!/bin/bash

set -e

echo "=== Déploiement MeeSpot VPS ==="
echo ""

# 1. Git pull
echo "📥 1. Mise à jour du code..."
git pull origin main || git pull origin master
echo "   ✅ Code mis à jour"
echo ""

# 2. Activation environnement virtuel
echo "🐍 2. Activation environnement virtuel..."
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "   ✅ venv activé"
elif [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "   ✅ .venv activé"
else
    echo "   ⚠️  Pas de venv trouvé - création..."
    python3 -m venv venv
    source venv/bin/activate
    echo "   ✅ venv créé et activé"
fi
echo ""

# 3. Installation dépendances
echo "📦 3. Installation des dépendances..."
pip install -r requirements.txt --quiet
echo "   ✅ Dépendances installées"
echo ""

# 4. Vérification fichier .env
echo "🔐 4. Vérification configuration..."
if [ ! -f ".env" ]; then
    echo "   ⚠️  ATTENTION: Fichier .env manquant!"
    echo "   Créez un fichier .env avec:"
    echo "   DATABASE_URL=postgresql://user:password@host:port/dbname"
    echo "   ENCRYPTION_KEY=votre_clé"
    exit 1
fi
echo "   ✅ Fichier .env présent"
echo ""

# 5. Migrations base de données
echo "🔧 5. Application des migrations..."
python3 scripts/fix_database.py
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Erreur lors des migrations - arrêt du déploiement"
    exit 1
fi
echo ""

# 6. Redémarrage application
echo "🔄 6. Redémarrage de l'application..."

# Détection et arrêt du processus existant
if pgrep -f "gunicorn.*main:app" > /dev/null; then
    echo "   ⏹️  Arrêt de l'instance existante..."
    pkill -f "gunicorn.*main:app"
    sleep 2
fi

# Vérifier si systemd service existe
if [ -f "/etc/systemd/system/meetspot.service" ]; then
    sudo systemctl restart meetspot
    echo "   ✅ Service systemd redémarré"
elif [ -f "/etc/systemd/system/matchspot.service" ]; then
    sudo systemctl restart matchspot
    echo "   ✅ Service systemd redémarré"
else
    # Démarrage manuel avec gunicorn
    echo "   🚀 Démarrage gunicorn..."
    mkdir -p logs
    nohup gunicorn --bind 0.0.0.0:5000 --reuse-port --workers 4 main:app > logs/gunicorn.log 2>&1 &
    echo "   ✅ Gunicorn démarré (PID: $!)"
fi

echo ""
echo "✅ Déploiement terminé avec succès"
echo ""
echo "Pour vérifier les logs: tail -f logs/gunicorn.log"
