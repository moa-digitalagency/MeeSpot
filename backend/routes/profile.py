#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from flask import Blueprint, request, jsonify
from backend import db
from backend.utils.auth import token_required
from backend.utils.file_upload import save_upload_file, delete_upload_file
import bcrypt

bp = Blueprint('profile', __name__, url_prefix='/api/profile')

@bp.route('', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify(current_user.to_dict())

@bp.route('', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.json
    
    if 'bio' in data:
        current_user.bio = data['bio']
    if 'gender' in data:
        current_user.gender = data['gender']
    if 'sexual_orientation' in data:
        current_user.sexual_orientation = data['sexual_orientation']
    if 'religion' in data:
        current_user.religion = data['religion']
    if 'lgbtq_friendly' in data:
        current_user.lgbtq_friendly = data['lgbtq_friendly']
    if 'meeting_type' in data:
        current_user.meeting_type = data['meeting_type']
    if 'interests' in data:
        current_user.interests = data['interests']
    if 'alternative_mode' in data and current_user.subscription_tier in ['premium', 'platinum']:
        current_user.alternative_mode = data['alternative_mode']
    if 'alternative_name' in data and current_user.subscription_tier in ['premium', 'platinum']:
        current_user.alternative_name = data['alternative_name']
    if 'photo_consent_enabled' in data:
        current_user.photo_consent_enabled = data['photo_consent_enabled']
    if 'language' in data:
        current_user.language = data['language']
    if 'theme' in data:
        current_user.theme = data['theme']
    
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully', 'profile': current_user.to_dict()})

@bp.route('/photo', methods=['POST'])
@token_required
def upload_profile_photo(current_user):
    """Upload profile photo"""
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo file provided'}), 400
    
    file = request.files['photo']
    
    try:
        # Delete old photo if exists
        if current_user.photo_url:
            delete_upload_file(current_user.photo_url)
        
        # Save new photo
        photo_path = save_upload_file(file, 'photos/profile')
        current_user.photo_url = photo_path
        
        db.session.commit()
        return jsonify({
            'message': 'Profile photo uploaded successfully',
            'photo_url': photo_path
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to upload photo'}), 500

@bp.route('/gallery', methods=['POST'])
@token_required
def upload_gallery_photo(current_user):
    """Upload gallery photo"""
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo file provided'}), 400
    
    file = request.files['photo']
    
    try:
        # Save new photo
        photo_path = save_upload_file(file, 'photos/gallery')
        
        # Add to gallery
        gallery = current_user.gallery_photos or []
        gallery.append(photo_path)
        current_user.gallery_photos = gallery
        
        db.session.commit()
        return jsonify({
            'message': 'Gallery photo uploaded successfully',
            'photo_url': photo_path,
            'gallery': gallery
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to upload photo'}), 500

@bp.route('/gallery/<int:index>', methods=['DELETE'])
@token_required
def delete_gallery_photo(current_user, index):
    """Delete gallery photo by index"""
    gallery = current_user.gallery_photos or []
    
    if index < 0 or index >= len(gallery):
        return jsonify({'error': 'Invalid photo index'}), 400
    
    # Delete file
    photo_path = gallery[index]
    delete_upload_file(photo_path)
    
    # Remove from gallery
    gallery.pop(index)
    current_user.gallery_photos = gallery
    
    db.session.commit()
    return jsonify({
        'message': 'Gallery photo deleted successfully',
        'gallery': gallery
    })

@bp.route('/password', methods=['PUT'])
@token_required
def change_password(current_user):
    """Change user password"""
    data = request.json
    
    if not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Current password and new password are required'}), 400
    
    # Verify current password
    if not bcrypt.checkpw(data['current_password'].encode('utf-8'), current_user.password_hash.encode('utf-8')):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    # Update password
    new_password_hash = bcrypt.hashpw(data['new_password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    current_user.password_hash = new_password_hash
    
    db.session.commit()
    return jsonify({'message': 'Password changed successfully'})

@bp.route('/deactivate', methods=['POST'])
@token_required
def deactivate_account(current_user):
    """Deactivate user account"""
    data = request.json
    
    if not data.get('password'):
        return jsonify({'error': 'Password is required to deactivate account'}), 400
    
    # Verify password
    if not bcrypt.checkpw(data['password'].encode('utf-8'), current_user.password_hash.encode('utf-8')):
        return jsonify({'error': 'Password is incorrect'}), 401
    
    # Delete user's photos
    if current_user.photo_url:
        delete_upload_file(current_user.photo_url)
    
    for photo in (current_user.gallery_photos or []):
        delete_upload_file(photo)
    
    # Delete user account
    db.session.delete(current_user)
    db.session.commit()
    
    return jsonify({'message': 'Account deactivated successfully'})
