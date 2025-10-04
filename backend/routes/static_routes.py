from flask import Blueprint, send_from_directory

bp = Blueprint('static_routes', __name__)

@bp.route('/')
def index():
    return send_from_directory('../static/pages', 'index.html')

@bp.route('/<path:path>')
def static_files(path):
    if path.endswith('.html'):
        return send_from_directory('../static/pages', path)
    return send_from_directory('../static', path)
