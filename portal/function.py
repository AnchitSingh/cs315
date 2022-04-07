from flask import Flask,abort, session, render_template, url_for, flash, redirect, request,send_file
from portal import app, db, bcrypt,mail
from portal.forms import  *
from portal.models import  *
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import os 
import json
import secrets
from os import path
from os.path import join, dirname, realpath
from sqlalchemy.sql.functions import func
from sqlalchemy.sql import text
from sqlalchemy import update
import pandas as pd
from datetime import datetime ,date ,timedelta
from flask import Response
import json
import os

from sqlalchemy import and_,or_
import requests

global cur_usr

from datetime import date
from datetime import datetime
from dateutil import parser
import urllib.request, json
from sqlalchemy import func
import codecs


import shutil
import os


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path= os.path.join(app.root_path,'static/profile_pics',picture_fn)
    form_picture.save(picture_path)
    return picture_fn

def save_csv(form_file):
    random_hex = secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_file.filename)
    picture_fn=random_hex+f_ext
    picture_path= os.path.join(app.root_path,'static/student_csv',picture_fn)
    form_file.save(picture_path)
    return picture_fn
