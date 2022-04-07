import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
import smtplib


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:verystrongpassword@localhost/threads?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CELERY_BACKEND']='redis://localhost'
app.config['CELERY_BROKER_URL']='redis://localhost'
# from portal.src.school import school
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['DEBUG'] = True   
app.config['TESTING'] = False             
mail = Mail(app)
moment = Moment(app)

from portal import routes

from portal.route import chat,admin,database,forum,course
import shutil
import os

