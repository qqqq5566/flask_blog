# -*- coding:utf-8 -*-
#
# 开发人员 ： sunshenggang
# 开始时间 ： 19-6-20 下午9:18
# 开发工具 ： PyCharm Community Edition
from flask import render_template

from . import home

@home.app_errorhandler(404)
def page_not_found(e):
    return render_template('/home/error/404.html'), 404

@home.app_errorhandler(500)
def internal_server_error(e):
    return render_template('/home/error/500.html'), 500