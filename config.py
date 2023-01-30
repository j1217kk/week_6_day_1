import os

basedir = os.path.abspath(os.path.dirname(__file__))

#Give access to the project in ANY Operating System we find ourselves in
#Allows outside files/folders to be added to the project from the base directory

class Config():
    """
    Set Config variables for the flask app.
    Using Environment Variables where available.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nananana boo boo you will never guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False #turn off update messages from sqlalchemy