# -*- coding:utf-8 -*-
#
# 开发人员 ： sunshenggang
# 开始时间 ： 19-6-20 下午8:48
# 开发工具 ： PyCharm Community Edition
from flask import Flask
from app import create_app, db
from flask_script import Manager,  Shell
from  flask_migrate import Migrate, MigrateCommand
from app.models import *
app = create_app('default')


#def
manger = Manager(app)  #添加扩展，可以在命令启动
migrate = Migrate(app, db)

def make_shell_contxt():
    return dict(app=app, db=db)

manger.add_command('shell',Shell(make_context=make_shell_contxt))
manger.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manger.run()



