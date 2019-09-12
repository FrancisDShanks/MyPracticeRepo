#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import redirect
from flask import abort
from flask import url_for
from flask import session
from flask import flash

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# set up a encription key for security
app.config['SECRET_KEY'] = 'hard to guess string'

# initial for flask_bootstrap module
bootstrap = Bootstrap(app)

# initial for flask_moment module
moment = Moment(app)

# initial sqlalchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlit')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Role(db.Model):
    # '__tablename__' define table name in database
    __tablename__ = 'roles'

    # define columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # users will return a list of all User relate to this Role
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Email()])
    passwd = PasswordField('Password:',validators=[Length(6,10)])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    # user_agent = request.headers.get('User-Agent')
    # response = make_response('<h1>This document carries a cookie!</h1>',200)
    # response.set_cookie('answer','42')
    form = NameForm()
    show_form = True

    # handling POST request
    if form.validate_on_submit():
        old_name = session['name']
        if old_name is not None and old_name!=form.name.data:
            flash('You changed you name?')
        session['name'] = form.name.data
        session['passwd'] = form.passwd.data
        show_form = False
        return redirect(url_for('index'))

    ur = url_for('user_stranger',_external=True)
    return render_template('index.html',ur=ur, current_time=datetime.utcnow(),form=form,name=session.get('name'),show_form=show_form)

@app.route('/redirect')
def redi():
    return redirect('http://www.google.com/ncr')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',user=name)

@app.route('/user/')
def user_stranger():
    return render_template('user.html')

@app.route('/nums/<num>')
def nums(num):
    c = list()
    for i in range(1,int(num)+1):
        c.append(i)
    return render_template('nums.html',nums=c)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == '__main__':
    app.run(debug=True)

