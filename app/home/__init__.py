# -*- coding:utf-8 -*-
#
# 开发人员 ： sunshenggang
# 开始时间 ： 19-6-20 下午9:16
# 开发工具 ： PyCharm Community Edition
from flask import Blueprint

home = Blueprint('home', __name__)
from .errors import *
from .user import views
from .article import views