#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/19 16:55

# Django 用户注册系统 1.6
# 直接上代码，下载代码自己跑起来看看。
# 链接: https://pan.baidu.com/s/1fCXe9rTZdHjnvf2sPDla4g
# 密码: 9fm3
# 下面的需要更新，建议不要看，可以大致浏览下，其它可参考的实现 django-user-accounts, django-userena。
# Django 的源码中已经有登陆，退出，重设密码等相关的视图函数，在下面这个 app 中
# django.contrib.auth

# 一，创建一个 zqxt_auth 项目
# django-admin startproject zqxt_auth

# 打开 zqxt_auth/setting.py 可以看到 django.contrib.auth 已经在 INSTALLED_APPS 中 ：
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
# ]
# 注：各版本的Django生成的文件可能有些差异，请按照你的 Django 版本为准。


# 二，修改 urls.py 【此步阅读即可，不需要照着做】
# from django.conf.urls import url, include
# from django.contrib import admin
# from django.contrib.auth import urls as auth_urls
#
# urlpatterns = [
#     url(r'^accounts/', include(auth_urls, namespace='accounts')),
#     url(r'^admin/', admin.site.urls),
# ]
# 我们引入了 django.contrib.auth.urls 中的内容，改好后，我们试着访问一下：
# http://127.0.0.1:8000/accounts/login/  报错信息说：
# 下面我们的任务就是弄一些相关的模板了。
# 三，准备相关的模板文件【此步阅读即可，不需要照着做】
# Django默认配置下会自动寻找 app 下的模板，但是 django.contrib.auth 这个是官方提供的，我们修改这个 app 不太容易，我们可以建立一个公用的模板文件夹。
# 3.1 添加一个公用的放模板的文件夹
# Django 1.8 及以上的版本 settings.py，修改 TEMPLATES 中的 DIRS
# TEMPLATES = [
#     {
#         ...
#         'DIRS': [os.path.join(BASE_DIR, 'templates')],
#         ...
#     },
# ]
# Django 1.7 及以下的版本，修改 TEMPLATE_DIRS：
# TEMPLATE_DIRS = (
#     os.path.join(BASE_DIR, 'templates'),
# )
# 注：如果是旧的项目已经存在公用的，可以不添加上面的目录
# 这个文件夹需要我们手工创建出来，创建后如下：
# tree .

# 3.2 模板文件
# 熟悉Django的同学知道，Django 的后台是有登陆，重设密码的功能，那么在 django.contrib.admin 中应该是有相应的模板文件的，一找，果然有，查看链接。

# 我们把这些文件拷贝出来。
# 需要注意的是，有人已经按照类似的方法，做成了一个包了，地址在这里：https://github.com/mishbahr/django-users2
# 这个包比较完善了，我们没必要重新发明轮子，上面的示例只是让你明白，这个包其实是由官方的django.contrib.auth 改进后做出来的。
# 四，用 django-users2 这个包来实现登陆注册及找回密码等功能。
# django-users2 这个包在 Django 1.5 - Django 1.9 中使用都没有问题。

# 4.1 安装
# pip install django-users2
# 4.2 把 users 这个 app 加入到 INSTALLED_APPS
# INSTALLED_APPS = (
#     ...
# 'django.contrib.auth',
# 'django.contrib.sites',
# 'users',
# ...
# )
#
#
# AUTH_USER_MODEL = 'users.User'
# AUTH_USER_MODEL 是替换成自定义的用户认证。参考这里

# 4.3 修改 urls.py
# urlpatterns = patterns('',
#     ...
#     url(r'^accounts/', include('users.urls')),
#     ...
# )

# 4.4 同步数据，创建相应的表
# python manage.py syncdb
#
# Django 1.7 及以上
# python manage.py makemigrations
# python manage.py migrate

# 4.5 配置登陆注册的一些选项，找密码时发邮件的邮箱
# 下面的代码加在 settings.py 最后面
# USERS_REGISTRATION_OPEN = True
#
# USERS_VERIFY_EMAIL = True
#
# USERS_AUTO_LOGIN_ON_ACTIVATION = True
#
# USERS_EMAIL_CONFIRMATION_TIMEOUT_DAYS = 3
#
# # Specifies minimum length for passwords:
# USERS_PASSWORD_MIN_LENGTH = 5
#
# # Specifies maximum length for passwords:
# USERS_PASSWORD_MAX_LENGTH = None
#
# # the complexity validator, checks the password strength
# USERS_CHECK_PASSWORD_COMPLEXITY = True
#
# USERS_SPAM_PROTECTION = False  # important!
#
# #  ---------------------------------------------------------
# #  Email
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#
# EMAIL_USE_TLS = False
# EMAIL_HOST = 'smtp.tuweizhong.com'
# EMAIL_PORT = 25
# EMAIL_HOST_USER = 'mail@tuweizhong.com'
# EMAIL_HOST_PASSWORD = 'xxxx'
# DEFAULT_FROM_EMAIL = 'mail@tuweizhong.com'
#  ---------------------------------------------------------
# 这样登陆注册和找回密码功能应该就没有问题了。