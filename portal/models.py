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
from portal.src.mapping import *
from portal.src.course import *
from portal.src.chat import *


@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))



class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(120), unique=True)
    image_file = db.Column(db.Text, default='default.jpg')
    password = db.Column(db.String(60))
    name = db.Column(db.String(60))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    is_student = db.Column(db.Boolean, default=False)
    is_instructor = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    login_req = db.Column(db.Integer,default=0)
    
    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return user.query.get(user_id) 
    def get_invite_token(self,expires_sec=180000):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    @staticmethod
    def verify_invite_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return user.query.get(user_id) 

    def __repr__(self):
        return f"user('{self.username}')"







class Controller(ModelView):
    column_display_pk=True
    can_create=True
    can_edit=True
    can_delete=True
    can_export=True
    def on_model_change(self,form,model,is_create):
        model.password=bcrypt.generate_password_hash(model.password).decode('utf-8')
        return current_user.is_authenticated
    def is_accessible(self):
        if current_user.is_active==True and current_user.is_admin:
            return current_user.is_authenticated
        else:
            return abort(404)


class Controller1(ModelView):
    column_display_pk=True
    can_create=True
    can_edit=True
    can_delete=True
    can_export=True
    def is_accessible(self):
        if current_user.is_active==True and current_user.is_admin:
            return current_user.is_authenticated
        else:
            return abort(404)



# db.drop_all()
db.create_all()
db.session.commit()

admin = Admin(app, template_mode='bootstrap3')

class NotificationsView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('admin_dash'))



admin.add_view(Controller(user,db.session))
admin.add_view(Controller1(course,db.session))
admin.add_view(Controller1(thread_object,db.session))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
admin.add_view(NotificationsView(name='Dashboard', endpoint='notify'))
