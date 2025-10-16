#!/bin/bash

echo "=== Script de déploiement MatchSpot ==="
echo ""

echo "1. Mise à jour du code depuis GitHub..."
git pull origin main || git pull origin master
echo "✓ Code mis à jour"
echo ""

echo "2. Installation des dépendances Python..."
pip install -r requirements.txt --quiet
echo "✓ Dépendances installées"
echo ""

echo "3. Vérification des variables d'environnement..."
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  DATABASE_URL n'est pas défini"
    exit 1
fi

if [ -z "$ENCRYPTION_KEY" ]; then
    echo "⚠️  ENCRYPTION_KEY n'est pas défini"
    exit 1
fi

echo "✓ Variables d'environnement OK"
echo ""

echo "4. Application des migrations de base de données..."
python3 << 'EOF'
from backend import db, create_app
from backend.utils.db_migration import run_migrations

app = create_app()
with app.app_context():
    print("   - Création des tables si nécessaire...")
    db.create_all()
    print("   - Application des migrations...")
    run_migrations()
    print("   ✓ Migrations terminées")
EOF
echo ""

echo "5. Redémarrage de l'application..."
if command -v pkill &> /dev/null; then
    pkill -f gunicorn
    sleep 2
fi
echo "✓ Application prête à redémarrer"
echo ""

echo "=== Déploiement terminé avec succès ==="
echo ""
echo "Pour démarrer l'application, utilisez:"
echo "  gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app"
