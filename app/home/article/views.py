# -*- coding:utf-8 -*-
#
# 开发人员 ： sunshenggang
# 开始时间 ： 19-6-22 下午2:00
# 开发工具 ： PyCharm Community Edition
from app.home import home
from app import db
from flask import render_template, flash, url_for, request, current_app, send_from_directory, redirect, jsonify
from flask_login import login_required, current_user
from .forms import ArticleForm
import os
from flask_ckeditor import upload_fail, upload_success
from datetime import datetime
import random
from app.models import Article, Category, Comment



@home.route('/show/<int:id>')
def show(id):
    article = Article.query.get_or_404(id)
    if article:
        article.view_num = int(article.view_num) + 1
        db.session.commit()
    return render_template('/home/article/show.html',article=article)

@home.route('/article', methods=['GET', 'POST'])
@login_required
def article():
    """发布文章"""
    form = ArticleForm()
    form.category.choices = ( (categroy.id,categroy.name) for categroy in Category.query.filter_by(state=1).all())
    if form.validate_on_submit():
        data = form.data
        file = request.files['file']
        print(file)
        error = ''
        fname, fext = os.path.splitext(file.filename)
        if fext not in ['.jpg', '.gif', '.png', '.jpeg']:  # 验证文件类型示例
            flash('封面保存失败')
            return url_for('home.article')

        rnd_name = '%s%s' % (gen_rnd_filename(), fext)  # 新的文件名称

        filepath = os.path.join(current_app.config['UP_DIR'], rnd_name)
        dirname = os.path.dirname(filepath)  # 获取目录

        if not os.path.exists(dirname):  # 检查目录是否存在
            try:
                os.makedirs(dirname)
                os.chmod(dirname, 'rw')
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'

        if not error:
            file.save(filepath)
            url = url_for('home.uploadfile', filename=rnd_name)
            #return upload_success(url=url)  # 返回upload_success调用
        else:
            flash('封面保存失败')
            return url_for('home.article')


        article = Article(
            title = data['title'],
            content = data['body'],
            cover_url = url,
            category_id = data['category'],
            user_id = current_user.get_id()
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('home.index'))

    return render_template('home/article/post.html',form=form)

@home.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files.get('upload')
    error = ''
    fname, fext = os.path.splitext(file.filename)


    if fext not in ['.jpg', '.gif', '.png', '.jpeg']:  # 验证文件类型示例
        return upload_fail('文件类型不匹配')

    rnd_name = '%s%s' % (gen_rnd_filename(), fext) #新的文件名称

    filepath = os.path.join(current_app.config['UP_DIR'],rnd_name)
    dirname = os.path.dirname(filepath) #获取目录

    if not os.path.exists(dirname): #检查目录是否存在
        try:
            os.makedirs(dirname)
            os.chmod(dirname,'rw')
        except:
            error = 'ERROR_CREATE_DIR'
    elif not os.access(dirname, os.W_OK):
        error = 'ERROR_DIR_NOT_WRITEABLE'

    if not error:
        file.save(filepath)
        url = url_for('home.uploadfile',filename=rnd_name)
        return upload_success(url=url) # 返回upload_success调用
    else:
        return upload_fail('上传失败')

@home.route('/uploadfile/<path:filename>')
def uploadfile(filename):
    #path = os.path.join(current_app.config['UP_DIR'],filename)
    return send_from_directory(current_app.config['UP_DIR'],filename)


@home.route('/blog_list/<int:page>')
def blog_list(page=None):
    """显示文章列表"""
    if not page:
        page=1

    articleList = Article.query.order_by('add_time').filter_by(state=1).paginate(page=page, per_page=10)

    return render_template('/home/index.html', paginate=articleList)



@home.route('/category/<int:categoryId>/<int:page>')
def category(categoryId, page=None):
    if not page:
        page=1
    articleListPaginate = Article.query.filter_by(category_id=categoryId).order_by(Article.add_time.desc()).paginate(page=page,per_page=10)

    articleList = articleListPaginate.items

    return render_template('/home/article/category.html',articleList=articleList, paginate=articleListPaginate, categoryId=categoryId)

def gen_rnd_filename():
    """生产随机文件名称"""
    filename_prefix = datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@home.route('/comment/<int:articleId>', methods=['POST'])
@login_required
def comment(articleId):
    content = request.form['commentContent']
    if content:
        comment = Comment(
            user_id = current_user.get_id(),
            article_id = articleId,
            content = content
        )
        db.session.add(comment)
        db.session.commit()
        return jsonify(
            {
                'success':True,
                'errorcode':200,
                'msg':'保存成功',
                'data':{
                    'username':current_user.username,
                    't': datetime.now()
                }
            }
        )
    else:
        return jsonify(
            {
                'success': False,
                'errorcode': 301,
                'msg': '内容不能为空'
            }
        )

@home.route('/comment_list/<int:articleId>', methods=['POST'])
def comment_list(articleId):
    if articleId:
        commentList = Comment.query.filter_by(article_id=articleId).order_by(Comment.add_time.desc()).offset(0).limit(10)
        commentDIct = {}
        for comment in commentList:
            commentDIct['username'] = comment.user.username
            commentDIct['content'] = comment.content
            commentDIct['t'] = comment.add_time
        return jsonify(
            {
                'success':True,
                'errorcode':200,
                'msg':'保存成功',
                'data':commentDIct
            }
        )
    else:
        return jsonify(
            {
                'success': False,
                'errorcode': 301,
                'msg': '没有文章编号参数'
            }
        )


