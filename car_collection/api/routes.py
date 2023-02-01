from flask import Blueprint, request, jsonify
from car_collection.helpers import token_required, random_captcha_generator
from car_collection.models import db, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix='/api')


#Create Car Endpoint
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(our_user):
    make = request.json['make']
    model = request.json['model']
    model_year = request.json['model_year']
    type_ = request.json['type_']
    price = request.json['price']
    horsepower = request.json['horsepower']
    license = request.json['license']
    random_captcha = random_captcha_generator()
    user_token = our_user.token

    print(f"User Token: {our_user.token}")
    
    car = Car(make, model, model_year, type_, price, horsepower, license, random_captcha, user_token = user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)

#Retrieve all car endpoints
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(our_user):
    owner = our_user.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

#Retrieve One Car Endpoint
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(our_user, id):
    owner = our_user.token
    if owner == our_user.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid ID Required'}), 401

#Update Endpoint
@api.route('/cars/<id>', methods = ['PUT', 'POST'])
@token_required
def update_car(our_user, id):
    car = Car.query.get(id)
    car.make = request.json['make']
    car.model = request.json['model']
    car.model_year = request.json['model_year']
    car.type_ = request.json['type_']
    car.price = request.json['price']
    car.horsepower = request.json['horsepower']
    car.license = request.json['license']
    car.random_captcha = random_captcha_generator()
    car.user_token = our_user.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

#Delete Car Endpoint
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_cars(our_user, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)