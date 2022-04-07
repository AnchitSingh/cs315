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




class chat_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Chat('{self.content}', '{self.date_created}')"




class thread_question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"question('{self.question}', '{self.date_created}')"




class thread_object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('thread_object.id',ondelete='CASCADE'))
    parent_comments = db.relationship('thread_object', remote_side='thread_object.id',backref='sub_comments', lazy=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id',ondelete='CASCADE'))
    unique_key = db.Column(db.Text)

    def __repr__(self):
        return f"thread('{self.content}', '{self.id}')"

        
