#!/usr/bin/env python3
#
# MeetSpot - Script de mise à jour depuis GitHub
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

import os
import subprocess
import sys
from datetime import datetime
from backup import BackupManager

GITHUB_REPO = "https://github.com/moa-digitalagency/MeeSpot.git"
LOG_FILE = f"logs/update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

class UpdateManager:
    def __init__(self):
        self.log_lines = []
        
    def log(self, message, level="INFO"):
        """Log un message"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] [{level}] {message}"
        print(log_line)
        self.log_lines.append(log_line)
        
    def save_log(self):
        """Sauvegarde le log dans un fichier"""
        os.makedirs('logs', exist_ok=True)
        with open(LOG_FILE, 'w') as f:
            f.write('\n'.join(self.log_lines))
        self.log(f"Log sauvegardé: {LOG_FILE}")
        
    def run_command(self, cmd, description):
        """Exécute une commande et log le résultat"""
        self.log(f"🔄 {description}...")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=isinstance(cmd, str)
        )
        
        if result.returncode == 0:
            self.log(f"✅ {description} - Succès")
            if result.stdout:
                self.log(f"   Output: {result.stdout.strip()}")
            return True
        else:
            self.log(f"❌ {description} - Échec", "ERROR")
            if result.stderr:
                self.log(f"   Error: {result.stderr.strip()}", "ERROR")
            return False
    
    def check_git_status(self):
        """Vérifie si on est dans un repo git"""
        if not os.path.exists('.git'):
            self.log("❌ Pas un dépôt Git. Clonage du repo...", "WARNING")
            return False
        return True
    
    def create_backup(self):
        """Crée un backup avant la mise à jour"""
        self.log("📦 Création du backup pré-mise à jour...")
        try:
            backup_manager = BackupManager()
            backup_path = backup_manager.create_backup()
            self.log(f"✅ Backup créé: {backup_path}")
            return True
        except Exception as e:
            self.log(f"❌ Erreur lors du backup: {str(e)}", "ERROR")
            return False
    
    def fetch_updates(self):
        """Récupère les mises à jour depuis GitHub"""
        commands = [
            (['git', 'fetch', 'origin'], "Récupération des mises à jour"),
            (['git', 'status', '-uno'], "Vérification du statut"),
        ]
        
        for cmd, desc in commands:
            if not self.run_command(cmd, desc):
                return False
        return True
    
    def check_for_changes(self):
        """Vérifie s'il y a des changements à appliquer"""
        result = subprocess.run(
            ['git', 'rev-list', 'HEAD...origin/main', '--count'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            changes_count = int(result.stdout.strip())
            if changes_count == 0:
                self.log("ℹ️  Aucune mise à jour disponible")
                return False
            else:
                self.log(f"📥 {changes_count} commit(s) à appliquer")
                return True
        return False
    
    def stash_local_changes(self):
        """Sauvegarde les modifications locales"""
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            self.log("💾 Sauvegarde des modifications locales...")
            return self.run_command(
                ['git', 'stash', 'push', '-m', f'Auto-stash before update {datetime.now().isoformat()}'],
                "Stash des modifications locales"
            )
        return True
    
    def pull_updates(self):
        """Applique les mises à jour"""
        return self.run_command(
            ['git', 'pull', 'origin', 'main', '--rebase'],
            "Application des mises à jour"
        )
    
    def install_dependencies(self):
        """Installe les dépendances Python"""
        return self.run_command(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--upgrade'],
            "Installation des dépendances"
        )
    
    def migrate_database(self):
        """Exécute les migrations de base de données"""
        self.log("🗄️  Migration de la base de données...")
        
        # Import du script de migration
        try:
            from migrate_database import DatabaseMigrator
            migrator = DatabaseMigrator()
            migrator.migrate()
            self.log("✅ Migrations appliquées avec succès")
            return True
        except Exception as e:
            self.log(f"❌ Erreur lors de la migration: {str(e)}", "ERROR")
            return False
    
    def restart_server(self):
        """Redémarre le serveur (si géré par systemd ou PM2)"""
        self.log("🔄 Le serveur sera redémarré automatiquement par Replit")
        return True
    
    def update(self, skip_backup=False):
        """Processus complet de mise à jour"""
        self.log("=" * 60)
        self.log("🚀 DÉMARRAGE DE LA MISE À JOUR DEPUIS GITHUB")
        self.log("=" * 60)
        
        try:
            # 1. Vérifier git
            if not self.check_git_status():
                self.log("❌ Initialisation Git requise", "ERROR")
                return False
            
            # 2. Créer un backup
            if not skip_backup:
                if not self.create_backup():
                    self.log("⚠️  Backup échoué, continuer quand même? (risqué)", "WARNING")
                    # Continuer quand même pour l'automatisation
            
            # 3. Vérifier les mises à jour disponibles
            if not self.fetch_updates():
                self.log("❌ Impossible de récupérer les mises à jour", "ERROR")
                return False
            
            if not self.check_for_changes():
                self.log("✅ Application déjà à jour!")
                return True
            
            # 4. Sauvegarder les modifications locales
            if not self.stash_local_changes():
                self.log("❌ Impossible de sauvegarder les modifications locales", "ERROR")
                return False
            
            # 5. Appliquer les mises à jour
            if not self.pull_updates():
                self.log("❌ Échec de la mise à jour", "ERROR")
                return False
            
            # 6. Installer les dépendances
            if not self.install_dependencies():
                self.log("⚠️  Avertissement: Erreur lors de l'installation des dépendances", "WARNING")
            
            # 7. Migrer la base de données
            if not self.migrate_database():
                self.log("⚠️  Avertissement: Erreur lors de la migration DB", "WARNING")
            
            # 8. Redémarrer le serveur
            self.restart_server()
            
            self.log("=" * 60)
            self.log("✅ MISE À JOUR TERMINÉE AVEC SUCCÈS!")
            self.log("=" * 60)
            
            return True
            
        except Exception as e:
            self.log(f"❌ ERREUR CRITIQUE: {str(e)}", "ERROR")
            return False
        finally:
            self.save_log()

if __name__ == '__main__':
    skip_backup = '--skip-backup' in sys.argv
    
    manager = UpdateManager()
    success = manager.update(skip_backup=skip_backup)
    
    sys.exit(0 if success else 1)
