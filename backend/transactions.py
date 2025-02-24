from flask import Blueprint, jsonify
from models import User, Transaction
from extensions import db
from sqlalchemy import or_

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions/<username>', methods=['GET'])
def fetch_transactions(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    transactions = Transaction.query.filter(
        or_(Transaction.seller_id == user.id, Transaction.buyer_renter_id == user.id)
    ).all()
    transactions_data = [{
        'id': t.id,
        'book_name': t.book_name,
        'transaction_type': t.transaction_type,
        'price': t.price,
        'seller': User.query.get(t.seller_id).username,
        'buyer_renter': User.query.get(t.buyer_renter_id).username,
        'rent_duration': t.rent_duration,
        'transaction_datetime': t.transaction_datetime.isoformat(),
        'status': t.status
    } for t in transactions]
    return jsonify({'success': True, 'transactions': transactions_data}), 200
