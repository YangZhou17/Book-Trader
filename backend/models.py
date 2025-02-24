import datetime
from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'rent' or 'sell'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    price = db.Column(db.Float, nullable=False)
    rent_duration = db.Column(db.Integer, nullable=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(200), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer_renter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rent_duration = db.Column(db.Integer, nullable=True)
    transaction_datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.String(20), nullable=True)

User.books = db.relationship('Book', foreign_keys=[Book.user_id], backref='owner', lazy=True)
User.bought_or_rented = db.relationship('Transaction', foreign_keys=[Transaction.buyer_renter_id], backref='buyer_renter', lazy=True)