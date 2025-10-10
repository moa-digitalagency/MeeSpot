#!/usr/bin/env python3
"""
Script de vérification de la configuration MatchSpot
Vérifie que toutes les variables d'environnement nécessaires sont présentes
"""

import os
import sys
from dotenv import load_dotenv

def check_env_var(var_name, critical=True):
    """Vérifie qu'une variable d'environnement existe"""
    value = os.environ.get(var_name)
    if value:
        print(f"✅ {var_name}: Configuré ({len(value)} caractères)")
        return True
    else:
        status = "❌ CRITIQUE" if critical else "⚠️  Optionnel"
        print(f"{status} {var_name}: MANQUANT!")
        return not critical

def main():
    print("=" * 60)
    print("🔍 Vérification de la Configuration MatchSpot")
    print("=" * 60)
    print()
    
    load_dotenv()
    
    print("📦 Variables Critiques:")
    print("-" * 60)
    
    all_ok = True
    
    secret_key = os.environ.get('SECRET_KEY') or os.environ.get('SESSION_SECRET')
    if secret_key:
        source = "SECRET_KEY" if os.environ.get('SECRET_KEY') else "SESSION_SECRET"
        print(f"✅ {source}: Configuré ({len(secret_key)} caractères)")
    else:
        print("❌ CRITIQUE SECRET_KEY ou SESSION_SECRET: MANQUANT!")
        all_ok = False
    
    all_ok &= check_env_var('ENCRYPTION_KEY', critical=True)
    
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        print(f"✅ DATABASE_URL: Configuré")
        if database_url.startswith('postgres://'):
            print("   ⚠️  Format postgres:// détecté (sera auto-converti en postgresql://)")
    else:
        print("⚠️  DATABASE_URL: MANQUANT (tentative construction auto depuis PG* vars)")
        pg_vars = ['PGUSER', 'PGPASSWORD', 'PGHOST', 'PGDATABASE']
        missing = [v for v in pg_vars if not os.environ.get(v)]
        if missing:
            print(f"   ❌ Variables PG manquantes: {', '.join(missing)}")
            all_ok = False
        else:
            print(f"   ✅ Toutes les variables PG présentes (construction auto possible)")
    
    print()
    print("📊 Variables Optionnelles:")
    print("-" * 60)
    
    flask_env = os.environ.get('FLASK_ENV', 'development')
    print(f"ℹ️  FLASK_ENV: {flask_env}")
    
    print()
    print("=" * 60)
    
    if all_ok:
        print("✅ CONFIGURATION OK - Prêt pour le déploiement!")
        print()
        print("💡 Commandes suivantes:")
        print("   - Test local: python main.py")
        print("   - Production: gunicorn --bind 0.0.0.0:5000 main:app")
        return 0
    else:
        print("❌ CONFIGURATION INCOMPLÈTE - Corrigez les erreurs ci-dessus")
        print()
        print("📝 Pour corriger:")
        print("   1. Copiez .env.example vers .env")
        print("   2. Remplissez les valeurs manquantes")
        print("   3. Relancez ce script: python verify_config.py")
        return 1

if __name__ == '__main__':
    sys.exit(main())
