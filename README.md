# flask_blog
[测试网址](http://www.huaweiappshop.com)

## 安装虚拟环境
在目录下面安装
```
pip install virtualenv
```
##安装第三方模块
```
pip install -r requirement.txt
```

## 修改config.py
把链接数据库的地方修改成自己的

## 数据库迁移
python manager.py db init

python manager.py db migrate

python manager.py db upgrade

## 启动
python manager.py runserver



