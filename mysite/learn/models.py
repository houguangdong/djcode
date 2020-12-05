# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# Django 1.7 及以上的版本需要用以下命令
# python manage.py makemigrations
# python manage.py migrate

# python manage.py shell

class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()

    def __unicode__(self):
        # 在Python3中使用 def __str__(self):
        return self.name


# 新建一个对象的方法有以下几种：
# Person.objects.create(name=name,age=age)
# p = Person(name="WZ", age=23)
# p.save()
# p = Person(name="TWZ")
# p.age = 23
# p.save()
# Person.objects.get_or_create(name="WZT", age=23)
# 这种方法是防止重复很好的方法，但是速度要相对慢些，返回一个元组，第一个为Person对象，第二个为True或False, 新建时返回的是True, 已经存在时返回False.


# 获取对象有以下方法：
# Person.objects.all()
# Person.objects.all()[:10] 切片操作，获取10个人，不支持负索引，切片可以节约内存
# Person.objects.get(name=name)


# get是用来获取一个对象的，如果需要获取满足条件的一些人，就要用到filter
# Person.objects.filter(name="abc")  # 等于Person.objects.filter(name__exact="abc") 名称严格等于 "abc" 的人
# Person.objects.filter(name__iexact="abc")  # 名称为 abc 但是不区分大小写，可以找到 ABC, Abc, aBC，这些都符合条件
# Person.objects.filter(name__contains="abc")  # 名称中包含 "abc"的人
# Person.objects.filter(name__icontains="abc")  #名称中包含 "abc"，且abc不区分大小写
# Person.objects.filter(name__regex="^abc")  # 正则表达式查询
# Person.objects.filter(name__iregex="^abc")  # 正则表达式不区分大小写


# filter是找出满足条件的，当然也有排除符合某条件的
# Person.objects.exclude(name__contains="WZ")  # 排除包含 WZ 的Person对象
# Person.objects.filter(name__contains="abc").exclude(age=23)  # 找出名称含有abc, 但是排除年龄是23岁的


class Order(models.Model):

    orderid = models.CharField(max_length=64, unique=True)
    desc = models.CharField(max_length=512)
    product = models.CharField(max_length=512, null=True)
    amount = models.IntegerField()
    userid = models.CharField(max_length=512, null=True)
    create_time = models.DateTimeField(db_index=True)


# 1. F() ---- 专门取对象中某列值的操作
from django.db.models import F
order = Order.objects.get(orderid='123456789')
order.amount = F('amount') - 1
order.save()

# 需要注意的是在使用上述方法更新过数据之后需要重新加载数据来使数据库中的值与程序中的值对应：
# order= Order.objects.get(pk=order.pk)
# 或者使用更加简单的方法：
# order.refresh_from_db()

# Q对象可以通过 &（与）、 |（或）、 ~（非）运算来组合生成不同的Q对象，便于在查询操作中灵活地运用。
from django.db.models import Q

# Order.objects.get(Q(desc__startswith='Who'), Q(create_time=date(2016, 10, 2)) | Q(create_time=date(2016, 10, 6)))
# 转换成sql语句，大致如下：
# SELECT * from core_order WHERE desc LIKE 'Who%' AND (create_time = '2016-10-02' OR create_time = '2016-10-06')
# Q对象可以与关键字参数查询一起使用，不过一定要把Q对象放在关键字参数查询的前面。
# 正确写法：
# Order.objects.get( Q(create_time=date(2016, 10, 2)) | Q(create_time=date(2016, 10, 6)) desc__startswith='Who', )
# 错误写法：
# Order.objects.get( desc__startswith='Who', Q(create_time=date(2016, 10, 2)) | Q(create_time=date(2016, 10, 6)) )

# 并且条件:与条件查询
# models.User.objects.filter(条件1,条件2,条件n..)
# models.User.objects.filter(Q(username='老王') & Q(userpass='admin'))

# 或者条件:或条件
# models.User.objects.fliter(Q(username='老王') | Q(username='老李'))

# 取反条件
# models.User.objects.filter(~Q(username='老王'))
# models.User.objects.exclude(username='老王')