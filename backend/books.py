from flask import Blueprint, request, jsonify
from models import User, Book, Transaction
from extensions import db

books_bp = Blueprint('books', __name__)

@books_bp.route('/upload', methods=['POST'])
def upload_book():
    data = request.get_json()
    username = data.get('username')
    book_name = data.get('book_name')
    transaction_type = data.get('transaction_type')
    
    if not username or not book_name or transaction_type not in ['rent', 'sell']:
        return jsonify({'success': False, 'message': 'Invalid parameters'}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    price = data.get('price')
    if price is None:
        return jsonify({'success': False, 'message': 'Price is required'}), 400

    if transaction_type == 'rent':
        rent_duration = data.get('rent_duration')
        if rent_duration is None:
            return jsonify({'success': False, 'message': 'Rent duration is required for renting books'}), 400
        book = Book(name=book_name, transaction_type=transaction_type, user_id=user.id, price=price, rent_duration=rent_duration)
    else:
        book = Book(name=book_name, transaction_type=transaction_type, user_id=user.id, price=price)
    
    db.session.add(book)
    db.session.commit()
    return jsonify({'success': True, 'book_id': book.id}), 201

@books_bp.route('/buy', methods=['POST'])
def buy_book():
    data = request.get_json()
    username = data.get('username')
    book_id = data.get('book_id')
    
    if not username or not book_id:
        return jsonify({'success': False, 'message': 'Invalid parameters'}), 400
    
    buyer = User.query.filter_by(username=username).first()
    if not buyer:
        return jsonify({'success': False, 'message': 'Buyer not found'}), 404

    book = Book.query.get(book_id)
    if not book:
        return jsonify({'success': False, 'message': 'Book not found'}), 404
    if book.transaction_type != 'sell':
        return jsonify({'success': False, 'message': 'This book is not for sale'}), 400

    seller_id = book.user_id
    db.session.delete(book)
    transaction = Transaction(
        book_name=book.name,
        transaction_type='sell',
        price=book.price,
        seller_id=seller_id,
        buyer_renter_id=buyer.id,
        rent_duration=None,
        status='completed'
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Book purchased successfully'}), 200

@books_bp.route('/rent', methods=['POST'])
def rent_book():
    data = request.get_json()
    username = data.get('username')
    book_id = data.get('book_id')
    
    if not username or not book_id:
        return jsonify({'success': False, 'message': 'Invalid parameters'}), 400
    
    renter = User.query.filter_by(username=username).first()
    if not renter:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'success': False, 'message': 'Book not found'}), 404
    if book.transaction_type != 'rent':
        return jsonify({'success': False, 'message': 'This book is not available for rent'}), 400

    seller_id = book.user_id
    transaction = Transaction(
        book_name=book.name,
        transaction_type='rent',
        price=book.price,
        seller_id=seller_id,
        buyer_renter_id=renter.id,
        rent_duration=book.rent_duration,
        status='ongoing'
    )
    db.session.delete(book)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Book rented successfully', 'transaction_id': transaction.id}), 200

@books_bp.route('/return', methods=['POST'])
def return_book():
    data = request.get_json()
    username = data.get('username')
    transaction_id = data.get('transaction_id')
    
    if not username or not transaction_id:
        return jsonify({'success': False, 'message': 'Invalid parameters'}), 400
    
    renter = User.query.filter_by(username=username).first()
    if not renter:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    transaction = Transaction.query.filter_by(
        id=transaction_id,
        transaction_type='rent',
        status='ongoing',
        buyer_renter_id=renter.id
    ).first()
    if not transaction:
        return jsonify({'success': False, 'message': 'No matching ongoing renting transaction found'}), 404

    transaction.status = 'returned'
    returned_book = Book(
        name=transaction.book_name,
        transaction_type='rent',
        user_id=transaction.seller_id,
        price=transaction.price,
        rent_duration=transaction.rent_duration
    )
    db.session.add(returned_book)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Book returned successfully'}), 200

