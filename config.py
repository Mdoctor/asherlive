#!/usr/bin/env python3
# coding:utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

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
