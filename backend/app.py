# app.py
import os
from flask import Flask
from flask_cors import CORS
from extensions import db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)

    with app.app_context():
        from models import User, Book, Transaction
        # db.drop_all()   For development
        db.create_all()

    # Register blueprints after creating the app context
    from auth import auth_bp
    from books import books_bp
    from transactions import transactions_bp
    from follows import follows_bp

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(books_bp, url_prefix='/api')
    app.register_blueprint(transactions_bp, url_prefix='/api')
    app.register_blueprint(follows_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)
