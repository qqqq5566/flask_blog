# -*- coding:utf-8 -*-
#
# 开发人员 ： sunshenggang
# 开始时间 ： 19-6-20 下午8:49
# 开发工具 ： PyCharm Community Edition

from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_ckeditor import CKEditor


db = SQLAlchemy() #操作数据库
bootstrap = Bootstrap() #基础模板
login_manager = LoginManager()
ckeditor = CKEditor()

login_manager.session_protection = 'strong' #提供不同等级的安全
login_manager.login_view = 'home.login' #设置登录页面的端点
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)

    #注册蓝本
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    return app

