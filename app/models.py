# -*- coding:utf-8 -*-
#
# 开发人员 ： sunshenggang
# 开始时间 ： 19-6-20 下午9:55
# 开发工具 ： PyCharm Community Edition
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    mobile = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, default=datetime.now)
    state = db.Column(db.Integer, default=1, comment='状态 1--有效 0--无效')

    Articles = db.relationship('Article', backref='user')
    def __repr__(self):
        return '<User %r>'% self.username
    # @property
    # def password(self):
    #     raise AttributeError('password not read')
    #
    # @password.setter
    # def password(self,password):
    #     self.password = generate_password_hash(password)


    def verify_password(self,pwd):
        """验证密码是否正确"""
        return check_password_hash(self.password, pwd)

class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, comment='文章标题')
    cover_url = db.Column(db.String(100), comment='封面链接')
    content = db.Column(db.Text, nullable=False, comment='文章内容')
    add_time = db.Column(db.DateTime, default=datetime.now, comment='添加时间')
    state = db.Column(db.SmallInteger, default=1, comment='状态 1---有效 0--无效')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return '<Article %r>' % self.title


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, comment='名称')
    pid = db.Column(db.Integer, default=0, comment='父id')
    add_time = db.Column(db.DateTime, default=datetime.now)
    state=db.Column(db.SmallInteger, default=1 ,comment='1--有效 0--无效')
    sort = db.Column(db.SmallInteger,default=0, comment='排序')
    article = db.relationship('Article', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.name