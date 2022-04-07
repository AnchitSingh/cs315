from datetime import datetime
from flask import abort, render_template, url_for, flash, redirect, request
from portal import app,db, login_manager,bcrypt
from flask_login import UserMixin
from flask_admin import Admin,BaseView,expose
from flask_admin.contrib import sqla
from flask_security import utils
from flask_admin.contrib.sqla import ModelView
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import current_user
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
from portal.src.mapping import  *





class course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    info = db.Column(db.Text)
    assign_share = db.Column(db.Float,default =25)
    quiz_share = db.Column(db.Float,default =25)
    live_share = db.Column(db.Float,default =25)
    ga_share = db.Column(db.Float,default =25)
    curr_active_assignment_id =  db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_closed = db.Column(db.Boolean,default =False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'))
    
    
    def __repr__(self):
        return f"Course('{self.name}', '{self.teacher_id}')"


