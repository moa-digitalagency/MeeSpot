#!/usr/bin/env python3

import sys
import os

# Charger les variables d'environnement depuis .env
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import db, create_app
from backend.utils.db_migration import run_migrations
from sqlalchemy import text, inspect

def fix_database():
    # Vérifier DATABASE_URL
    if not os.environ.get('DATABASE_URL'):
        print("❌ ERREUR: DATABASE_URL n'est pas défini")
        print("   Créez un fichier .env avec:")
        print("   DATABASE_URL=postgresql://user:password@host:port/dbname")
        print("   ENCRYPTION_KEY=votre_clé")
        return False
    
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
            
            # Vérifier establishments
            est_columns = [col['name'] for col in inspector.get_columns('establishments')]
            est_required = ['rooms_created_this_week', 'week_start_date']
            est_missing = [col for col in est_required if col not in est_columns]
            
            # Vérifier rooms
            room_columns = [col['name'] for col in inspector.get_columns('rooms')]
            room_required = ['is_temporarily_disabled']
            room_missing = [col for col in room_required if col not in room_columns]
            
            if est_missing or room_missing:
                if est_missing:
                    print(f"❌ Establishments - colonnes manquantes: {', '.join(est_missing)}")
                if room_missing:
                    print(f"❌ Rooms - colonnes manquantes: {', '.join(room_missing)}")
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
