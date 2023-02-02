from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from car_collection.forms import CarForm
from car_collection.models import Car, db
from car_collection.helpers import random_captcha_generator


site = Blueprint('site', __name__, template_folder = 'site_templates')

"""
Note that in the above code, some arguments are specified when creating the
Blueprint object. The first argument, 'site', is the Blueprint's name, this is
used by Flask's routing mechanism. The second argument, __name__, is the Blueprint's
import name which Flask uses to locate teh Blueprint's resources
"""

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    my_car = CarForm()
    try:
        if request.method == "POST" and my_car.validate_on_submit():
            make = my_car.make.data
            model = my_car.model.data
            model_year = my_car.model_year.data
            type_ = my_car.type_.data
            price = my_car.price.data
            horsepower = my_car.horsepower.data
            license = my_car.license.data
            random_captcha = random_captcha_generator()
            user_token = current_user.token

            car = Car(make, model, model_year, type_, price, horsepower, license, random_captcha, user_token) 

            db.session.add(car)
            db.session.commit()

            flash(f"You have successfully added a car. {model_year} {make} {model}")

            return redirect(url_for('site.profile'))
    except:
        raise Exception("Car not added, please check your form and try again!")

    user_token = current_user.token

    cars = Car.query.filter_by(user_token = user_token)
    return render_template('profile.html', form=my_car, cars=cars)
