#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/18 17:23

# Django 数据导入

# 从网上下载的一些数据，excel表格，xml文件，txt文件等有时候我们想把它导入数据库，应该如何操作呢？
# 以下操作符合 Django版本为 1.6 ，兼顾 Django 1.7, Django 1.8 版本，理论上Django 1.4, 1.5 也没有问题，没有提到的都是默认值
# 备注：你可能会问数据从哪儿来的，比如你用python从以前的blog上获取过来的，想导入现在的博客，或者别人整理好的数据，或者你自己整理的excel表，
# 一个个地在网站后台复制粘贴你觉得好么？这就是批量导入的必要性。
# 我们新建一个项目 mysite, 再新建一个 app，名称为blog
# django-admin.py startproject mysite
# cd mysite
# python manage.py startapp blog

# 一，同步数据库，创建相应的表
# python manage.py syncdb
# Django 创建了一些默认的表，注意后面那个红色标记的blog_blog是appname_classname的样式，这个表是我们自己写的Blog类创建的
# 二，输入 python manage.py shell
# 进入该项目的django环境的终端（windows如何进入对应目录？看 Django环境搭建 的 3.2 部分）
# 先说如何用命令新增一篇文章：
# python manage.py shell
# from blog.models import Blog
# Blog.objects.create(title="The first blog of my site",
#                         content="I am writing my blog on Terminal")
# 这样就新增了一篇博文，我们查看一下
# Blog.objects.all() # 获取所有blog
# 还有两种方法(这两种差不多)：
# blog2 = Blog()
# blog2.title = "title 2"
# blog2.content = "content 2"
# blog2.save()
# 或者
# blog2 = Blog(title="title 2",content="content 2")
# blog2.save()
# 后面两种方法也很重要，尤其是用在修改数据的时候，要记得最后要保存一下 blog.save(),第一种Blog.objects.create()是自动保存的。

# 三，批量导入
# 比如我们要导入一个文本，里面是标题和内容，中间用四个*隔开的，示例(oldblog.txt)：
# title 1****content 1
# title 2****content 2
# title 3****content 3
# title 4****content 4
# title 5****content 5
# title 6****content 6
# title 7****content 7
# title 8****content 8
# title 9****content 9
#
# 在终端导入有时候有些不方便，我们在 最外面那个 mysite目录下写一个脚本，叫 txt2db.py，把 oldblog.txt 也放在mysite下
# !/usr/bin/env python
# coding:utf-8
#
# import os
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
#
# '''
# Django 版本大于等于1.7的时候，需要加上下面两句
# import django
# django.setup()
# 否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
# '''
#
# import django
#
# if django.VERSION >= (1, 7):  # 自动判断版本
#     django.setup()
#
#
# def main():
#     from blog.models import Blog
#     f = open('oldblog.txt')
#     for line in f:
#         title, content = line.split('****')
#         Blog.objects.create(title=title, content=content)
#     f.close()
#
#
# if __name__ == "__main__":
#     main()
#     print('Done!')

# 好了，我们在终端运行它
# python txt2db.py
# 运行完后显示 一个 Done! 导入完成！
# 运行完毕后会打出一个 "Done!", 数据已经全部导入！

# 四，导入数据重复 解决办法
# 如果你导入数据过多，导入时出错了，或者你手动停止了，导入了一部分，还有一部分没有导入。或者你再次运行上面的命令，你会发现数据重复了，怎么办呢？
# django.db.models 中还有一个函数叫 get_or_create() 有就获取过来，没有就创建，用它可以避免重复，但是速度可以会慢些，因为要先尝试获取，看看有没有
# 只要把上面的
# Blog.objects.create(title=title,content=content)
# 换成下面的就不会重复导入数据了
# Blog.objects.get_or_create(title=title,content=content)
# 返回值是（BlogObject, True/False) 新建时返回 True, 已经存在时返回 False。
# 更多数据库API的知识请参见官网文档：QuerySet API

# 五, 用fixture导入
# 最常见的fixture文件就是用python manage.py dumpdata 导出的文件,示例如下:
# [
#   {
#     "model": "myapp.person",
#     "pk": 1,
#     "fields": {
#       "first_name": "John",
#       "last_name": "Lennon"
#     }
#   },
#   {
#     "model": "myapp.person",
#     "pk": 2,
#     "fields": {
#       "first_name": "Paul",
#       "last_name": "McCartney"
#     }
#   }
# ]
# 你也可以根据自己的models,创建这样的json文件,然后用 python manage.py loaddata fixture.json 导入
# 详见:https://docs.djangoproject.com/en/dev/howto/initial-data/
# 可以写一个脚本,把要导入的数据转化成 json 文件,这样导入也会更快些!

# 六，Model.objects.bulk_create() 更快更方便
# !/usr/bin/env python
# import os
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
#
#
# def main():
#     from blog.models import Blog
#     f = open('oldblog.txt')
#     BlogList = []
#     for line in f:
#         title, content = line.split('****')
#         blog = Blog(title=title, content=content)
#         BlogList.append(blog)
#     f.close()
#
#     Blog.objects.bulk_create(BlogList)
#
#
# if __name__ == "__main__":
#     main()
#     print('Done!')

# 由于Blog.objects.create()每保存一条就执行一次SQL，而bulk_create()是执行一条SQL存入多条数据，做会快很多！当然用列表解析代替 for 循环会更快！！
# !/usr/bin/env python
# import os
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
#
#
# def main():
#     from blog.models import Blog
#     f = open('oldblog.txt')
#
#     BlogList = []
#     for line in f:
#         parts = line.split('****')
#         BlogList.append(Blog(title=parts[0], content=parts[1]))
#
#     f.close()
#
#     # 以上四行 也可以用 列表解析 写成下面这样
#     # BlogList = [Blog(title=line.split('****')[0], content=line.split('****')[1]) for line in f]
#
#     Blog.objects.bulk_create(BlogList)
#
#
# if __name__ == "__main__":
#     main()
#     print('Done!')
# 当然也可以利用数据中的导出，再导入的方法，见下一节。