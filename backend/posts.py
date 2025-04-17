from flask import Blueprint, request, jsonify
from models import User, Book, Following
from extensions import db
from books import books_bp
from sqlalchemy.sql import func

posts_bp = Blueprint('posts', __name__)

@books_bp.route('/books/nearby/<username>', methods=['GET'])
def fetch_nearby_books(username):
    """Return all books uploaded by users from the same school as `username`.
        Can be filtered by 'transaction_type'(rent or sell)
        eg. /books/nearby/elaine?transaction_type=sell
    """
    transaction_type = request.args.get('transaction_type')
    if transaction_type and transaction_type not in {'rent', 'sell'}:
        return jsonify({'success': False, 'message': 'transaction_type must be either "rent" or "sell"'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    if not getattr(user, 'school', None):
        return jsonify({'success': False, 'message': 'User does not have a school set – cannot perform nearby search.'}), 400

    nearby_ids = db.session.query(User.id).filter(User.school == user.school, User.id != user.id)

    query = Book.query.filter(Book.user_id.in_(nearby_ids))
    if transaction_type:
        query = query.filter(Book.transaction_type == transaction_type)

    books = query.order_by(Book.uploaded_at.desc()).all()

    books_data = []
    for book in books:
        data = {
            'id': book.id,
            'name': book.name,
            'transaction_type': book.transaction_type,
            'price': book.price,
            'uploaded_at': book.uploaded_at.isoformat(),
            'owner': book.owner.username
        }
        if book.transaction_type == 'rent':
            data['rent_duration'] = book.rent_duration
        books_data.append(data)

    return jsonify({'success': True, 'books': books_data}), 200


@books_bp.route('/books/following/<username>', methods=['GET'])
def fetch_following_books(username):
    """Return books uploaded by the users that username is following.
        Can be filtered by 'transaction_type'(rent or sell)
    """
    transaction_type = request.args.get('transaction_type')
    if transaction_type and transaction_type not in {'rent', 'sell'}:
        return jsonify({'success': False, 'message': 'transaction_type must be either "rent" or "sell"'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    following_ids = db.session.query(Following.following_id).filter_by(user_id=user.id).subquery()

    query = Book.query.filter(Book.user_id.in_(following_ids))
    if transaction_type:
        query = query.filter(Book.transaction_type == transaction_type)

    books = query.order_by(Book.uploaded_at.desc()).all()

    books_data = []
    for book in books:
        data = {
            'id': book.id,
            'name': book.name,
            'transaction_type': book.transaction_type,
            'price': book.price,
            'uploaded_at': book.uploaded_at.isoformat(),
            'owner': book.owner.username
        }
        if book.transaction_type == 'rent':
            data['rent_duration'] = book.rent_duration
        books_data.append(data)

    return jsonify({'success': True, 'books': books_data}), 200


@books_bp.route('/books/recommend/<username>', methods=['GET'])
def recommend_books(username):
    """Return a set of random books for the username."""
    limit = 50

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    books = (
        Book.query
            .filter(Book.user_id != user.id) 
            .order_by(func.random())
            .limit(limit)
            .all()
    )

    books_data = []
    for book in books:
        data = {
            'id': book.id,
            'name': book.name,
            'transaction_type': book.transaction_type,
            'price': book.price,
            'uploaded_at': book.uploaded_at.isoformat(),
            'owner': book.owner.username
        }
        if book.transaction_type == 'rent':
            data['rent_duration'] = book.rent_duration
        books_data.append(data)

    return jsonify({'success': True, 'books': books_data}), 200
