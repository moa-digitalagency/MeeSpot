#
# MatchSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from flask import Blueprint, request, jsonify
import os
import base64
import uuid

bp = Blueprint('upload', __name__, url_prefix='/api/upload')

@bp.route('/image', methods=['POST'])
def upload_image():
    """Upload a single image and return its URL"""
    data = request.json
    
    if not data or not data.get('image'):
        return jsonify({'message': 'No image provided'}), 400
    
    image_type = data.get('type', 'profile')  # 'profile' or 'gallery'
    
    try:
        # Decode base64 image
        image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
        image_bytes = base64.b64decode(image_data)
        
        # Security: Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if len(image_bytes) > max_size:
            return jsonify({'message': 'Image too large (max 10MB)'}), 400
        
        # Security: Basic image validation (check for JPEG/PNG magic bytes)
        if not (image_bytes.startswith(b'\xff\xd8\xff') or  # JPEG
                image_bytes.startswith(b'\x89PNG')):         # PNG
            return jsonify({'message': 'Only JPEG and PNG images are allowed'}), 400
        
        # Determine upload directory
        if image_type == 'profile':
            upload_dir = 'static/uploads/profiles'
        else:
            upload_dir = 'static/uploads/gallery'
        
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        filename = f"{image_type}_{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(upload_dir, filename)
        
        # Save image
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        # Return URL
        url = f'/uploads/{image_type}s/{filename}' if image_type == 'profile' else f'/uploads/gallery/{filename}'
        
        return jsonify({
            'success': True,
            'url': url
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error uploading image: {str(e)}'
        }), 500
