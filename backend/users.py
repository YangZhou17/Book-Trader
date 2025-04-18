# users.py
from flask import Blueprint, jsonify
from models import User

# Mount this blueprint at /api/user
users_bp = Blueprint('users', __name__, url_prefix='/api/user')

@users_bp.route('/<username>', methods=['GET'])
def get_user_by_username(username):
    """
    GET /api/user/<username>
    Returns JSON: { success: True, email: "..."} or { success: False, message: "User not found" }
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    return jsonify({
        'success': True,
        'email': user.email
    }), 200