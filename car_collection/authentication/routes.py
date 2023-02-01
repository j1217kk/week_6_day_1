from flask import Blueprint, render_template, request, redirect, url_for, flash
from car_collection.forms import UserLoginForm
from car_collection.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

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
            
            return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('signup.html',form=form)


@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first() #queries user data in user table and stores first instance
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in via Email/Password', 'auth-success')
                return redirect(url_for('site.profile'))
    except:
        raise Exception("Invalid Form Data: Please check your form and try again.")
    return render_template('signin.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))
