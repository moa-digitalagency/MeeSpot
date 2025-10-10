#
# MatchSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from flask import Blueprint, request, jsonify, send_file
from backend import db
from backend.models.user import User
from backend.models.report import Report
from backend.models.api_key import APIKey
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

@bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
@admin_required
def get_user_by_id(current_user, user_id):
    """Get detailed information for a single user"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

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
        if not filename.startswith('matchspot_backup_'):
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

@bp.route('/backup/delete/<filename>', methods=['DELETE'])
@token_required
@admin_required
def delete_backup(current_user, filename):
    """Supprime un backup"""
    try:
        # Validation stricte du nom de fichier
        if not filename.startswith('matchspot_backup_'):
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
        
        # Supprimer le fichier
        os.remove(backup_path)
        
        return jsonify({
            'success': True,
            'message': 'Backup supprimé avec succès'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/update', methods=['POST'])
@token_required
@admin_required
def update_from_github(current_user):
    """Mise à jour automatique depuis GitHub en un seul clic
    
    Note: Cette fonctionnalité ne fonctionne que sur VPS/serveur dédié.
    Elle est désactivée sur Replit car les opérations git sont bloquées pour des raisons de sécurité.
    """
    try:
        result = subprocess.run(
            [sys.executable, 'scripts/update_from_github.py'],
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes max
        )
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Mise à jour terminée avec succès',
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
            'message': 'Délai dépassé - la mise à jour prend trop de temps'
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

# ========== API KEYS MANAGEMENT ==========

@bp.route('/apikeys/list', methods=['GET'])
@token_required
@admin_required
def list_api_keys(current_user):
    """Liste toutes les clés API"""
    try:
        keys = APIKey.query.order_by(APIKey.created_at.desc()).all()
        return jsonify({
            'success': True,
            'keys': [key.to_dict_safe() for key in keys]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/apikeys/create', methods=['POST'])
@token_required
@admin_required
def create_api_key(current_user):
    """Crée une nouvelle clé API"""
    try:
        data = request.json
        
        if not data.get('name'):
            return jsonify({
                'success': False,
                'message': 'Le nom de la clé est requis'
            }), 400
        
        # Générer une nouvelle clé
        new_key = APIKey(
            key=APIKey.generate_key(),
            name=data['name'],
            description=data.get('description', ''),
            created_by=current_user.id
        )
        
        db.session.add(new_key)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Clé API créée avec succès',
            'key': new_key.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/apikeys/<int:key_id>/revoke', methods=['POST'])
@token_required
@admin_required
def revoke_api_key(current_user, key_id):
    """Révoque une clé API"""
    try:
        api_key = APIKey.query.get(key_id)
        
        if not api_key:
            return jsonify({
                'success': False,
                'message': 'Clé API introuvable'
            }), 404
        
        api_key.is_active = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Clé API révoquée avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/apikeys/<int:key_id>/activate', methods=['POST'])
@token_required
@admin_required
def activate_api_key(current_user, key_id):
    """Réactive une clé API"""
    try:
        api_key = APIKey.query.get(key_id)
        
        if not api_key:
            return jsonify({
                'success': False,
                'message': 'Clé API introuvable'
            }), 404
        
        api_key.is_active = True
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Clé API réactivée avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/apikeys/<int:key_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_api_key(current_user, key_id):
    """Supprime définitivement une clé API"""
    try:
        api_key = APIKey.query.get(key_id)
        
        if not api_key:
            return jsonify({
                'success': False,
                'message': 'Clé API introuvable'
            }), 404
        
        db.session.delete(api_key)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Clé API supprimée définitivement'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# ========== SUBSCRIPTION PLANS MANAGEMENT ==========

@bp.route("/plans", methods=["GET"])
@token_required
@admin_required
def get_all_plans(current_user):
    """Get all subscription plans"""
    from backend.models.subscription_plan import SubscriptionPlan
    plans = SubscriptionPlan.query.all()
    return jsonify([p.to_dict() for p in plans])

@bp.route("/plans", methods=["POST"])
@token_required
@admin_required
def create_plan(current_user):
    """Create a new subscription plan"""
    from backend.models.subscription_plan import SubscriptionPlan
    data = request.json
    
    if not all(k in data for k in ["role", "name", "description", "price", "rooms_per_day"]):
        return jsonify({"error": "Missing required fields"}), 400
    
    plan = SubscriptionPlan(
        role=data["role"],
        name=data["name"],
        description=data["description"],
        price=data["price"],
        rooms_per_day=data["rooms_per_day"],
        is_active=True
    )
    
    db.session.add(plan)
    db.session.commit()
    
    return jsonify({
        "message": "Plan created successfully",
        "plan": plan.to_dict()
    })

@bp.route("/plans/<int:plan_id>", methods=["PUT"])
@token_required
@admin_required
def update_plan(current_user, plan_id):
    """Update a subscription plan"""
    from backend.models.subscription_plan import SubscriptionPlan
    plan = SubscriptionPlan.query.get_or_404(plan_id)
    data = request.json
    
    if "name" in data:
        plan.name = data["name"]
    if "description" in data:
        plan.description = data["description"]
    if "price" in data:
        plan.price = data["price"]
    if "rooms_per_day" in data:
        plan.rooms_per_day = data["rooms_per_day"]
    
    db.session.commit()
    
    return jsonify({
        "message": "Plan updated successfully",
        "plan": plan.to_dict()
    })

@bp.route("/plans/<int:plan_id>/toggle", methods=["POST"])
@token_required
@admin_required
def toggle_plan_active(current_user, plan_id):
    """Toggle plan active status"""
    from backend.models.subscription_plan import SubscriptionPlan
    plan = SubscriptionPlan.query.get_or_404(plan_id)
    data = request.json
    
    plan.is_active = data.get("is_active", not plan.is_active)
    db.session.commit()
    
    status = "activated" if plan.is_active else "deactivated"
    return jsonify({
        "message": f"Plan {status}",
        "plan": plan.to_dict()
    })

