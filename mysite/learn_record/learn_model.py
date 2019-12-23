#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/9 00:22

# Django 模型（数据库）
# Django 模型是与数据库相关的，与数据库相关的代码一般写在 models.py 中，Django 支持 sqlite3, MySQL, PostgreSQL等数据库，
# 只需要在settings.py中配置即可，不用更改models.py中的代码，丰富的API极大的方便了使用。
# 1. 新建项目和应用
# django-admin.py startproject learn_models # 新建一个项目
# cd learn_models # 进入到该项目的文件夹
# django-admin.py startapp people # 新建一个 people 应用（app)
# 补充：新建app也可以用 python manage.py startapp people, 需要指出的是，django-admin.py
# 是安装Django后多出的一个命令，并不是运行的当前目录下的django-admin.py（当前目录下也没有），但创建项目会生成一个 manage.py 文件。

# 2. 添加应用
# 将我们新建的应用（people）添加到 settings.py 中的 INSTALLED_APPS中，也就是告诉Django有这么一个应用。

# 3. 修改models.py
# 我们打开 people/models.py 文件，修改其中的代码如下：
# 我们新建了一个Person类，继承自models.Model, 一个人有姓名和年龄。
# 这里用到了两种Field，更多Field类型可以参考教程最后的链接。

# 4. 创建数据表
# 我们来同步一下数据库（我们使用默认的数据库 SQLite3，无需配置）
# 先cd进入manage.py所在的那个文件夹下，输入下面的命令
# Django 1.6.x 及以下
# python manage.py syncdb

# Django 1.7 及以上的版本需要用以下命令
# python manage.py makemigrations
# python manage.py migrate


# 5. 使用 Django 提供的 QuerySet API
# Django提供了丰富的API, 下面演示如何使用它。
# python manage.py shell
from people.models import Person
Person.objects.create(name="WeizhongTu", age=24)
Person.objects.get(name="WeizhongTu")
# 我们用了一个 .objects.get() 方法查询出来符合条件的对象，但是大家注意到了没有，查询结果中显示<Person: Person object>，
# 这里并没有显示出与WeizhongTu的相关信息，如果用户多了就无法知道查询出来的到底是谁，查询结果是否正确，
# 我们重新修改一下 people/models.py
# name 和 age 等字段中不能有 __（双下划线，因为在Django QuerySet API中有特殊含义（用于关系，包含，不区分大小写，以什么开头或结尾，日期的大于小于，正则等）
# 也不能有Python中的关键字，name 是合法的，student_name 也合法，但是student__name不合法，try, class, continue 也不合法，
# 因为它是Python的关键字( import keyword; print(keyword.kwlist) 可以打出所有的关键字)

# 新建一个对象的方法有以下几种：
Person.objects.create(name='ghou', age=23)
p = Person(name="WZ", age=23)
p.save()

p = Person(name="TWZ")
p.age = 23
p.save()
Person.objects.get_or_create(name="WZT", age=23)
# 这种方法是防止重复很好的方法，但是速度要相对慢些，返回一个元组，第一个为Person对象，第二个为True或False, 新建时返回的是True, 已经存在时返回False.

# 获取对象有以下方法：
Person.objects.all()
# Person.objects.all()[:10]    # 切片操作，获取10个人，不支持负索引，切片可以节约内存
Person.objects.get(name='WZT')

# get是用来获取一个对象的，如果需要获取满足条件的一些人，就要用到filter

Person.objects.filter(name="abc")               # 等于Person.objects.filter(name__exact="abc") 名称严格等于 "abc" 的人
Person.objects.filter(name__iexact="abc")       # 名称为 abc 但是不区分大小写，可以找到 ABC, Abc, aBC，这些都符合条件
Person.objects.filter(name__contains="abc")     # 名称中包含 "abc"的人
Person.objects.filter(name__icontains="abc")    # 名称中包含 "abc"，且abc不区分大小写
Person.objects.filter(name__regex="^abc")       # 正则表达式查询
Person.objects.filter(name__iregex="^abc")      # 正则表达式不区分大小写

# filter是找出满足条件的，当然也有排除符合某条件的
Person.objects.exclude(name__contains="WZ")     # 排除包含 WZ 的Person对象
Person.objects.filter(name__contains="abc").exclude(age=23)  # 找出名称含有abc, 但是排除年龄是23岁的