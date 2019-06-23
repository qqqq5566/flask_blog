# -*- coding:utf-8 -*-
#
# 开发人员 ： sunshenggang
# 开始时间 ： 19-6-20 下午9:17
# 开发工具 ： PyCharm Community Edition
from flask import redirect, render_template, session, url_for, flash, g,make_response
from app.models import User, Article, Category
from app.home import home
from app import db, login_manager
from .forms import LoginForm, RegisterForm, PasswordForm, ForgetpasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user, login_fresh
from app.library.captha import Captcha
from io import BytesIO

@home.before_request
def befor_request():
    g.loginForm = LoginForm()
    g.categoryList = Category.query.filter_by(state=1).order_by('sort').all()

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user




@home.route('/')
def index():

    articleList = Article.query.order_by('add_time').filter_by(state=1).paginate(page=1, per_page=10)

    return render_template('/home/index.html', articleList=articleList, paginate=articleList)


@home.route('/login', methods=['GET', 'POST'])
def login():
    """登录"""
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(username=data['username']).first()
        if check_password_hash(user.password, data['password']):
            print(222222)
            login_user(user)
            print(1111)
            return redirect(url_for('home.index'))
        else:
            print(44444444)
            flash('登录失败','err')

    return render_template('/home/user/login.html', form=form)

@home.route('/register', methods=['GET', 'POST'])
def register():
    """注册"""
    form = RegisterForm()

    if form.validate_on_submit():
        data = form.data

        user = User(
            username=data['username'],
            password=generate_password_hash(data['password']),
            email=data['email'],
            mobile=data['mobile']
        )
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('home.index'))

    return render_template('/home/user/register.html', form=form)


@home.route('/logout')
@login_required
def logout():
    """退出"""
    logout_user()
    return redirect(url_for('home.index'))

@home.route('/forgetpassword', methods=['GET', 'POST'])
def forgetpassword():
    form = ForgetpasswordForm()

    if form.validate_on_submit():
        pass
    return render_template('/home/user/forget.html', form=form)

@home.route('/set_password', methods=['GET', 'POST'])
@login_required
def set_password():
    """修改密码"""
    form = PasswordForm()
    if form.validate_on_submit():
        data = form.data  #获取数据
        print('用户编号{}'.format(current_user.get_id()))
        user = User.query.get(current_user.get_id())
        user.password = generate_password_hash(data['password'])
        db.session.commit()
        flash('修改成功')
        login_fresh()
        return redirect(url_for('home.login'))

    return render_template('/home/user/secret.html', form=form)

@home.route('/captha')
def captha():
    text, img = Captcha.gen_graph_captcha()
    session['code'] = text
    out = BytesIO()
    img.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp