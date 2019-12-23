# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.


class Blog(models.Model):
    '''
    博客
    '''
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __unicode__(self):      # __str__ on Python 3
        return self.name


class Author(models.Model):
    '''
    作者
    '''
    name = models.CharField(max_length=50)
    qq = models.CharField(max_length=10)
    addr = models.TextField()
    email = models.EmailField()

    def __unicode__(self):  # __str__ on Python 3
        return self.name


class Entry(models.Model):

    blog = models.ForeignKey(Blog)              # 属于一对多的关系，即一个entry对应多个blog，
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)    # entry与author是多对多的关系， 通过modles.ManyToManyField()实现。
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __unicode__(self):  # __str__ on Python 3
        return self.headline


@python_2_unicode_compatible
class Article(models.Model):
    '''
    文章
    '''
    title = models.CharField(u'标题', max_length=50)
    # 这里有一个需要注意的地方，第一次创建的时候，在Book类的author字段的第二个参数我没有添加on_delete = models.CASCADE
    # 在使用python manage.pymakeigrations进行迁移的时候的出错了，报错如下：
    # 经过筛查，在创建多对一的关系的, 需要在Foreign的第二参数中加入on_delete=models.CASCADE
    # 主外关系键中，级联删除，也就是当删除主表的数据时候从表中的数据也随着一起删除
    author = models.ForeignKey(Author, on_delete=models.CASCADE)    # 使用Foreign关键字创建多对一的关系，Foreign(外键所在类对象的名字)
    content = models.TextField(u'内容')
    pub_date = models.DateTimeField(u'发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)
    score = models.IntegerField()   # 文章的打分
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title

    # def __unicode__(self):  # 在Python3中用 __str__ 代替 __unicode__
    #     return self.title


class Tag(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# 比较简单，假设一篇文章只有一个作者(Author)，一个作者可以有多篇文章(Article)，一篇文章可以有多个标签（Tag)。
# 创建 migrations 然后 migrate 在数据库中生成相应的表
# python manage.py makemigrations
# python manage.py migrate


# list_display 就是来配置要显示的字段的，当然也可以显示非字段内容，或者字段相关的内容，比如：
class Person(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def my_property(self):
        return self.first_name + ' ' + self.last_name

    my_property.short_description = "Full name of the person"

    full_name = property(my_property)