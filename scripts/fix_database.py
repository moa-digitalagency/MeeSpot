#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import db, create_app
from backend.utils.db_migration import run_migrations
from sqlalchemy import text, inspect

def fix_database():
    app = create_app()
    
    with app.app_context():
        print("=== Correction base de données ===\n")
        
        try:
            db.session.execute(text("SELECT 1"))
            print("✅ Connexion DB OK\n")
        except Exception as e:
            print(f"❌ Erreur connexion: {e}")
            return False
        
        try:
            db.create_all()
            print("✅ Tables créées\n")
        except Exception as e:
            print(f"⚠️  {e}\n")
        
        try:
            run_migrations()
            print("✅ Migrations appliquées\n")
        except Exception as e:
            print(f"❌ Erreur migrations: {e}\n")
            return False
        
        try:
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('establishments')]
            required = ['rooms_created_this_week', 'week_start_date']
            missing = [col for col in required if col not in columns]
            
            if missing:
                print(f"❌ Colonnes manquantes: {', '.join(missing)}")
                return False
            else:
                print("✅ Toutes les colonnes présentes")
        except Exception as e:
            print(f"⚠️  {e}")
        
        print("\n=== Correction terminée ===")
        return True

if __name__ == '__main__':
    success = fix_database()
    sys.exit(0 if success else 1)
