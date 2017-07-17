#!/usr/bin/env python3
# coding:utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME=0.5
    
    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    """docstring for TestingConfig"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Svc_2015!@@rm-uf6lzwt5nol0s6quq.mysql.rds.aliyuncs.com/app_blog"


config = {
    "testing": TestingConfig,
    "default": TestingConfig
}
