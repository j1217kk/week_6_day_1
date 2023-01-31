from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm): #   inherits from FlaskForm
    #email, password, first_name, last_name
    email = StringField('Email', validators=[DataRequired(), Email()]) #'Email' is label #Email() uses regex to confirm email format
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    password = PasswordField('Password', validators = [DataRequired()]) #DataRequired() with no following parameter just means ANYTHING needs to be in there to validate
    submit_button = SubmitField()

