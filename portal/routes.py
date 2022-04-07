from flask import Flask,abort, session, render_template, url_for, flash, redirect, request,send_file,jsonify
from portal import app, db, bcrypt,mail
from portal.forms import  *
from portal.models import *
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


from portal.function import *



# def callback():
#     print("Hello Anchit!")

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()






@app.route("/")
def root():
    return redirect('login')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user1 = user.query.filter_by(email=form.email.data).first()
        if user1 and bcrypt.check_password_hash(user1.password, form.password.data):
            if(user1.is_active==False):
                flash('Your account is currently inactive, Please wait for approval', 'error')
                return redirect(url_for('login'))
            login_user(user1, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'error')
    # flash('Test','success')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route("/register", methods=['GET', 'POST'])
def register():
    user1=user.query.all()
    checkAdmin=1
    for u in user1:
        if u.is_admin==True:
            checkAdmin=0
            break
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('register.html', title='Register',check=checkAdmin)





@app.route("/register_usr", methods=['GET', 'POST'])
def register_usr():
    if request.method == 'GET':
        return render_template('error.html')
    else:
        usr_c=user.query.filter_by(username=request.form['username']).first()
        email_c=user.query.filter_by(email=request.form['email']).first()
        if usr_c is not None:
            flash('This username is already taken','error')
            return redirect(url_for('register'))
        elif email_c is not None:
            flash('This email is already taken','error')
            return redirect(url_for('register'))
        elif request.form['password'] != request.form['confirm']:
            flash('Password and Confirm password should be same','error')
            return redirect(url_for('register'))
        else:
            hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            user1 = user(username=request.form['username'], email=request.form['email'], password=hashed_password)
            db.session.add(user1)
            db.session.commit()
        code = request.form['code']
        if code != '' and code.lower() == 'Admin':
            user1.is_admin=True
            user1.is_active=True
            db.session.commit()
            flash('Admin account created','success')
        elif code != '' and code.lower() == 'student':
            user1.is_student=True
            user1.is_active=True
            db.session.commit()
            flash('Student account created','success')
        elif code != '' and code.lower() == 'teacher':
            user1.is_instructor=True
            user1.is_active=True
            db.session.commit()
            flash('Instructor account created','success')
        else:
            flash('Wait for admin approval', 'info')
        return redirect(url_for('login'))



@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.is_active == True:
        return render_template('chat.html',title='Discussion')
    else:
        flash('Your account has been deactivated by administrator','error')
        return redirect(url_for('logout'))















@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.is_active == True:
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file=picture_file
            current_user.username=form.username.data
            current_user.email=form.email.data
            current_user.firstname=form.firstname.data
            current_user.lastname=form.lastname.data
            current_user.address=form.address.data
            db.session.commit()
            flash('Your account has been updated','success')
            return redirect('profile')
        elif request.method == 'GET':
            form.username.data=current_user.username
            form.email.data=current_user.email
            form.firstname.data=current_user.firstname
            form.lastname.data=current_user.lastname
            form.address.data=current_user.address
        return render_template('profile.html', title='Profile',bot=btok,form=form,active_nav='profile')
    else:
        flash('Your account has been deactivated by administrator','info')
        return redirect(url_for('logout'))


@app.route('/users/<username>', methods=['GET', 'POST'])
@login_required
def users(username):
    if current_user.is_active == True:
        user1 = user.query.filter(and_(user.username==username,user.is_admin==False)).first_or_404()
        return render_template('user.html', user=user1,title='Users')
    else:
        flash('Your account has been deactivated by administrator','error')
        return redirect(url_for('logout'))



def send_invite_email(user,msg):
    token = user.get_invite_token()
    msg = Message("You've been invited to join "+msg+" as a teacher.",
                  sender='t2tadmin@cse.iitk.ac.in',
                  recipients=[user.email])
    msg.body = f'''Visit the following link to set up your account and password: 
{url_for('setup_account', token=token, _external=True)}
If you already had an account then simply ignore this email and no changes will be made.
'''
    mail.send(message=msg)


@app.route("/setup_account/<token>", methods=['GET', 'POST'])
def setup_account(token):
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    user1 = user.verify_invite_token(token)
    if user1 is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('register'))
    form = InviteForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file=picture_file
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user1.password = hashed_password
        user1.firstname = form.firstname.data
        db.session.commit()
        flash('Your account setup is complete! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('invite.html', title='Setup Account',usr=user1, form=form)





def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='t2tadmin@cse.iitk.ac.in',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(message=msg)





@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user1 = user.query.filter_by(email=form.email.data).first()
        send_reset_email(user1)
        flash('A email has been sent with instructions to reset your password','success')
        return redirect(url_for('login'))
    return render_template('reset_request.html',title= 'Reset Password',form=form)



@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    user1 = user.verify_reset_token(token)
    if user1 is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user1.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',error=404)
