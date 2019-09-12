from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    # user_agent = request.headers.get('User-Agent')
    # response = make_response('<h1>This document carries a cookie!</h1>',200)
    # response.set_cookie('answer','42')

    form = NameForm()

    # handling POST request
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'],
                            'NEW USER',
                            'mail/new_user',
                            user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',
                            form=form, name=session.get('name'),
                            known=session.get('known', False))


@main.route('/redirect')
def redi():
    return redirect('http://www.google.com/ncr')

@main.route('/user/<name>')
def user(name):
    return render_template('user.html', user=name)

@main.route('/user/')
def user_stranger():
    return render_template('user.html')

@main.route('/nums/<num>')
def nums(num):
    c = list()
    for i in range(1, int(num)+1):
        c.append(i)
    return render_template('nums.html', nums=c)