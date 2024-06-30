from flask import Blueprint, request, jsonify, current_app
from ..models import User
import jwt
from datetime import datetime, timedelta

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print("Received data JSON:", data)  # test
    username = data['username']
    password = data['password']
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = jwt.encode(
            {'username': username, 'exp': datetime.now() + timedelta(minutes=30)},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )
        print("Received data JSON:", token)  # test
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401
    

# @auth_blueprint.route('/verify-token', methods=['POST'])
# def verify_token():
#     token = request.form.get('token')
#     if token:
#         try:
#             decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
#             return jsonify({'username': decoded_token['username']}), 200
#         except jwt.ExpiredSignatureError:
#             return jsonify({'message': 'Token has expired'}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({'message': 'Invalid token'}), 401
#     return jsonify({'message': 'Token is required'}), 400