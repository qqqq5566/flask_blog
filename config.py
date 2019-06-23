# -*- coding:utf-8 -*-
#
# 开发人员 ： sunshenggang
# 开始时间 ： 19-6-20 下午8:49
# 开发工具 ： PyCharm Community Edition

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'ssssssssss'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS  = True
    CKEDITOR_LANGUAGE = 'zh-cn'
    CKEDITOR_FILE_UPLOADER = '/upload'
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_HEIGHT = 500
    UP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app/static/uploads/")  # 文件上传路径
    FC_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app/static/uploads/users/")  # 用户头像上传路径

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/flask'


class TestingConfig(Config):
    pass

class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}