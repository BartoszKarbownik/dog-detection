from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import Swagger, swag_from
import jwt
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Load configuration directly into Flask's configuration
with open('config.json', 'r') as file:
    app.config.update(json.load(file))

app.config.setdefault('SECRET_KEY', 'your_secret_key_here')
app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'mysql+mysqlconnector://root:@localhost/dpm')
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Swagger
Swagger(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('User_ID', db.Integer, primary_key=True)
    username = db.Column('User_Username', db.String(50), unique=True, nullable=False)
    password = db.Column('User_Password', db.String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Authentication Blueprint
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = jwt.encode(
            {'username': username, 'exp': datetime.now() + timedelta(minutes=30)},
            app.config['SECRET_KEY'], algorithm='HS256'
        )
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@auth_blueprint.route('/generate-token', methods=['POST'])
def generate_token():
    data = request.form
    if 'username' in data and 'password' in data:
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            token = jwt.encode(
                {'username': user.username, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                app.config['SECRET_KEY'], algorithm='HS256'
            )
            return jsonify({'token': token}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    else:
        return jsonify({'message': 'Username and password are required'}), 400

@auth_blueprint.route('/verify-token', methods=['POST'])
def verify_token():
    token = request.form.get('token')
    if token:
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            return jsonify({'username': decoded_token['username']}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
    return jsonify({'message': 'Token is required'}), 400

# Register the Blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

