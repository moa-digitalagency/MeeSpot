#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from flask import Blueprint, request, jsonify
from backend import db
from backend.models.subscription_request import SubscriptionRequest
from backend.models.subscription_plan import SubscriptionPlan
from backend.utils.auth import token_required, admin_required
from datetime import datetime

bp = Blueprint('subscriptions', __name__, url_prefix='/api/subscriptions')

@bp.route('/request', methods=['POST'])
@token_required
def request_subscription(current_user):
    """User requests a subscription upgrade"""
    data = request.json
    
    if not data.get('subscription_tier'):
        return jsonify({'error': 'Subscription tier is required'}), 400
    
    # Check if there's already a pending request
    existing = SubscriptionRequest.query.filter_by(
        user_id=current_user.id,
        status='pending'
    ).first()
    
    if existing:
        return jsonify({'error': 'You already have a pending subscription request'}), 400
    
    # Create new request
    sub_request = SubscriptionRequest(
        user_id=current_user.id,
        subscription_tier=data['subscription_tier'],
        status='pending'
    )
    
    db.session.add(sub_request)
    db.session.commit()
    
    return jsonify({
        'message': 'Subscription request submitted successfully',
        'request': sub_request.to_dict()
    })

@bp.route('/my-requests', methods=['GET'])
@token_required
def get_my_requests(current_user):
    """Get current user's subscription requests"""
    requests = SubscriptionRequest.query.filter_by(user_id=current_user.id).order_by(SubscriptionRequest.requested_at.desc()).all()
    return jsonify([r.to_dict() for r in requests])

@bp.route('/pending', methods=['GET'])
@admin_required
def get_pending_requests(current_user):
    """Admin: Get all pending subscription requests"""
    requests = SubscriptionRequest.query.filter_by(status='pending').order_by(SubscriptionRequest.requested_at.asc()).all()
    return jsonify([r.to_dict() for r in requests])

@bp.route('/<int:request_id>/approve', methods=['POST'])
@admin_required
def approve_request(current_user, request_id):
    """Admin: Approve a subscription request"""
    sub_request = SubscriptionRequest.query.get_or_404(request_id)
    
    if sub_request.status != 'pending':
        return jsonify({'error': 'Request already processed'}), 400
    
    # Update user's subscription tier
    user = sub_request.user
    user.subscription_tier = sub_request.subscription_tier
    
    # Update request status
    sub_request.status = 'approved'
    sub_request.reviewed_at = datetime.utcnow()
    sub_request.reviewed_by = current_user.id
    
    db.session.commit()
    
    return jsonify({
        'message': 'Subscription request approved',
        'request': sub_request.to_dict()
    })

@bp.route('/<int:request_id>/reject', methods=['POST'])
@admin_required
def reject_request(current_user, request_id):
    """Admin: Reject a subscription request"""
    data = request.json
    sub_request = SubscriptionRequest.query.get_or_404(request_id)
    
    if sub_request.status != 'pending':
        return jsonify({'error': 'Request already processed'}), 400
    
    # Update request status
    sub_request.status = 'rejected'
    sub_request.reviewed_at = datetime.utcnow()
    sub_request.reviewed_by = current_user.id
    sub_request.rejection_reason = data.get('reason', '')
    
    db.session.commit()
    
    return jsonify({
        'message': 'Subscription request rejected',
        'request': sub_request.to_dict()
    })

@bp.route('/plans', methods=['GET'])
@token_required
def get_plans(current_user):
    """Get all subscription plans"""
    plans = SubscriptionPlan.query.all()
    return jsonify([p.to_dict() for p in plans])
