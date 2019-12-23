#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/23 15:48

# Django 上下文渲染器
# 有时候我们想让一些内容在多个模板中都要有，比如导航内容，我们又不想每个视图函数都写一次这些变量内容，怎么办呢？
# 这时候就可以用 Django 上下文渲染器来解决。
# 一，初识上下文渲染器
# 我们从视图函数说起，在 views.py 中返回字典在模板中使用:
from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {'info': 'Welcome to ziqiangxuetang.com !'})

# 这样我们就可以在模板中使用 info 这个变量了。
# {{ info }}

# 模板对应的地方就会显示：Welcome to ziqiangxuetang.com !
# 但是如果我们有一个变量，比如用户的IP，想显示在网站的每个网页上。再比如显示一些导航信息在每个网页上，该怎么做呢？
# 一种方法是用死代码，直接把栏目固定写在 模块中，这个对于不经常变动的来说也是一个办法，简单高效。
# 但是像用户IP这样的因人而异的，或者经常变动的，就不得不想一个更好的解决办法了。
# 由于上下文渲染器API在Django 1.8 时发生了变化，被移动到了 tempate 文件夹下，所以讲解的时候分两种，一种是 Django 1.8 及以后的，和Django 1.7及以前的。
# 我们来看Django官方自带的小例子：
# Django 1.8 版本：
# django.template.context_processors 中有这样一个函数
def request(request):
    return {'request': request}

# Django 1.7 及以前的代码在这里：django.core.context_processors.request 函数是一样的。
# 在settings.py 中：
# Django 1.8 版本 settings.py:
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Django 1.7 版本 settings.py 默认是这样的：
# TEMPLATE_CONTEXT_PROCESSORS = (
#     "django.contrib.auth.context_processors.auth",
#     "django.core.context_processors.debug",
#     "django.core.context_processors.i18n",
#     "django.core.context_processors.media",
#     "django.core.context_processors.static",
#     "django.core.context_processors.tz",
#     "django.contrib.messages.context_processors.messages"
# )
#
# 我们可以手动添加 request 的渲染器
# TEMPLATE_CONTEXT_PROCESSORS = (
#     "django.core.context_processors.request",
# )

# 这里的 context_processors 中放了一系列的 渲染器，上下文渲染器 其实就是函数返回字典，字典的 keys 可以用在模板中。
# request 函数就是在返回一个字典，每一个模板中都可以使用这个字典中提供的 request 变量。
# 比如 在template 中 获取当前访问的用户的用户名：
# User Name: {{ request.user.username }}

# 二，动手写个上下文渲染器
# 2.1 新建一个项目，基于 Django 1.8，低版本的请自行修改对应地方：
# django-admin.py startproject zqxt
# cd zqxt
# python manage.py startapp blog
# 我们新建了 zqxt 项目和 blog 这个应用。
# 把 blog 这个app 加入到 settings.py 中
# INSTALLED_APPS = (
#     'django.contrib.admin',
#     'blog',
# )
# 整个项目当前目录结构如下：
# 2.2 我们在 zqxt/zqxt/ 这个目录下（与settings.py 在一起）新建一个 context_processor.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-10-31 14:26:26
# @Author  : Weizhong Tu (mail@tuweizhong.com)

from django.conf import settings as original_settings


def settings(request):
    return {'settings': original_settings}


def ip_address(request):
    return {'ip_address': request.META['REMOTE_ADDR']}


# 2.3 我们把新建的两个 上下文渲染器 加入到 settings.py 中：
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#
#                 'zqxt.context_processor.settings',
#                 'zqxt.context_processor.ip_address',
#             ],
#         },
#     },
# ]
# 最后面两个是我们新加入的，我们稍后在模板中测试它。

# 2.4 修改 blog/views.py
# from django.shortcuts import render
#
#
# def index(reuqest):
#     return render(reuqest, 'blog/index.html')
#
#
# def columns(request):
#     return render(request, 'blog/columns.html')
#
# 2.5 新建两个模板文件，放在 zqxt/blog/templates/blog/ 中
# index.html
# <h1> Blog Home Page </h1>
# DEBUG: {{settings.DEBUG}}
# ip: {{ip_address}}

# columns.html
# <h1>Blog Columns</h1>
# DEBUG: {{settings.DEBUG}}
# ip: {{ip_address}}

# 2.6 修改 zqxt/urls.py
# from django.conf.urls import include, url
# from django.contrib import admin
# from blog import views as blog_views
#
# urlpatterns = [
#     url(r'^blog_home/$', blog_views.index),
#     url(r'^blog_columns/$', blog_views.columns),
#     url(r'^admin/', include(admin.site.urls)),
# ]
#
# 2.7 打开开发服务器并访问，进行测试吧：
# python manage.py runserver
# 就会看到所有的模板都可以使用 settings 和 ip_address 变量：
# http://127.0.0.1:8000/blog_home/
# http://127.0.0.1:8000/blog_columns/