#!/usr/bin/env python3
# coding:utf-8

from flask import request, render_template, \
    flash, redirect, url_for, make_response
from . import app


@app.route('/')
def index():
    return render_template('index.html')

