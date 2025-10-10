#!/usr/bin/env python3
#
# MatchSpot - Script de restauration
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

import os
import subprocess
import shutil
import tarfile
import json

class RestoreManager:
    def __init__(self, backup_file):
        self.backup_file = backup_file
        self.temp_dir = 'temp_restore'
        
    def restore(self):
        """Restaure un backup complet"""
        print(f"🔄 Démarrage de la restauration: {self.backup_file}")
        
        if not os.path.exists(self.backup_file):
            raise Exception(f"Fichier de backup introuvable: {self.backup_file}")
        
        try:
            # 1. Extraire l'archive
            self.extract_backup()
            
            # 2. Lire les métadonnées
            self.read_metadata()
            
            # 3. Restaurer la base de données
            self.restore_database()
            
            # 4. Restaurer les fichiers uploadés
            self.restore_uploads()
            
            # 5. Restaurer la configuration
            self.restore_config()
            
            # 6. Nettoyer
            self.cleanup()
            
            print("✅ Restauration terminée avec succès!")
            
        except Exception as e:
            print(f"❌ Erreur lors de la restauration: {str(e)}")
            self.cleanup()
            raise
    
    def extract_backup(self):
        """Extrait l'archive de backup de manière sécurisée"""
        print("📦 Extraction de l'archive...")
        
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Extraction sécurisée avec validation des chemins
        with tarfile.open(self.backup_file, 'r:gz') as tar:
            # Vérifier tous les membres avant extraction
            for member in tar.getmembers():
                # Bloquer les chemins absolus et les remontées de répertoire
                if member.name.startswith('/') or '..' in member.name:
                    raise Exception(f"Chemin dangereux détecté dans l'archive: {member.name}")
                
                # Bloquer les liens symboliques
                if member.issym() or member.islnk():
                    raise Exception(f"Lien symbolique détecté dans l'archive: {member.name}")
            
            # Extraction sécurisée
            tar.extractall(self.temp_dir, filter='data')
        
        # Trouver le dossier extrait
        extracted_dirs = os.listdir(self.temp_dir)
        if len(extracted_dirs) == 1:
            self.backup_content = os.path.join(self.temp_dir, extracted_dirs[0])
        else:
            self.backup_content = self.temp_dir
        
        print("  ✓ Archive extraite")
    
    def read_metadata(self):
        """Lit les métadonnées du backup"""
        metadata_file = os.path.join(self.backup_content, 'metadata.json')
        
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                self.metadata = json.load(f)
            print(f"  ℹ️  Backup du {self.metadata['date']}")
        else:
            self.metadata = {}
    
    def restore_database(self):
        """Restaure la base de données"""
        print("🗄️  Restauration de la base de données...")
        
        db_file = os.path.join(self.backup_content, 'database.dump')
        if not os.path.exists(db_file):
            raise Exception("Fichier de base de données introuvable dans le backup")
        
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            raise Exception("DATABASE_URL non définie")
        
        # Avertissement
        print("  ⚠️  ATTENTION: Cette opération va effacer les données actuelles!")
        
        # Restaurer avec pg_restore
        cmd = [
            'pg_restore',
            '-d', db_url,
            '--clean',  # Nettoie d'abord
            '--if-exists',
            '--no-owner',
            '--no-acl',
            '-v',  # Verbose pour debug
            db_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Vérifier les erreurs critiques
        if result.returncode != 0:
            # Certains avertissements sont normaux (tables already exists)
            stderr_lower = result.stderr.lower()
            if any(error in stderr_lower for error in ['fatal', 'error:', 'cannot drop', 'permission denied']):
                # Filtrer les avertissements bénins
                if not ('already exists' in stderr_lower or 'no matching tables' in stderr_lower):
                    raise Exception(f"Erreur critique lors de la restauration: {result.stderr}")
            print(f"  ⚠️  Avertissements: {result.stderr}")
        
        print("  ✓ Base de données restaurée")
    
    def restore_uploads(self):
        """Restaure les fichiers uploadés"""
        print("📁 Restauration des fichiers uploadés...")
        
        source_dir = os.path.join(self.backup_content, 'uploads')
        dest_dir = 'uploads'
        
        if os.path.exists(source_dir):
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            shutil.copytree(source_dir, dest_dir)
            
            file_count = sum(len(files) for _, _, files in os.walk(dest_dir))
            print(f"  ✓ {file_count} fichiers restaurés")
        else:
            print("  ⚠️  Aucun fichier uploadé dans le backup")
    
    def restore_config(self):
        """Restaure les fichiers de configuration"""
        print("⚙️  Restauration de la configuration...")
        
        config_dir = os.path.join(self.backup_content, 'config')
        
        if os.path.exists(config_dir):
            # Ne pas restaurer .env automatiquement pour éviter d'écraser des secrets
            config_files = [f for f in os.listdir(config_dir) if f != '.env']
            
            restored = 0
            for file in config_files:
                source = os.path.join(config_dir, file)
                dest = file
                
                # Backup du fichier actuel si il existe
                if os.path.exists(dest):
                    shutil.copy2(dest, f"{dest}.backup")
                
                shutil.copy2(source, dest)
                restored += 1
            
            print(f"  ✓ {restored} fichiers de configuration restaurés")
            print("  ℹ️  .env non restauré (vérifier manuellement dans backups/config/)")
        else:
            print("  ⚠️  Aucune configuration dans le backup")
    
    def cleanup(self):
        """Nettoie les fichiers temporaires"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python restore.py <backup_file.tar.gz>")
        sys.exit(1)
    
    manager = RestoreManager(sys.argv[1])
    manager.restore()