@books_bp.route('/delete', methods=['DELETE'])
def delete_book():
    data = request.get_json()
    username = data.get('username')
    book_id = data.get('book_id')
    
    if not username or not book_id:
        return jsonify({'success': False, 'message': 'Invalid parameters'}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    book = Book.query.get(book_id)
    if not book:
        return jsonify({'success': False, 'message': 'Book not found'}), 404
    
    # Ensure the book was uploaded by this user.
    if book.user_id != user.id:
        return jsonify({'success': False, 'message': 'Not authorized to delete this book'}), 403

    db.session.delete(book)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Book deleted successfully'}), 200

@books_bp.route('/books/selling', methods=['GET'])
def fetch_selling_books():
    books = Book.query.filter_by(transaction_type='sell').all()
    books_data = [{
        'id': book.id,
        'name': book.name,
        'price': book.price,
        'owner': book.owner.username,
        'uploaded_at': book.uploaded_at.isoformat()
    } for book in books]
    return jsonify({'success': True, 'books': books_data}), 200

@books_bp.route('/books/renting', methods=['GET'])
def fetch_renting_books():
    books = Book.query.filter_by(transaction_type='rent').all()
    books_data = [{
        'id': book.id,
        'name': book.name,
        'price': book.price,
        'rent_duration': book.rent_duration,
        'owner': book.owner.username,
        'uploaded_at': book.uploaded_at.isoformat()
    } for book in books]
    return jsonify({'success': True, 'books': books_data}), 200

@books_bp.route('/books/search', methods=['GET'])
def fetch_books_by_parameter():
    # Retrieve query parameters from the URL (all are optional)
    book_name = request.args.get('book_name')
    transaction_type = request.args.get('transaction_type')
    username = request.args.get('username')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    rent_duration = request.args.get('rent_duration')

    print(f"Search parameters: book_name={book_name}, transaction_type={transaction_type}, username={username}, min_price={min_price}, max_price={max_price}, rent_duration={rent_duration}")

    # Ensure that at least one search parameter has been provided.
    if not (book_name or transaction_type or username or min_price or max_price or rent_duration):
        return jsonify({'success': False, 'message': 'At least one search parameter must be provided.'}), 400

    query = Book.query

    # Filter by book name (using case-insensitive partial matching)
    if book_name:
        query = query.filter(Book.name.ilike(f"%{book_name}%"))
    
    # Filter by transaction type ('rent' or 'sell')
    if transaction_type:
        query = query.filter(Book.transaction_type == transaction_type)
    
    # Filter by owner's username using the relationship from models (Book.owner)
    if username:
        query = query.filter(Book.owner.has(username=username))
    
    # Filter by a minimum price if provided
    if min_price:
        try:
            min_price_value = float(min_price)
            query = query.filter(Book.price >= min_price_value)
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid min_price value'}), 400
    
    # Filter by a maximum price if provided
    if max_price:
        try:
            max_price_value = float(max_price)
            query = query.filter(Book.price <= max_price_value)
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid max_price value'}), 400

    # Filter by rent_duration if provided.
    # Note: The rent_duration filter is only applicable when looking for renting books.
    if rent_duration:
        try:
            rent_duration_value = int(rent_duration)
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid rent_duration value'}), 400
        
        if transaction_type:
            if transaction_type.lower() == 'rent':
                query = query.filter(Book.rent_duration == rent_duration_value)
            # If transaction_type is 'sell', we ignore the rent_duration filter.
        else:
            # When transaction_type is not provided, return all selling books
            # and renting books with rent_duration >= the provided value.
            from sqlalchemy import or_, and_
            query = query.filter(
                or_(
                    Book.transaction_type == 'sell',
                    and_(Book.transaction_type == 'rent', Book.rent_duration >= rent_duration_value)
                )
            )

    # Execute the query and prepare the result data
    books = query.all()
    books_data = []
    for book in books:
        book_data = {
            'id': book.id,
            'name': book.name,
            'transaction_type': book.transaction_type,
            'price': book.price,
            'uploaded_at': book.uploaded_at.isoformat(),
            'owner': book.owner.username
        }
        if book.transaction_type == 'rent':
            book_data['rent_duration'] = book.rent_duration
        books_data.append(book_data)

    return jsonify({'success': True, 'books': books_data}), 200

@books_bp.route('/books/all/<username>', methods=['GET'])
def fetch_all_user_books(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    books = Book.query.filter_by(user_id=user.id).all()
    books_data = [{
        'id': book.id,
        'name': book.name,
        'price': book.price,
        'transaction_type': book.transaction_type,
        'rent_duration': book.rent_duration if book.transaction_type == 'rent' else None,
        'uploaded_at': book.uploaded_at.isoformat()
    } for book in books]
    return jsonify({'success': True, 'books': books_data}), 200

@books_bp.route('/books/selling/<username>', methods=['GET'])
def fetch_user_selling_books(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    books = Book.query.filter_by(transaction_type='sell', user_id=user.id).all()
    books_data = [{
        'id': book.id,
        'name': book.name,
        'price': book.price,
        'uploaded_at': book.uploaded_at.isoformat()
    } for book in books]
    return jsonify({'success': True, 'books': books_data}), 200

@books_bp.route('/books/renting/<username>', methods=['GET'])
def fetch_user_renting_books(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    books = Book.query.filter_by(transaction_type='rent', user_id=user.id).all()
    books_data = [{
        'id': book.id,
        'name': book.name,
        'price': book.price,
        'rent_duration': book.rent_duration,
        'uploaded_at': book.uploaded_at.isoformat()
    } for book in books]
    return jsonify({'success': True, 'books': books_data}), 200