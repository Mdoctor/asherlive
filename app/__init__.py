#!/usr/bin/env python3
# coding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import config
from flask_mail import Mail
# from flask_moment import Moment
from flask_login import LoginManager
from flask_pagedown import PageDown
from flaskext.markdown import Markdown
import markdown

bootstrap = Bootstrap()
mail = Mail()
# moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    Markdown(app)
    # moment.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    # 附加路由和自定义的错误页面

    from .views import main as app_blueprint
    app.register_blueprint(app_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    @app.template_filter('markdown2html')
    def markdown2html(text):
        return markdown.markdown(text, ['extra'])

    return app
