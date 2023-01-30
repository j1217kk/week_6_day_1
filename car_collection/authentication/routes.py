from flask import Blueprint, render_template

site = Blueprint('authentication', __name__, template_folder = 'auth_templates')

"""
Note that in the above code, some arguments are specified when creating the
Blueprint object. The first argument, 'site', is the Blueprint's name, this is
used by Flask's routing mechanism. The second argument, __name__, is the Blueprint's
import name which Flask uses to locate teh Blueprint's resources
"""

@site.route('/')
def home():
    return render_template('index.html')
