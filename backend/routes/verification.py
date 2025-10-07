#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from flask import Blueprint, request, jsonify
from backend import db
from backend.models.verification_request import VerificationRequest
from backend.models.user import User
from backend.utils.auth import token_required
from datetime import datetime
import os
import base64
import uuid

bp = Blueprint('verification', __name__, url_prefix='/api/verification')

@bp.route('/request', methods=['POST'])
@token_required
def request_verification(current_user):
    """User submits a verification request with photo"""
    if current_user.role != 'user':
        return jsonify({'message': 'Only users can request verification'}), 403
    
    # Check if already has pending request
    existing = VerificationRequest.query.filter_by(
        user_id=current_user.id,
        status='pending'
    ).first()
    
    if existing:
        return jsonify({'message': 'You already have a pending verification request'}), 400
    
    data = request.json
    if not data or 'photo' not in data:
        return jsonify({'message': 'Photo is required'}), 400
    
    # Save photo (base64 to file)
    try:
        photo_data = data['photo'].split(',')[1] if ',' in data['photo'] else data['photo']
        photo_bytes = base64.b64decode(photo_data)
        
        # Create uploads directory if it doesn't exist
        upload_dir = 'static/uploads/verifications'
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        filename = f"{current_user.id}_{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(upload_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(photo_bytes)
        
        photo_url = f'/uploads/verifications/{filename}'
        
    except Exception as e:
        return jsonify({'message': f'Error saving photo: {str(e)}'}), 500
    
    # Create verification request
    verification = VerificationRequest(
        user_id=current_user.id,
        photo_url=photo_url
    )
    
    db.session.add(verification)
    db.session.commit()
    
    return jsonify({
        'message': 'Verification request submitted successfully',
        'verification': verification.to_dict()
    }), 201

@bp.route('/status', methods=['GET'])
@token_required
def get_verification_status(current_user):
    """Get user's verification status"""
    verification = VerificationRequest.query.filter_by(
        user_id=current_user.id
    ).order_by(VerificationRequest.created_at.desc()).first()
    
    if not verification:
        return jsonify({'status': 'none', 'message': 'No verification request found'}), 200
    
    return jsonify({
        'status': verification.status,
        'verification': verification.to_dict()
    }), 200

@bp.route('/admin/list', methods=['GET'])
@token_required
def list_verification_requests(current_user):
    """Admin: List all verification requests"""
    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    status = request.args.get('status', 'pending')
    
    verifications = VerificationRequest.query.filter_by(status=status).order_by(
        VerificationRequest.created_at.desc()
    ).all()
    
    return jsonify({
        'verifications': [v.to_dict() for v in verifications]
    }), 200

@bp.route('/admin/<int:verification_id>/approve', methods=['POST'])
@token_required
def approve_verification(current_user, verification_id):
    """Admin: Approve verification request"""
    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    verification = VerificationRequest.query.get_or_404(verification_id)
    
    if verification.status != 'pending':
        return jsonify({'message': 'Request already processed'}), 400
    
    data = request.json or {}
    
    verification.status = 'approved'
    verification.reviewed_at = datetime.utcnow()
    verification.reviewed_by = current_user.id
    verification.admin_notes = data.get('notes', '')
    
    # Update user's verified status
    user = User.query.get(verification.user_id)
    if user:
        user.is_verified = True
    
    db.session.commit()
    
    return jsonify({
        'message': 'Verification approved',
        'verification': verification.to_dict()
    }), 200

@bp.route('/admin/<int:verification_id>/reject', methods=['POST'])
@token_required
def reject_verification(current_user, verification_id):
    """Admin: Reject verification request"""
    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    verification = VerificationRequest.query.get_or_404(verification_id)
    
    if verification.status != 'pending':
        return jsonify({'message': 'Request already processed'}), 400
    
    data = request.json or {}
    
    verification.status = 'rejected'
    verification.reviewed_at = datetime.utcnow()
    verification.reviewed_by = current_user.id
    verification.admin_notes = data.get('notes', 'Verification rejected by admin')
    
    db.session.commit()
    
    return jsonify({
        'message': 'Verification rejected',
        'verification': verification.to_dict()
    }), 200
