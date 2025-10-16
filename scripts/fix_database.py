#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import db, create_app
from backend.utils.db_migration import run_migrations
from sqlalchemy import text, inspect

def fix_database():
    """Corrige la base de données et applique les migrations"""
    
    app = create_app()
    
    with app.app_context():
        print("=== Correction de la base de données ===\n")
        
        print("1. Vérification de la connexion...")
        try:
            db.session.execute(text("SELECT 1"))
            print("   ✓ Connexion à la base de données OK\n")
        except Exception as e:
            print(f"   ✗ Erreur de connexion: {e}")
            return False
        
        print("2. Création des tables manquantes...")
        try:
            db.create_all()
            print("   ✓ Tables créées\n")
        except Exception as e:
            print(f"   ✗ Erreur création tables: {e}\n")
        
        print("3. Application des migrations...")
        try:
            run_migrations()
            print("   ✓ Migrations appliquées\n")
        except Exception as e:
            print(f"   ✗ Erreur migrations: {e}\n")
        
        print("4. Vérification des colonnes de la table establishments...")
        try:
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('establishments')]
            print(f"   Colonnes présentes: {', '.join(columns)}")
            
            required_columns = ['rooms_created_this_week', 'week_start_date']
            missing = [col for col in required_columns if col not in columns]
            
            if missing:
                print(f"   ⚠️  Colonnes manquantes: {', '.join(missing)}")
            else:
                print("   ✓ Toutes les colonnes requises sont présentes")
        except Exception as e:
            print(f"   ⚠️  Impossible de vérifier: {e}")
        
        print("\n=== Correction terminée ===")
        print("\nPour redémarrer l'application:")
        print("  gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app")
        
        return True

if __name__ == '__main__':
    success = fix_database()
    sys.exit(0 if success else 1)
