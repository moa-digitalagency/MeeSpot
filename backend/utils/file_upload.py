#
# MatchSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_upload_file(file: FileStorage, subfolder='photos'):
    """Save uploaded file and return its path"""
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        raise ValueError('File type not allowed. Please upload PNG, JPG, JPEG, GIF, or WEBP images.')
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise ValueError('File size exceeds 10MB limit.')
    
    # Create upload directory if it doesn't exist
    upload_path = os.path.join(UPLOAD_FOLDER, subfolder)
    os.makedirs(upload_path, exist_ok=True)
    
    # Generate unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join(upload_path, unique_filename)
    
    # Save file
    file.save(file_path)
    
    # Return relative path for storage in database (strip 'static/' prefix)
    relative_path = file_path.replace('static/', '', 1)
    return f"/{relative_path}"

def save_chat_photo(file: FileStorage):
    """Save chat photo and return its path"""
    return save_upload_file(file, subfolder='chat_photos')

def delete_upload_file(file_path):
    """Delete uploaded file"""
    if file_path:
        # Convert URL path back to file system path
        # /uploads/photos/profile/uuid.ext -> static/uploads/photos/profile/uuid.ext
        fs_path = file_path.lstrip('/')
        if not fs_path.startswith('static/'):
            fs_path = f"static/{fs_path}"
        
        if os.path.exists(fs_path):
            try:
                os.remove(fs_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
