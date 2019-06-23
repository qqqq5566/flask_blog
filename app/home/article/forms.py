# -*- coding:utf-8 -*-
#
# 开发人员 ： sunshenggang
# 开始时间 ： 19-6-22 下午2:00
# 开发工具 ： PyCharm Community Edition
from  flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, SelectField, RadioField, FileField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_ckeditor import CKEditorField
from app.models import Article

class ArticleForm(FlaskForm):
    title = StringField(
        label='标题',
        validators=[
            DataRequired('不能为空')
        ],
        render_kw={
            'class':'form-control',
            'id':'title'
        }
    )
    file = FileField(
        label='封面',
    )
    body =CKEditorField(
        label='内容',
        validators=[
            DataRequired('不能为空'),
        ],
        render_kw={
            'rows':5,
            'id':'body',
            'class': 'form-control'
        }
    )
    category = SelectField(
        label='类别',
        coerce=int,
        validators=[
            DataRequired('不能为空')
        ],
        render_kw={
            'id':'category',
            'class':'form-control'
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-primary btn-lg'
        }
    )

    def validate_title(self, field):
        """验证标题是否重复"""
        title = field.data

        title_count = Article.query.filter_by(title=title).count()
        if title_count == 1:
            raise ValidationError('标题重复')




