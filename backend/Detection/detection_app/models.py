from detection_app import db  
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta 

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('User_ID', db.Integer, primary_key=True)
    username = db.Column('User_Username', db.String(50), unique=True, nullable=False)
    password = db.Column('User_Password', db.String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Screenshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    filepath = db.Column(db.String(255))
    expires_at = db.Column(db.DateTime, default=lambda: datetime.now() + timedelta(days=1))
    uploaded = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Screenshot {self.filename}>"
