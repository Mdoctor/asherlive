#!/usr/bin/env python3
# coding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    # 附加路由和自定义的错误页面
    from .views import app as app_blueprint
    app.register_blueprint(app_blueprint)

    return app
