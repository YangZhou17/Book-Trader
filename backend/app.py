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

if __name__ == '__main__':
    app.run(debug=True, port=8080)
