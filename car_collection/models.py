from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

#Adding Flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

#Import secrets -- a module for generating randomized characters -- how to generate user token
import secrets

#Import for an authenticated user
from flask_login import UserMixin, LoginManager

#Import for flask marshmallow
from flask_marshmallow import Marshmallow




db = SQLAlchemy() #instantiating sql db
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False) #need to have an email
    password = db.Column(db.String, nullable=False) #need to have password. but this will be hashed and committed.
    token = db.Column(db.String, default='', unique = True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    car = db.relationship('Car', backref='owner', lazy=True)

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

class Car(db.Model):
    id = db.Column(db.String, primary_key=True)
    make = db.Column(db.String(150))
    model = db.Column(db.String(200), nullable=True)
    model_year = db.Column(db.Integer)
    type_ = db.Column(db.String(100)) #suv, sedan, coupe, truck, van, etc.
    price = db.Column(db.Numeric(precision=12, scale=2))
    horsepower = db.Column(db.Integer)
    license = db.Column(db.String(100))
    random_captcha = db.Column(db.String)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, make, model, model_year, type_, price, horsepower, license, random_captcha, user_token):
        self.id = self.set_id()
        self.make = make
        self.model = model 
        self.model_year = model_year
        self.type_ = type_
        self.price = price
        self.horsepower = horsepower
        self.license = license
        self.random_captcha = random_captcha
        self.user_token = user_token
    
    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f"The following car has been added: {self.model_year} {self.make} {self.model}"

    
class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'make', 'model', 'model_year', 'type_', 'price', 'horsepower', 'license', 'random_captcha']


car_schema = CarSchema()
cars_schema = CarSchema(many=True)    




