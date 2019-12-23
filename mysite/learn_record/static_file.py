#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/13 14:43

# Django 静态文件
# 静态文件是指 网站中的 js, css, 图片，视频等文件
# 开发阶段
# 推荐用新版本的Django进行开发，可以肯定的是 Django 1.4 以后的版本应该都支持下面的设置
# 注意：Django 1.4 版本需要在 project/urls.py 底部加上：
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# urlpatterns += staticfiles_urlpatterns()
# Django 1.5 - Django 1.8 不需要添加上面的代码。

# settings.py 静态文件相关示例代码及说明：
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

STATIC_URL = '/static/'

# 当运行 python manage.py collectstatic 的时候
# STATIC_ROOT 文件夹 是用来将所有STATICFILES_DIRS中所有文件夹中的文件，以及各app中static中的文件都复制过来
# 把这些文件放到一起是为了用apache等部署的时候更方便
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

# 其它 存放静态文件的文件夹，可以用来存放项目中公用的静态文件，里面不能包含 STATIC_ROOT
# 如果不想用 STATICFILES_DIRS 可以不用，都放在 app 里的 static 中也可以
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "common_static"),
    '/path/to/others/static/',  # 用不到的时候可以不写这一行
)

# 这个是默认设置，Django 默认会在 STATICFILES_DIRS中的文件夹 和 各app下的static文件夹中找文件
# 注意有先后顺序，找到了就不再继续找了
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

# 静态文件放在对应的 app 下的 static 文件夹中 或者 STATICFILES_DIRS 中的文件夹中。
# 当 DEBUG = True 时，Django 就能自动找到放在里面的静态文件。（Django 通过 STATICFILES_FINDERS 中的“查找器”，找到符合的就停下来，寻找的过程 类似于 Python 中使用 import xxx 时，找 xxx 这个包的过程）。
# 示例项目 dj18static, 应用 app 下面有一个 static 里面有一个 aaa.jpg 图片：


# settings.py 中的 DEBUG = True 时，打开开发服务器 python manage.py runserver 直接访问 /static/zqxt.png 就可以找到这个静态文件。
# 也可以在 settings.py 中指定所有 app 共用的静态文件，比如 jquery.js 等

# 其它参考办法（当你想为静态文件分配多个不同的网址时，可能会用上这个）：
# static files
# import os
# from django.conf.urls.static import static
# from django.conf import settings
# if settings.DEBUG:
#     media_root = os.path.join(settings.BASE_DIR,'media2')
#     urlpatterns += static('/media2/', document_root=media_root)
# 也可以这样
# from django.conf.urls.static import static
# urlpatterns = ...
# urlpatterns += static('/media2/', document_root=media_root)

# 部署时
# 1. 收集静态文件
# python manage.py collectstatic
# 这一句话就会把以前放在app下static中的静态文件全部拷贝到 settings.py 中设置的 STATIC_ROOT 文件夹中


# 2.用apache2或nginx示例代码
# apache2配置文件
# Alias /static/ /path/to/collected_static/
#
# <Directory /path/to/collected_static>
#     Require all granted
# </Directory>

# nginx 示例代码：
# location /media
# {
#     alias/path/to/project/media;
# }
#
# location /static
# {
#     alias/path/to/project/collected_static;
# }

# Apache 完整的示例代码：
# <VirtualHost *:80>
#     ServerName www.ziqiangxuetang.com
#     ServerAlias ziqiangxuetang.com
#     ServerAdmin tuweizhong@163.com
#
#     Alias /media/ /path/to/media/
#     Alias /static/ /path/to/collected_static/
#
#     <Directory /path/to/media>
#         Require all granted
#     </Directory>
#
#     <Directory /path/to/collected_static>
#         Require all granted
#     </Directory>
#
#     WSGIScriptAlias / /path/to/prj/prj/wsgi.py
#     <Directory /path/to/prj/prj>
#     <Files wsgi.py>
#         Require all granted
#     </Files>
#     </Directory>
# </VirtualHost>

# 如果你用的是apache 2.2 版本 用下面的代替 Require all granted 赋予权限
# Order allow,deny
# Allow from all
# 备注：（用 apachectl -v 命令查看 apache2版本号）