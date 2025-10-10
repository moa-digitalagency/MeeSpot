#!/usr/bin/env python3
#
# MatchSpot - Script de migration automatique de base de données
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

import os
import sys
from sqlalchemy import create_engine, inspect, MetaData, Table, Column
from sqlalchemy.schema import CreateTable
import subprocess

# Ajouter le dossier parent au path pour importer backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import db
from backend.models.user import User
from backend.models.room import Room
from backend.models.room_member import RoomMember
from backend.models.establishment import Establishment
from backend.models.connection_request import ConnectionRequest
from backend.models.private_conversation import PrivateConversation
from backend.models.private_message import PrivateMessage
from backend.models.report import Report
from backend.models.profile_option import ProfileOption

class DatabaseMigrator:
    def __init__(self):
        self.db_url = os.environ.get('DATABASE_URL')
        if not self.db_url:
            raise Exception("DATABASE_URL non définie")
        
        self.engine = create_engine(self.db_url)
        self.inspector = inspect(self.engine)
        
    def get_existing_tables(self):
        """Récupère la liste des tables existantes"""
        return self.inspector.get_table_names()
    
    def get_table_columns(self, table_name):
        """Récupère les colonnes d'une table"""
        columns = {}
        for col in self.inspector.get_columns(table_name):
            columns[col['name']] = col
        return columns
    
    def get_model_tables(self):
        """Récupère les tables définies dans les modèles SQLAlchemy"""
        return db.metadata.tables
    
    def check_missing_tables(self):
        """Vérifie les tables manquantes"""
        existing = set(self.get_existing_tables())
        model_tables = set(self.get_model_tables().keys())
        
        missing = model_tables - existing
        extra = existing - model_tables - {'alembic_version'}
        
        return list(missing), list(extra)
    
    def check_missing_columns(self):
        """Vérifie les colonnes manquantes dans les tables existantes"""
        changes = {}
        
        for table_name, table in self.get_model_tables().items():
            if table_name in self.get_existing_tables():
                existing_cols = set(self.get_table_columns(table_name).keys())
                model_cols = set([col.name for col in table.columns])
                
                missing = model_cols - existing_cols
                extra = existing_cols - model_cols
                
                if missing or extra:
                    changes[table_name] = {
                        'missing': list(missing),
                        'extra': list(extra)
                    }
        
        return changes
    
    def create_missing_tables(self):
        """Crée les tables manquantes"""
        print("🔍 Vérification des tables manquantes...")
        
        missing_tables, _ = self.check_missing_tables()
        
        if not missing_tables:
            print("  ✓ Toutes les tables existent")
            return True
        
        print(f"  📝 Création de {len(missing_tables)} table(s) manquante(s):")
        for table_name in missing_tables:
            print(f"     - {table_name}")
        
        try:
            # Créer toutes les tables avec SQLAlchemy
            db.metadata.create_all(self.engine)
            print("  ✅ Tables créées avec succès")
            return True
        except Exception as e:
            print(f"  ❌ Erreur: {str(e)}")
            return False
    
    def add_missing_columns(self):
        """Ajoute les colonnes manquantes"""
        print("🔍 Vérification des colonnes manquantes...")
        
        changes = self.check_missing_columns()
        
        if not changes:
            print("  ✓ Toutes les colonnes existent")
            return True
        
        print(f"  📝 Modifications détectées dans {len(changes)} table(s):")
        
        for table_name, cols in changes.items():
            if cols['missing']:
                print(f"     {table_name}:")
                print(f"       Colonnes manquantes: {', '.join(cols['missing'])}")
            if cols['extra']:
                print(f"       Colonnes en trop: {', '.join(cols['extra'])}")
        
        # Ajouter les colonnes manquantes
        success = True
        for table_name, cols in changes.items():
            table = self.get_model_tables()[table_name]
            
            for col_name in cols['missing']:
                col = table.columns[col_name]
                try:
                    self.add_column(table_name, col)
                    print(f"  ✅ Colonne ajoutée: {table_name}.{col_name}")
                except Exception as e:
                    print(f"  ❌ Erreur pour {table_name}.{col_name}: {str(e)}")
                    success = False
        
        return success
    
    def add_column(self, table_name, column):
        """Ajoute une colonne à une table"""
        from sqlalchemy import VARCHAR, INTEGER, BOOLEAN, TIMESTAMP, TEXT
        from sqlalchemy.dialects.postgresql import UUID
        
        # Déterminer le type SQL
        col_type = str(column.type)
        if 'VARCHAR' in col_type:
            sql_type = f"VARCHAR({column.type.length})" if hasattr(column.type, 'length') else "VARCHAR(255)"
        elif 'INTEGER' in col_type or 'SERIAL' in col_type:
            sql_type = "INTEGER"
        elif 'BOOLEAN' in col_type:
            sql_type = "BOOLEAN"
        elif 'TIMESTAMP' in col_type or 'DATETIME' in col_type:
            sql_type = "TIMESTAMP"
        elif 'TEXT' in col_type:
            sql_type = "TEXT"
        else:
            sql_type = "VARCHAR(255)"
        
        # Construire la requête ALTER TABLE
        nullable = "NULL" if column.nullable else "NOT NULL"
        default = ""
        
        if column.default is not None:
            if hasattr(column.default, 'arg'):
                if callable(column.default.arg):
                    default = ""  # Skip function defaults
                else:
                    default = f"DEFAULT {column.default.arg}"
        
        sql = f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column.name} {sql_type} {nullable} {default}"
        
        with self.engine.connect() as conn:
            conn.execute(sql)
            conn.commit()
    
    def migrate(self):
        """Exécute toutes les migrations nécessaires"""
        print("=" * 60)
        print("🗄️  MIGRATION DE LA BASE DE DONNÉES")
        print("=" * 60)
        
        try:
            # 1. Créer les tables manquantes
            if not self.create_missing_tables():
                return False
            
            # 2. Ajouter les colonnes manquantes
            if not self.add_missing_columns():
                return False
            
            print("=" * 60)
            print("✅ MIGRATION TERMINÉE AVEC SUCCÈS")
            print("=" * 60)
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la migration: {str(e)}")
            return False

if __name__ == '__main__':
    migrator = DatabaseMigrator()
    migrator.migrate()
