from . import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.sql.functions import user
from werkzeug.security import check_password_hash, generate_password_hash

# Database model used to store user's notes information
class Note(db.Model):
    # define database columns and their types
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # setting timezone as well as date (func will automatically add current date and time to note)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # setting relationship between note and user object using a foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Note('{self.data}', '{self.date}')" 


# Database model used to store User information
class User(db.Model, UserMixin):
    # define database columns and their types
    # unique means users cannot share the same values in that column
    # find out what nullable means
    # __tablename__ = 'flasklogin-users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # password can store 200 characters because of hashing
    password = db.Column(db.String(200), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='avatar.png')
    account_date = joined_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    last_login = db.Column(db.DateTime(), index=False, default=datetime.utcnow)
    # notes all of the notes that a user has created
    notes = db.relationship('Note') # Note here is the name of Note object created below

    # sha256 is a hashing algorithm
    def encrypt_password(self, password):
        # Create hashed password
        self.password = generate_password_hash(password, method='sha256')
          

    def check_password(self, password):
        # Check hashed password
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"