# -*- coding:utf-8 -*-
#
# 开发人员 ： sunshenggang
# 开始时间 ： 19-6-20 下午10:07
# 开发工具 ： PyCharm Community Edition
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField, RadioField, FileField, PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired, ValidationError, Length, Regexp
from app import db
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import current_user
from flask import session

class LoginForm(FlaskForm):
    """用户登录表单"""
    username = StringField(
        label='用户名',
        validators=[
            DataRequired('用户名不能为空')
        ],
        description='用户名',
        render_kw={
            'placeholder':'请输入用户名',
            'id': 'loginModalUserNmae',
            'class':'form-control'
        }
    )

    password = PasswordField(
        label="密码",
        validators=[
            DataRequired('密码不能为空')
        ],
        description='密码',
        render_kw={
            'placeholder':'请输入密码',
            'id': 'loginModalUserPwd',
            'class': 'form-control'
        }
    )
    submit = SubmitField(
        "登录"
    )

    def validate_username(self, field):
        username = field.data
        user = User.query.filter_by(username=username).count()
        if user == 0:
            raise ValidationError('用户名不正确')


class RegisterForm(FlaskForm):
    username = StringField(
        label='用户名',
        validators=[
            DataRequired('用户名不能为空'),
            Length(5,20, '长度在5~20之间'),
        ],
        description='用户名',
        render_kw={
            'placeholder':'请输入用户名',
            'class':'txt03 f-r3 required'
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('不能为空'),
            Email('请输入正确的格式')
        ],
        description='邮箱',
        render_kw={
            'class': 'txt03 f-r3 required'
        }
    )
    mobile = StringField(
        label='手机号',
        validators=[
            DataRequired('不能为空'),
            Length(11,11,'长度不对'),
            Regexp('^1[378]\d{3,11}',0,message='格式不正确')
        ],
        render_kw={
            'class': 'txt03 f-r3 required'
        }
    )
    password = PasswordField(
        label='密码',
        validators=[
            DataRequired('不能为空'),
        ],
        render_kw={
            'class': 'txt03 f-r3 required'
        }
    )
    repassword = PasswordField(
        label='重复密码',
        validators=[
            DataRequired('不能为空'),
            EqualTo('password','两次密码不一致')
        ],
        render_kw={
            'class': 'txt03 f-r3 required'
        }
    )
    vercode = StringField(
        label='验证码',
    )
    submit = SubmitField(
        '注册',
        render_kw={
            'class':'btn-blue f-r3 btn'
        }
    )

    def validate_username(self, field):
        """验证用户是否重复"""
        username = field.data

        user_count = User.query.filter_by(username=username).count()

        if user_count >= 1:
            raise ValidationError('用户名重复')


    def validate_email(self, filed):
        """验证邮箱是否注册"""
        email = filed.data

        user_count = User.query.filter_by(email=email).count()
        if user_count >= 1:
            raise ValidationError('邮箱已经注册')


    # def validate_vercode(self,field):
    #     vercode = field.data
    #
    #     if vercode != session['code']:
    #         return ValidationError('验证码不正确')

class PasswordForm(FlaskForm):
    oldPassword = PasswordField(
        label='旧密码',
        validators=[
            DataRequired('不能 为空')
        ],
        description='旧密码'
    )
    password = PasswordField(
        label='新密码',
        validators=[
            DataRequired('不能 为空')
        ],
        description='新密码'
    )

    rePassword = PasswordField(
        label='重复密码',
        validators=[
            DataRequired('不能 为空'),
            EqualTo('password','两次数据密码不一致')
        ],
        description='重复密码'
    )

    submit = SubmitField(
        '提交'
    )

    def validate_oldPassword(self, field):
        """验证旧密码是否正确"""
        oldPassword = field.data

        if not check_password_hash(current_user.password, oldPassword):
            raise ValidationError('旧密码错误')

class ForgetpasswordForm(FlaskForm):
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('不能为空'),
            Email('格式不正确')
        ],
        description='邮箱',
        render_kw={
            'placeholder':'请输入邮箱'
        }
    )
    password = PasswordField(
        label='密码',
        validators=[
            DataRequired('不能为空'),
            Length(4,30,'长度范围4~30个字符')
        ],
        description='密码',
        render_kw={
            'placeholder':'请输入密码'
        }
    )
    repassword = PasswordField(
        label='重复密码',
        validators=[
            DataRequired('不能为空'),
            EqualTo('password','两次密码不一致')
        ],
        description='重复密码',
        render_kw={
            'placeholder':'请输入重复密码'
        }
    )

    def validate_email(self, filed):
        """验证邮箱是否存在"""
        email = filed.data

        user_count = User.query.filter_by(email=email).count()
        if user_count == 0:
            raise ValidationError('邮箱不存在')
