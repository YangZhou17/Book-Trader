import datetime
import base64
from email.headerregistry import Group
from genericpath import isfile
from glob import glob
from hashlib import new
from operator import length_hint
from pydoc import describe, pager
import re
from unittest import result
import zipfile
import shutil
from tkinter import Label
from urllib import response
from urllib.parse import quote
from urllib.robotparser import RequestRate
from flask import Flask, jsonify, request, abort, send_file,g, session,make_response,send_from_directory
import os
import csv
import shutil
import random
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from sqlalchemy import or_

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
# Configuring the Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'rent' or 'sell'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # seller/owner
    uploaded_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    price = db.Column(db.Float, nullable=False)  # Price for both selling and renting
    # For renting books only:
    rent_duration = db.Column(db.Integer, nullable=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(200), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'rent' or 'sell'
    price = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer_renter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rent_duration = db.Column(db.Integer, nullable=True)  # Only for renting books
    transaction_datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.String(20), nullable=True)
    # For selling: status can be 'completed'
    # For renting: status is 'ongoing' until returned, then 'returned'

# Relationships on the User model for clarity
User.books = db.relationship('Book', foreign_keys=[Book.user_id], backref='owner', lazy=True)
User.bought_or_rented = db.relationship('Transaction', foreign_keys=[Transaction.buyer_renter_id], backref='buyer_renter', lazy=True)

# Initialize the database
@app.before_request
def create_tables():
    db.create_all()

# Login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        return jsonify({'success': True}), 200
    else:
        user_exists = User.query.filter_by(username=data['username']).first() is not None
        return jsonify({'success': False, 'userExists': user_exists}), 401

# Register endpoint
@app.route('/api/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first() is not None:
        return jsonify({'success': False, 'message': 'Username already exists'}), 409
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'success': True}), 201

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response

@app.route('/api/upload', methods=['POST'])
def upload_book():
    data = request.get_json()
    username = data.get('username')
    book_name = data.get('book_name')
    transaction_type = data.get('transaction_type')  # Expected to be 'rent' or 'sell'
    
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

@app.route('/api/books/selling', methods=['GET'])
def fetch_selling_books():
    books = Book.query.filter_by(transaction_type='sell').all()
    books_data = [{
        'id': book.id,
        'name': book.name,
        'price': book.price,
        'owner': book.owner.username,
        'uploaded_at': book.uploaded_at.isoformat()
    } for book in books]
    return jsonify({'books': books_data}), 200

@app.route('/api/books/renting', methods=['GET'])
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
    return jsonify({'books': books_data}), 200

@app.route('/api/buy', methods=['POST'])
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
    # Remove the book from the available books table.
    db.session.delete(book)
    # Create a transaction record.
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

@app.route('/api/rent', methods=['POST'])
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

# Endpoint for returning a rented book.
@app.route('/api/return', methods=['POST'])
def return_book():
    data = request.get_json()
    username = data.get('username')
    transaction_id = data.get('transaction_id')
    
    if not username or not transaction_id:
        return jsonify({'success': False, 'message': 'Invalid parameters'}), 400
    
    renter = User.query.filter_by(username=username).first()
    if not renter:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    # Find an ongoing renting transaction matching the provided id and renter.
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

# New endpoint: Fetch all transactions for a user, whether they are the seller or buyer/renter.
@app.route('/api/transactions/<username>', methods=['GET'])
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

if __name__ == '__main__':
    app.run(debug=True, port=8080)
