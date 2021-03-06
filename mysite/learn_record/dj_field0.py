#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/12 00:36

# Django 的官方提供了很多的 Field，但是有时候还是不能满足我们的需求，不过Django提供了自定义 Field 的方法：
# 提示：如果现在用不到可以跳过这一节，不影响后面的学习，等用到的时候再来学习不迟。
# 来一个简单的例子吧。
# 1. 减少文本的长度，保存数据的时候压缩，读取的时候解压缩，如果发现压缩后更长，就用原文本直接存储：
# Django 1.7 以下
# from django.db import models
#
#
# class CompressedTextField(models.TextField):
#     """model Fields for storing text in a compressed format (bz2 by default)    """
#     __metaclass__ = models.SubfieldBase
#
#     def to_python(self, value):
#         if not value:
#             return value
#         try:
#             return value.decode('base64').decode('bz2').decode('utf-8')
#         except Exception:
#             return value
#
#     def get_prep_value(self, value):
#         if not value:
#             return value
#         try:
#             value.decode('base64')
#             return value
#         except Exception:
#             try:
#                 tmp = value.encode('utf-8').encode('bz2').encode('base64')
#             except Exception:
#                 return value
#             else:
#                 if len(tmp) > len(value):
#                     return value
#                 return tmp
#
# to_python 函数用于转化数据库中的字符到 Python的变量， get_prep_value 用于将Python变量处理后(此处为压缩）保存到数据库，使用和Django自带的 Field 一样。

# Django 1.8 以上版本，可以用
# coding:utf-8
from django.db import models


# class CompressedTextField(models.TextField):
#     """
#     model Fields for storing text in a compressed format (bz2 by default)
#     """
#     def from_db_value(self, value, expression, connection, context):
#         if not value:
#             return value
#         try:
#             return value.decode('base64').decode('bz2').decode('utf-8')
#         except Exception:
#             return value
#
#     def to_python(self, value):
#         if not value:
#             return value
#         try:
#             return value.decode('base64').decode('bz2').decode('utf-8')
#         except Exception:
#             return value
#
#     def get_prep_value(self, value):
#         if not value:
#             return value
#         try:
#             value.decode('base64')
#             return value
#         except Exception:
#             try:
#                 return value.encode('utf-8').encode('bz2').encode('base64')
#             except Exception:
#                 return value
# Django 1.8及以上版本中，from_db_value 函数用于转化数据库中的字符到 Python的变量。


# 2. 比如我们想保存一个 列表到数据库中，在读取用的时候要是 Python的列表的形式，我们来自己写一个 ListField：
# 这个ListField继承自 TextField，代码如下：
from django.db import models
import ast


class ListField(models.TextField):

    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __index__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)  # use str(value) in Python 3

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


# 使用它很简单，首先导入 ListField，像自带的 Field 一样使用：
class Article(models.Model):

    labels = ListField()


# 在终端上尝试（运行 python manage.py shell 进入）：
from blog.models import Article
d = Article()
print(d.labels)
d.labels = ["Python", "Django"]
print(d.labels)

# 下载上面的代码，解压，进入项目目录，输入 python manage.py shell 搞起
from blog.models import Article
a = Article()
a.labels.append('Django')
a.labels.append('custom fields')
print(a.labels)
print(type(a.labels))
a.content = u'我正在写一篇关于自定义Django Fields的教程'
a.save()