#!/bin/bash

echo "=== Script de déploiement MatchSpot ==="
echo ""

echo "1. Mise à jour du code depuis GitHub..."
if git pull origin main 2>/dev/null || git pull origin master 2>/dev/null; then
    echo "✓ Code mis à jour"
else
    echo "ℹ Code déjà à jour ou pas de remote Git"
fi
echo ""

echo "2. Vérification des variables d'environnement..."
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  DATABASE_URL n'est pas défini - Essai de construction..."
    if [ -n "$PGUSER" ] && [ -n "$PGPASSWORD" ] && [ -n "$PGHOST" ] && [ -n "$PGDATABASE" ]; then
        export DATABASE_URL="postgresql://${PGUSER}:${PGPASSWORD}@${PGHOST}:${PGPORT:-5432}/${PGDATABASE}"
        echo "✓ DATABASE_URL construit: postgresql://${PGUSER}:***@${PGHOST}:${PGPORT:-5432}/${PGDATABASE}"
    else
        echo "❌ Impossible de construire DATABASE_URL - Variables PostgreSQL manquantes"
        exit 1
    fi
else
    echo "✓ DATABASE_URL défini"
fi

if [ -z "$ENCRYPTION_KEY" ]; then
    echo "⚠️  ENCRYPTION_KEY n'est pas défini"
    echo "   Générez une clé avec: python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'"
    exit 1
else
    echo "✓ ENCRYPTION_KEY défini"
fi
echo ""

echo "3. Application des migrations de base de données..."
python3 scripts/fix_database.py
if [ $? -ne 0 ]; then
    echo "❌ Erreur lors des migrations"
    exit 1
fi
echo ""

echo "4. L'application va redémarrer automatiquement..."
echo "   Le workflow Replit détecte les changements et redémarre"
echo ""

echo "=== Déploiement terminé avec succès ==="
echo ""
echo "Vérifiez que l'application fonctionne dans l'interface Replit"
