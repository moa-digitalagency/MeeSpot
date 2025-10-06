#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from flask import Blueprint, send_from_directory

bp = Blueprint('static_routes', __name__)

@bp.route('/')
def index():
    return send_from_directory('../static/pages', 'index.html')

@bp.route('/app')
def app():
    return send_from_directory('../static/pages', 'app.html')

@bp.route('/establishment')
def establishment():
    return send_from_directory('../static/pages', 'establishment.html')

@bp.route('/admin')
def admin():
    return send_from_directory('../static/pages', 'admin.html')

@bp.route('/uploads/<path:filename>')
def serve_upload(filename):
    response = send_from_directory('../uploads', filename)
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

@bp.route('/<path:path>')
def static_files(path):
    if path.endswith('.html'):
        return send_from_directory('../static/pages', path)
    return send_from_directory('../static', path)
