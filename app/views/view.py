#!/usr/bin/env python3
# coding:utf-8


from flask import request, render_template, \
    flash, current_app, abort, redirect, url_for, make_response, send_from_directory
from . import main
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from .forms import EditProfileForm, EditProfileAdminForm, PostForm,\
    CommentForm
from .. import db
from ..models import Permission, Role, User, Post, Comment
from ..decorators import admin_required, permission_required
import os
import re
import copy

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = copy.deepcopy(pagination.items)

    def replace_body(body):
        regex = re.compile("<(?:.|\s)*?>")
        rest = regex.sub('',body)[:150]
        return  rest
    for x in posts:
        x.body = replace_body(x.body)
        x.body_html = replace_body(x.body_html)
    return render_template('index.html',posts=posts,
                           show_followed=show_followed, pagination=pagination)

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def article(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
            db.session.add(comment)
            flash('Your comment has been published.')
            return redirect(url_for('.article', id=post.id))
        else:
            return redirect(url_for('auth.login', next=url_for('.article', id=post.id)))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('article.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@main.route('/post/', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    return render_template('post.html', form=form)

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        return redirect(url_for('.index'))
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.article', id=post.id))
    id= post.id
    form.title.data = post.title
    form.body.data = post.body
    return render_template('post.html', form=form,id=id)

@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        return redirect(url_for('.index'))
    db.session.delete(post)
    return redirect(url_for('.index'))

@main.route('/download/<path:filename>', methods=['POST', 'GET'])
def downloadfile(filename):
    print(filename)
    from urllib import parse
    return send_from_directory("/data/asherlive/app/download/", filename, as_attachment=True,attachment_filename = parse.quote(filename))



@main.route('/download/')
@login_required
def download():
    listdir = sorted(os.listdir("/data/asherlive/app/download/"))
    return render_template("download.html",listdir=listdir)


