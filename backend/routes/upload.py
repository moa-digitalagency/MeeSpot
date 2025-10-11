#
# MatchSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from flask import Blueprint, request, jsonify
from backend.utils.file_upload import save_upload_file, delete_upload_file
from backend.utils.auth import token_required
from functools import wraps
import jwt
import os

bp = Blueprint('upload', __name__, url_prefix='/api/upload')

def optional_auth(f):
    """Decorator that validates token if present, but doesn't require it"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        current_user = None
        
        if token and token.startswith('Bearer '):
            try:
                token = token.split(' ')[1]
                data = jwt.decode(token, os.environ.get('SECRET_KEY') or os.environ.get('SESSION_SECRET'), algorithms=['HS256'])
                from backend.models.user import User
                current_user = User.query.get(data['user_id'])
            except:
                pass
        
        return f(current_user, *args, **kwargs)
    return decorated

@bp.route('/image', methods=['POST'])
@optional_auth
def upload_image(current_user):
    """Unified image upload endpoint for all types (profile, gallery, verification, chat, establishment)
    
    Authentication: Optional - works both authenticated and unauthenticated
    - Authenticated: For logged-in users (verification, profile updates, etc.)
    - Unauthenticated: For registration and establishment onboarding
    """
    
    if 'photo' not in request.files:
        return jsonify({'success': False, 'message': 'No photo file provided'}), 400
    
    file = request.files['photo']
    upload_type = request.form.get('type', 'profile')
    
    valid_types = ['profile', 'gallery', 'verification', 'chat', 'establishment']
    if upload_type not in valid_types:
        return jsonify({'success': False, 'message': f'Invalid upload type. Must be one of: {", ".join(valid_types)}'}), 400
    
    try:
        photo_path = save_upload_file(file, f'photos/{upload_type}')
        
        return jsonify({
            'success': True,
            'url': photo_path,
            'message': f'{upload_type.capitalize()} photo uploaded successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to upload photo'}), 500

@bp.route('/image', methods=['DELETE'])
@token_required
def delete_image(current_user):
    """Delete an uploaded image (requires authentication)"""
    data = request.json
    
    if not data or 'url' not in data:
        return jsonify({'success': False, 'message': 'Image URL is required'}), 400
    
    try:
        delete_upload_file(data['url'])
        return jsonify({
            'success': True,
            'message': 'Image deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to delete image'}), 500

@bp.route('/images/multiple', methods=['POST'])
@optional_auth
def upload_multiple_images(current_user):
    """Upload multiple images at once (for gallery)
    
    Authentication: Optional - works both authenticated and unauthenticated
    """
    
    if 'photos' not in request.files:
        return jsonify({'success': False, 'message': 'No photo files provided'}), 400
    
    files = request.files.getlist('photos')
    upload_type = request.form.get('type', 'gallery')
    
    if not files:
        return jsonify({'success': False, 'message': 'No photo files provided'}), 400
    
    uploaded_urls = []
    errors = []
    
    for file in files:
        if file and file.filename:
            try:
                photo_path = save_upload_file(file, f'photos/{upload_type}')
                uploaded_urls.append(photo_path)
            except ValueError as e:
                errors.append(f'{file.filename}: {str(e)}')
            except Exception as e:
                errors.append(f'{file.filename}: Upload failed')
    
    if not uploaded_urls and errors:
        return jsonify({
            'success': False,
            'message': 'All uploads failed',
            'errors': errors
        }), 400
    
    response = {
        'success': True,
        'urls': uploaded_urls,
        'message': f'{len(uploaded_urls)} photo(s) uploaded successfully'
    }
    
    if errors:
        response['partial'] = True
        response['errors'] = errors
        response['message'] = f'{len(uploaded_urls)} uploaded, {len(errors)} failed'
    
    return jsonify(response), 200
