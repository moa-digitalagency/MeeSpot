#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from flask import Blueprint, request, jsonify
from backend import db
from backend.models.user import User
from backend.models.report import Report
from backend.utils.auth import token_required, admin_required

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@bp.route('/users', methods=['GET'])
@token_required
@admin_required
def get_users(current_user):
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@bp.route('/reports', methods=['GET'])
@token_required
@admin_required
def get_reports(current_user):
    reports = Report.query.all()
    return jsonify([report.to_dict() for report in reports])

@bp.route('/reports', methods=['POST'])
@token_required
def create_report(current_user):
    data = request.json
    report = Report(
        reporter_id=current_user.id,
        reported_user_id=data.get('reported_user_id'),
        room_id=data.get('room_id'),
        reason=data['reason']
    )
    db.session.add(report)
    db.session.commit()
    
    return jsonify({'message': 'Report submitted successfully'})
