#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/20 22:55

# Django ORM
# 本文介绍如何只使用Django的数据库。
# Django 的数据库接口非常好用，我们甚至不需要知道SQL语句如何书写，就可以轻松地查询，创建一些内容，所以有时候想，在其它的地方使用Django的 ORM呢？它有这么丰富的 QuerySet API.
# 示例代码：Django_DB.zip
# settings.py
# import os
#
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# SECRET_KEY = 'at8j8i9%=+m@topzgjzvhs#64^0&qlr6m5yc(_&me%!@jp-7y+'
#
# INSTALLED_APPS = (
#     'test',
# )
# # Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
# 在这个文件中写上 SQLite, MySQL或PostgreSQL的信息，这样就可以运用这个数据库了。
# 新建确保每个app下有一个 models.py 和 __init__.py 文件，就可以享受 Django 的 ORM 带来的便利！
# 可以用 Django QuerySet API 来创建，查询，删除，修改，不用写SQL语句。
# 更详细的请查看本文提供的源代码。