from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

#Adding Flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

#Import secrets -- a module for generating randomized characters -- how to generate user token
import secrets

db = SQLAlchemy() #instantiating sql db

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False) #need to have an email
    password = db.Column(db.String, nullable=False) #need to have password. but this will be hashed and committed.
    token = db.Column(db.String, default='', unique = True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    #consider whats above the postgres side, and whats below the python side
    def __init__(self, email, password, first_name='', last_name='', id='', token=''): #need init because we need something to create the instance of the user.
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4()) #generates random set of numbers/id
    
    def set_token(self, length):
        return secrets.token_hex(length)

    def set_password(self, password):
        return generate_password_hash(password)

    def __repr__(self):
        return f"User {self.email} has been added to the database!"



