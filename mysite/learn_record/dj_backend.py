#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/12 11:26

# Django 后台
# django的后台我们只要加少些代码，就可以实现强大的功能。
# 与后台相关文件：每个app中的 admin.py 文件与后台相关。

# 下面示例是做一个后台添加博客文章的例子：
# 一，新建一个 名称为 zqxt_admin 的项目
# django-admin.py startproject zqxt_admin
# 二，新建一个 叫做 blog 的app
# 进入 zqxt_admin 文件夹
# cd zqxt_admin
# 创建 blog 这个 app
# python manage.py startapp blog

# 三，修改 blog 文件夹中的 models.py
# coding:utf-8
from django.db import models


class Article(models.Model):
    title = models.CharField(u'标题', max_length=256)
    content = models.TextField(u'内容')

    pub_date = models.DateTimeField(u'发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)


# 四，把 blog 加入到settings.py中的INSTALLED_APPS中
# 五，同步所有的数据表
# 进入包含有 manage.py 的文件夹
# python manage.py makemigrations
# python manage.py migrate

# 注意：Django 1.6.x 及以下的版本需要用以下命令
# python manage.py syncdb

# 如果是 Django 不主动提示创建管理员（Django 1.9不提示）用下面的命令创建一个帐号
# python manage.py createsuperuser

# 六，修改 admin.py
# 进入 blog 文件夹，修改 admin.py 文件（如果没有新建一个），内容如下
from django.contrib import admin
from blog.models import Article
admin.site.register(Article)
# 只需要这三行代码，我们就可以拥有一个强大的后台！
# 提示：urls.py中关于 admin的已经默认开启，如果没有，参考这里。

# 七，打开 开发服务器
# python manage.py runserver
# 如果提示 8000 端口已经被占用，可以用 python manage.py runserver 8001 以此类推

# 访问 http://localhost:8000/admin/ 输入设定的帐号和密码, 就可以看到：
# 点击 Articles，动手输入 添加几篇文章，就可以看到：
# 我们会发现所有的文章都是叫 Article object，这样肯定不好，比如我们要修改，如何知道要修改哪个呢？
# 我们加了一个 __unicode__ 函数，
# 所以推荐定义 Model 的时候 写一个 __unicode__ 函数(或 __str__函数)

# 技能提升：如何兼容python2.x和python3.x呢？
# python_2_unicode_compatible 会自动做一些处理去适应python不同的版本，
# 本例中的 unicode_literals 可以让python2.x 也像 python3 那个处理 unicode 字符，以便有更好地兼容性。

# 八，在列表显示与字段相关的其它内容
# 后台已经基本上做出来了，可是如果我们还需要显示一些其它的fields，如何做呢？
# from django.contrib import admin
# from blog.models import Article
#
#
# class ArticleAdmin(admin.ModelAdmin):
#     list_display = ('title', 'pub_date', 'update_time',)
#
#
# admin.site.register(Article, ArticleAdmin)
# list_display 就是来配置要显示的字段的，当然也可以显示非字段内容，或者字段相关的内容，比如：
# class Person(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#
#     def my_property(self):
#         return self.first_name + ' ' + self.last_name
#
#     my_property.short_description = "Full name of the person"
#
#     full_name = property(my_property)


# 在admin.py中
# from django.contrib import admin
# from blog.models import Article, Person
#
# class ArticleAdmin(admin.ModelAdmin):
#     list_display = ('title', 'pub_date', 'update_time',)
#
#
# class PersonAdmin(admin.ModelAdmin):
#     list_display = ('full_name',)
#
#
# admin.site.register(Article, ArticleAdmin)
# admin.site.register(Person, PersonAdmin)


# 到这里我们发现我们又有新的需求，比如要改 models.py 中的字段，添加一个文章的状态（草稿，正式发布），
# 这时候我们就需要更改表，django 1.7以前的都不会自动更改表，我们需要用第三方插件 South，参见 Django 迁移数据。
# Django 1.7 及以上用以下命令来同步数据库表的更改
# python manage.py makemigrations
# python manage.py migrate

# 其它一些常用的功能：
# 搜索功能：search_fields = ('title', 'content',) 这样就可以按照 标题或内容搜索了
# https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
# 筛选功能：list_filter = ('status',) 这样就可以根据文章的状态去筛选，比如找出是草稿的文章
# https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
# 新增或修改时的布局顺序：https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets

# 有时候我们需要对django admin site进行修改以满足自己的需求，那么我们可以从哪些地方入手呢？
# 以下举例说明：
# 1.定制加载的列表, 根据不同的人显示不同的内容列表，比如输入员只能看见自己输入的，审核员能看到所有的草稿，这时候就需要重写get_queryset方法
