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
from flask import Blueprint

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message

from datetime import datetime
from threading import Thread
from config import config

main = Blueprint('main', __name__)

from . import views, errors

# initial for flask_bootstrap module
bootstrap = Bootstrap()

# initial for flask_moment module
moment = Moment()

# initial sqlalchemy
db = SQLAlchemy()

mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app