from flask import Blueprint, request, jsonify, current_app
from ..models import User
import jwt
from datetime import datetime, timedelta

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = jwt.encode(
            {'username': username, 'exp': datetime.now() + timedelta(minutes=30)},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401
    
