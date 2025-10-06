#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from flask import Blueprint, request, jsonify, send_file
from backend import db
from backend.models.user import User
from backend.models.report import Report
from backend.utils.auth import token_required, admin_required
import subprocess
import os
import sys

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@bp.route('/users', methods=['GET'])
@token_required
@admin_required
def get_users(current_user):
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@bp.route('/reports', methods=['GET'])
@token_required
@admin_required
def get_reports(current_user):
    reports = Report.query.all()
    return jsonify([report.to_dict() for report in reports])

@bp.route('/reports', methods=['POST'])
@token_required
def create_report(current_user):
    data = request.json
    report = Report(
        reporter_id=current_user.id,
        reported_user_id=data.get('reported_user_id'),
        room_id=data.get('room_id'),
        reason=data['reason']
    )
    db.session.add(report)
    db.session.commit()
    
    return jsonify({'message': 'Report submitted successfully'})

# ========== BACKUP & UPDATE MANAGEMENT ==========

@bp.route('/backup/create', methods=['POST'])
@token_required
@admin_required
def create_backup(current_user):
    """Crée un backup complet de l'application"""
    try:
        result = subprocess.run(
            [sys.executable, 'scripts/backup.py'],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes max
        )
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Backup créé avec succès',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Erreur lors du backup',
                'error': result.stderr
            }), 500
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'message': 'Timeout lors du backup'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/backup/list', methods=['GET'])
@token_required
@admin_required
def list_backups(current_user):
    """Liste tous les backups disponibles"""
    try:
        sys.path.insert(0, 'scripts')
        from backup import BackupManager
        
        backups = BackupManager.list_backups()
        return jsonify({
            'success': True,
            'backups': backups
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/backup/download/<filename>', methods=['GET'])
@token_required
@admin_required
def download_backup(current_user, filename):
    """Télécharge un backup"""
    try:
        # Validation stricte du nom de fichier
        if not filename.startswith('meetspot_backup_'):
            return jsonify({
                'success': False,
                'message': 'Nom de fichier invalide'
            }), 400
        
        if not filename.endswith('.tar.gz'):
            return jsonify({
                'success': False,
                'message': 'Extension de fichier invalide'
            }), 400
        
        # Bloquer les caractères dangereux
        if '..' in filename or '/' in filename or '\\' in filename:
            return jsonify({
                'success': False,
                'message': 'Caractères non autorisés dans le nom de fichier'
            }), 400
        
        backup_path = os.path.join('backups', filename)
        
        # Vérifier que le chemin réel est bien dans le dossier backups
        real_backup_path = os.path.realpath(backup_path)
        real_backups_dir = os.path.realpath('backups')
        
        if not real_backup_path.startswith(real_backups_dir):
            return jsonify({
                'success': False,
                'message': 'Accès refusé'
            }), 403
        
        if not os.path.exists(backup_path):
            return jsonify({
                'success': False,
                'message': 'Backup introuvable'
            }), 404
        
        return send_file(
            backup_path,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/backup/restore', methods=['POST'])
@token_required
@admin_required
def restore_backup(current_user):
    """Restaure un backup"""
    data = request.json
    backup_file = data.get('backup_file')
    
    if not backup_file:
        return jsonify({
            'success': False,
            'message': 'Fichier de backup requis'
        }), 400
    
    backup_path = os.path.join('backups', backup_file)
    
    if not os.path.exists(backup_path):
        return jsonify({
            'success': False,
            'message': 'Backup introuvable'
        }), 404
    
    try:
        result = subprocess.run(
            [sys.executable, 'scripts/restore.py', backup_path],
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes max
        )
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Backup restauré avec succès',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Erreur lors de la restauration',
                'error': result.stderr
            }), 500
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'message': 'Timeout lors de la restauration'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/update/check', methods=['GET'])
@token_required
@admin_required
def check_updates(current_user):
    """Vérifie si des mises à jour sont disponibles depuis GitHub"""
    try:
        # Fetch depuis GitHub
        result = subprocess.run(
            ['git', 'fetch', 'origin'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return jsonify({
                'success': False,
                'message': 'Erreur lors de la vérification',
                'error': result.stderr
            }), 500
        
        # Vérifier le nombre de commits en retard
        result = subprocess.run(
            ['git', 'rev-list', 'HEAD...origin/main', '--count'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            commits_behind = int(result.stdout.strip())
            
            # Récupérer les derniers commits
            log_result = subprocess.run(
                ['git', 'log', 'HEAD..origin/main', '--oneline', '-n', '10'],
                capture_output=True,
                text=True
            )
            
            return jsonify({
                'success': True,
                'updates_available': commits_behind > 0,
                'commits_behind': commits_behind,
                'recent_commits': log_result.stdout.strip().split('\n') if log_result.stdout else []
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Erreur lors de la vérification',
                'error': result.stderr
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/update/apply', methods=['POST'])
@token_required
@admin_required
def apply_updates(current_user):
    """Applique les mises à jour depuis GitHub"""
    data = request.json
    skip_backup = data.get('skip_backup', False)
    
    try:
        cmd = [sys.executable, 'scripts/update_from_github.py']
        if skip_backup:
            cmd.append('--skip-backup')
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes max
        )
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Mise à jour appliquée avec succès',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Erreur lors de la mise à jour',
                'error': result.stderr,
                'output': result.stdout
            }), 500
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'message': 'Timeout lors de la mise à jour'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/database/migrate', methods=['POST'])
@token_required
@admin_required
def migrate_database(current_user):
    """Exécute les migrations de base de données"""
    try:
        result = subprocess.run(
            [sys.executable, 'scripts/migrate_database.py'],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes max
        )
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Migration réussie',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Erreur lors de la migration',
                'error': result.stderr,
                'output': result.stdout
            }), 500
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'message': 'Timeout lors de la migration'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/logs/list', methods=['GET'])
@token_required
@admin_required
def list_logs(current_user):
    """Liste les logs de mise à jour disponibles"""
    try:
        logs = []
        log_dir = 'logs'
        
        if os.path.exists(log_dir):
            for file in os.listdir(log_dir):
                if file.startswith('update_') and file.endswith('.log'):
                    file_path = os.path.join(log_dir, file)
                    logs.append({
                        'name': file,
                        'path': file_path,
                        'size': os.path.getsize(file_path),
                        'date': os.path.getmtime(file_path)
                    })
        
        logs.sort(key=lambda x: x['date'], reverse=True)
        return jsonify({
            'success': True,
            'logs': logs
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/logs/view/<filename>', methods=['GET'])
@token_required
@admin_required
def view_log(current_user, filename):
    """Affiche le contenu d'un log"""
    try:
        log_path = os.path.join('logs', filename)
        
        if not os.path.exists(log_path):
            return jsonify({
                'success': False,
                'message': 'Log introuvable'
            }), 404
        
        with open(log_path, 'r') as f:
            content = f.read()
        
        return jsonify({
            'success': True,
            'content': content
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
