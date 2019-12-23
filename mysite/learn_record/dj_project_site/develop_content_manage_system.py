#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/23 18:08

# Django 开发内容管理系统
# 用Django开发一个简易的内容管理系统，比如显示新闻的列表，点击进去可以看内容详情等，新闻发布网站。
# 一，搭建互不干扰的 Python 包开发环境
# 我们有的时候会发现，一个电脑上有多个项目，一个依赖 Django 1.8，另一个比较旧的项目又要用 Django 1.5，这时候怎么办呢？
# 我们需要一个依赖包管理的工具来处理不同的环境。如果不想搭建这个环境，可以直接去看 2.2
# 1.1 环境搭建
# 开发会用 virtualenv 来管理多个开发环境，virtualenvwrapper 使得virtualenv变得更好用
# 安装:
# (sudo) pip install virtualenv virtualenvwrapper
# Linux/Mac OSX 下：
# 修改~/.bash_profile或其它环境变量相关文件，添加以下语句
# export WORKON_HOME=$HOME/.virtualenvs
# export PROJECT_HOME=$HOME/workspace
# source /usr/local/bin/virtualenvwrapper.sh
# Windows 下：
# pip install virtualenvwrapper-win
# 【可选】Windows下默认虚拟环境是放在用户名下面的Envs中的，与桌面，我的文档，下载等文件夹在一块的。更改方法：计算机，属性，高级系统设置，环境变量，添加WORKON_HOME，如图（windows 10 环境变量设置截图）：
# 1.2 使用方法：
# mkvirtualenv zqxt：创建运行环境zqxt
# workon zqxt: 工作在 zqxt 环境
# 其它的：
# rmvirtualenv ENV：删除运行环境ENV
# mkproject mic：创建mic项目和运行环境mic
# mktmpenv：创建临时运行环境
# lsvirtualenv: 列出可用的运行环境
# lssitepackages: 列出当前环境安装了的包
# 创建的环境是独立的，互不干扰，无需sudo权限即可使用 pip 来进行包的管理。
# 二，安装软件，开发 minicms 项目
# 2.1 创建一个开发环境 minicms
# Linux 或 Mac OSX
# mkproject minicms

# windows
# mkvirtualenv minicms

# Mac OSX 下的输出示例：
# mkproject minicms
# 2.2 安装 Django
# pip install Django==1.8.3
# 2.3 创建项目 minicms 和 应用 news
# django-admin.py startproject minicms
# cd minicms
# python manage.py startapp news
# 添加 news 到 settings.py 中的 INSTALLED_APPS 中。
# 2.4 规划 news 中的栏目和每篇文章相关的字段
# 栏目：名称，网址，简介等
# 文章：标题，作者，网址，内容等
# 我们假设一篇文章只有一个作者（文章和作者是多对一的关系），一篇文章可以属于多个栏目（栏目和文章是多对多的关系）
# 为了用到更多的情况，我们假设作者可以为空，栏目不能为空。
# 开写 models.py

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Column(models.Model):
    name = models.CharField('栏目名称', max_length=256)
    slug = models.CharField('栏目网址', max_length=256, db_index=True)
    intro = models.TextField('栏目简介', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '栏目'
        verbose_name_plural = '栏目'
        ordering = ['name']  # 按照哪个栏目排序


@python_2_unicode_compatible
class Article(models.Model):
    column = models.ManyToManyField(Column, verbose_name='归属栏目')

    title = models.CharField('标题', max_length=256)
    slug = models.CharField('网址', max_length=256, db_index=True)

    author = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='作者')
    content = models.TextField('内容', default='', blank=True)

    published = models.BooleanField('正式发布', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '教程'
        verbose_name_plural = '教程'


# 2.5 创建数据库
# python manage.py makemigrations news
# python manage.py migrate
#
# 2.6 创建完数据库后，用了一段时间，我们发现以前的文章的字段不合理
# 比如我们想记录文章添加的日期，修改的日期，我们更改 models.py （不变动的大部分省去了，添加两个字段）
# class Article(models.Model):
#
#     pub_date = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
#     update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

# 这时候，我们对 models.py 进行了更改，这些字段数据库中还没有，我们要同步更改到数据库中去：
# python manage.py makemigrations news
# 这段话的意思是 pub_date 字段没有默认值，而且非Null 那么
# 1) 指定一个一次性的值供更改数据库时使用。
# 2) 停止当前操作，在 models.py 中给定默认值，然后再来migrate。
# 我们选择第一个，输入 1
# Select an option: 1
# timezone.now()
# 这样是生成了一个对表进行更改的 py 文件在 news/migrations 文件夹中，我们要执行更改
# python manage.py migrate 或 python manage.py migrate news

# 2.7 创建一个脚本，导入一些数据到数据库中
# 我们导入一些演示数据：
# 栏目： [<Column: 体育新闻>, <Column: 社会新闻>, <Column: 科技新闻>]
# 文章：[<Article: 体育新闻_1>, <Article: 体育新闻_2>, <Article: 体育新闻_3>, <Article: 体育新闻_4>, <Article: 体育新闻_5>,
        # <Article: 体育新闻会>, <Article: 体育新闻_7>, <Article: 体育新闻_8>, <Article: 体育新闻_9>, <Article: 体育新闻_10>,
        # <Article: 社会新闻_1>, <Article: 社新闻_2>,'...(remaining elements truncated)...']

# create_demo_records.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-07-28 20:38:38
# @Author  : Weizhong Tu (mail@tuweizhong.com)
# @Link    : http://www.tuweizhong.com
#
# '''
# create some records for demo database
# '''
#
# from minicms.wsgi import *
# from news.models import Column, Article
#
#
# def main():
#     columns_urls = [
#         ('体育新闻', 'sports'),
#         ('社会新闻', 'society'),
#         ('科技新闻', 'tech'),
#     ]
#
#     for column_name, url in columns_urls:
#         c = Column.objects.get_or_create(name=column_name, slug=url)[0]
#
#         # 创建 10 篇新闻
#         for i in range(1, 11):
#             article = Article.objects.get_or_create(
#                 title='{}_{}'.format(column_name, i),
#                 slug='article_{}'.format(i),
#                 content='新闻详细内容： {} {}'.format(column_name, i)
#             )[0]
#
#             article.column.add(c)
#
#
# if __name__ == '__main__':
#     main()
#     print("Done!")
# 假设这个文件被保存为 create_demo_records.py （和 manage.py 放在一块，同一个文件夹下）
# 运行脚本 导入数据：
# python create_demo_records.py
# Done!
# 终端上显示一个  Done!   就这样 Duang 的一下，数据就导进去了！
# 第一次提交：github: https://github.com/twz915/django-minicms/tree/dff31758173852344af5d8d5b4fad858a0b16907
# 内容管理系统继续开发，点此查看第二部分