#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from flask import Blueprint, request, jsonify
from backend import db
from backend.models.profile_option import ProfileOption
from backend.utils.auth import token_required, admin_required

bp = Blueprint('profile_options', __name__, url_prefix='/api/profile-options')

@bp.route('', methods=['GET'])
@token_required
def get_options(current_user):
    """Get all active profile options"""
    category = request.args.get('category')
    
    query = ProfileOption.query.filter_by(is_active=True)
    if category:
        query = query.filter_by(category=category)
    
    options = query.all()
    
    result = {}
    for option in options:
        if option.category not in result:
            result[option.category] = []
        result[option.category].append(option.to_dict())
    
    return jsonify(result)

@bp.route('', methods=['POST'])
@token_required
@admin_required
def create_option(current_user):
    """Admin: Create new profile option"""
    data = request.json
    
    option = ProfileOption(
        category=data['category'],
        value=data['value'],
        label=data['label']
    )
    
    db.session.add(option)
    db.session.commit()
    
    return jsonify(option.to_dict()), 201

@bp.route('/<int:option_id>', methods=['PUT'])
@token_required
@admin_required
def update_option(current_user, option_id):
    """Admin: Update profile option"""
    option = ProfileOption.query.get_or_404(option_id)
    data = request.json
    
    if 'label' in data:
        option.label = data['label']
    if 'is_active' in data:
        option.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify(option.to_dict())

@bp.route('/<int:option_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_option(current_user, option_id):
    """Admin: Deactivate profile option"""
    option = ProfileOption.query.get_or_404(option_id)
    option.is_active = False
    
    db.session.commit()
    
    return jsonify({'message': 'Option deactivated'})
