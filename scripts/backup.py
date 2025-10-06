#!/usr/bin/env python3
#
# MeetSpot - Script de backup complet
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

import os
import subprocess
import shutil
import tarfile
from datetime import datetime
import json

class BackupManager:
    def __init__(self):
        self.backup_dir = 'backups'
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_name = f'meetspot_backup_{self.timestamp}'
        self.backup_path = os.path.join(self.backup_dir, self.backup_name)
        
    def create_backup(self):
        """Crée un backup complet de l'application"""
        print(f"🔄 Démarrage du backup: {self.backup_name}")
        
        # Créer le dossier de backup
        os.makedirs(self.backup_path, exist_ok=True)
        
        try:
            # 1. Backup de la base de données
            self.backup_database()
            
            # 2. Backup des fichiers uploadés
            self.backup_uploads()
            
            # 3. Backup des configurations
            self.backup_config()
            
            # 4. Créer un fichier de métadonnées
            self.create_metadata()
            
            # 5. Compresser le backup
            archive_path = self.compress_backup()
            
            # 6. Nettoyer les anciens backups
            self.cleanup_old_backups()
            
            print(f"✅ Backup créé avec succès: {archive_path}")
            return archive_path
            
        except Exception as e:
            print(f"❌ Erreur lors du backup: {str(e)}")
            # Nettoyer en cas d'erreur
            if os.path.exists(self.backup_path):
                shutil.rmtree(self.backup_path)
            raise
    
    def backup_database(self):
        """Backup de la base de données PostgreSQL"""
        print("📦 Backup de la base de données...")
        
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            raise Exception("DATABASE_URL non définie")
        
        db_backup_file = os.path.join(self.backup_path, 'database.dump')
        
        # Utiliser pg_dump avec format custom (meilleur pour les restaurations)
        cmd = [
            'pg_dump',
            '-F', 'c',  # Format custom
            '-f', db_backup_file,
            db_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Erreur pg_dump: {result.stderr}")
        
        print(f"  ✓ Base de données sauvegardée ({os.path.getsize(db_backup_file)} bytes)")
    
    def backup_uploads(self):
        """Backup des fichiers uploadés"""
        print("📦 Backup des fichiers uploadés...")
        
        uploads_dir = 'uploads'
        if os.path.exists(uploads_dir):
            dest_dir = os.path.join(self.backup_path, 'uploads')
            shutil.copytree(uploads_dir, dest_dir)
            
            # Compter les fichiers
            file_count = sum(len(files) for _, _, files in os.walk(dest_dir))
            print(f"  ✓ {file_count} fichiers sauvegardés")
        else:
            print("  ⚠ Aucun dossier uploads trouvé")
    
    def backup_config(self):
        """Backup des fichiers de configuration"""
        print("📦 Backup de la configuration...")
        
        config_files = [
            '.env',
            '.encryption_key',
            'requirements.txt',
            'main.py',
            'replit.md'
        ]
        
        config_dir = os.path.join(self.backup_path, 'config')
        os.makedirs(config_dir, exist_ok=True)
        
        backed_up = 0
        for file in config_files:
            if os.path.exists(file):
                shutil.copy2(file, config_dir)
                backed_up += 1
        
        print(f"  ✓ {backed_up} fichiers de configuration sauvegardés")
    
    def create_metadata(self):
        """Crée un fichier de métadonnées pour le backup"""
        metadata = {
            'backup_name': self.backup_name,
            'timestamp': self.timestamp,
            'date': datetime.now().isoformat(),
            'app_version': '1.0.0',
            'python_version': subprocess.run(['python', '--version'], 
                                            capture_output=True, text=True).stdout.strip(),
            'database_url': os.environ.get('DATABASE_URL', 'Not set').split('@')[-1]  # Sans credentials
        }
        
        metadata_file = os.path.join(self.backup_path, 'metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"  ✓ Métadonnées créées")
    
    def compress_backup(self):
        """Compresse le backup en .tar.gz"""
        print("🗜️  Compression du backup...")
        
        archive_name = f"{self.backup_name}.tar.gz"
        archive_path = os.path.join(self.backup_dir, archive_name)
        
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(self.backup_path, arcname=self.backup_name)
        
        # Supprimer le dossier non compressé
        shutil.rmtree(self.backup_path)
        
        size_mb = os.path.getsize(archive_path) / (1024 * 1024)
        print(f"  ✓ Archive créée: {archive_name} ({size_mb:.2f} MB)")
        
        return archive_path
    
    def cleanup_old_backups(self, keep_count=7):
        """Garde seulement les N derniers backups"""
        backups = []
        for file in os.listdir(self.backup_dir):
            if file.startswith('meetspot_backup_') and file.endswith('.tar.gz'):
                file_path = os.path.join(self.backup_dir, file)
                backups.append((file_path, os.path.getmtime(file_path)))
        
        # Trier par date de modification
        backups.sort(key=lambda x: x[1], reverse=True)
        
        # Supprimer les anciens
        for backup_path, _ in backups[keep_count:]:
            os.remove(backup_path)
            print(f"  🗑️  Ancien backup supprimé: {os.path.basename(backup_path)}")

    @staticmethod
    def list_backups():
        """Liste tous les backups disponibles"""
        backup_dir = 'backups'
        backups = []
        
        if os.path.exists(backup_dir):
            for file in os.listdir(backup_dir):
                if file.startswith('meetspot_backup_') and file.endswith('.tar.gz'):
                    file_path = os.path.join(backup_dir, file)
                    size = os.path.getsize(file_path)
                    mtime = os.path.getmtime(file_path)
                    
                    backups.append({
                        'name': file,
                        'path': file_path,
                        'size': size,
                        'size_mb': round(size / (1024 * 1024), 2),
                        'date': datetime.fromtimestamp(mtime).isoformat()
                    })
        
        # Trier par date décroissante
        backups.sort(key=lambda x: x['date'], reverse=True)
        return backups

if __name__ == '__main__':
    manager = BackupManager()
    manager.create_backup()
