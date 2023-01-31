from flask import Blueprint, render_template, request, redirect, url_for, flash
from car_collection.forms import UserLoginForm
from car_collection.models import User, db

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

"""
Note that in the above code, some arguments are specified when creating the
Blueprint object. The first argument, 'site', is the Blueprint's name, this is
used by Flask's routing mechanism. The second argument, __name__, is the Blueprint's
import name which Flask uses to locate teh Blueprint's resources
"""

@auth.route('/signup', methods = ['GET', 'POST']) #always methods, even if one method. always in list, even if one method.
def signup():
    form = UserLoginForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = form.password.data

            user = User(email, password, first_name, last_name) #non defaults first

            db.session.add(user)
            db.session.commit()

            flash(f"You have successfully created a User account {email}", "user-created") #display (message, category)
            
            return redirect(url_for('site.home'))

    except:
        raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('signup.html',form=form)

@auth.route('/signin')
def signin():
    return render_template('signin.html')

