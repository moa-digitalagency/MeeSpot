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

bp = Blueprint('profile', __name__, url_prefix='/api/profile')

@bp.route('', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify(current_user.to_dict())

@bp.route('', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.json
    
    if 'name' in data:
        current_user.name = data['name']
    if 'gender' in data:
        current_user.gender = data['gender']
    if 'orientation' in data:
        current_user.orientation = data['orientation']
    if 'age' in data:
        current_user.age = data['age']
    if 'bio' in data:
        current_user.bio = data['bio']
    if 'photo_url' in data:
        current_user.photo_url = data['photo_url']
    if 'alternative_mode' in data and current_user.subscription_tier in ['premium', 'platinum']:
        current_user.alternative_mode = data['alternative_mode']
    if 'alternative_name' in data and current_user.subscription_tier in ['premium', 'platinum']:
        current_user.alternative_name = data['alternative_name']
    
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'})
