#!/bin/bash
# Script de déploiement rapide - pour utilisation après git pull

echo "🚀 Déploiement rapide MatchSpot"
echo ""

# Correction de la base de données
echo "📦 Correction de la base de données..."
python3 scripts/fix_database.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Déploiement terminé!"
    echo "   L'application redémarre automatiquement"
else
    echo ""
    echo "❌ Erreur pendant le déploiement"
    exit 1
fi
