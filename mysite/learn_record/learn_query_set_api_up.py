#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/10 11:19

# 1. 查看 Django queryset 执行的 SQL
from mysite.wsgi import *
from blog.models import Author, Article, Tag
print(str(Author.objects.all().query))

print str(Author.objects.filter(name="WeizhongTu").query)
# 所以，当不知道Django做了什么时，你可以把执行的 SQL 打出来看看，
# 也可以借助 django-debug-toolbar 等工具在页面上看到访问当前页面执行了哪些SQL，耗时等。
# 还有一种办法就是修改一下 log 的设置，后面会讲到。

# 2. values_list 获取元组形式结果
# 2.1 比如我们要获取作者的 name 和 qq
authors = Author.objects.values_list('name', 'qq')
print(authors)
# 如果只需要 1 个字段，可以指定 flat=True
c = Author.objects.values_list('name', flat=True)
print(c)
print(list(Author.objects.values_list('name', flat=True)))
# 查询 twz915 这个人的文章标题
print(Article.objects.filter(author__name='twz915').values_list('title', flat=True))

# 3. values 获取字典形式的结果
# 3.1 比如我们要获取作者的 name 和 qq
print(Author.objects.values('name', 'qq'))
print(list(Author.objects.values('name', 'qq')))
# 3.2 查询 twz915 这个人的文章标题
print(Article.objects.filter(author__name='twz915').values('title'))
# 注意：
# 1. values_list 和 values 返回的并不是真正的 列表 或 字典，也是 queryset，他们也是 lazy evaluation 的（惰性评估，通俗地说，就是用的时候才真正的去数据库查）
# 2. 如果查询后没有使用，在数据库更新后再使用，你发现得到在是新内容！！！如果想要旧内容保持着，数据库更新后不要变，可以 list 一下
# 3. 如果只是遍历这些结果，没有必要 list 它们转成列表（浪费内存，数据量大的时候要更谨慎！！！）

# 4. extra 实现 别名，条件，排序等
# extra 中可实现别名，条件，排序等，后面两个用 filter, exclude 一般都能实现，排序用 order_by 也能实现。我们主要看一下别名这个
# 比如 Author 中有 name， Tag 中有 name 我们想执行
# 这样的语句，就可以用 select 来实现，如下：
tags = Tag.objects.all().extra(select={'tag_name': 'name'})
print(tags[0].name)
print(tags[0].tag_name)
# 我们发现 name 和 tag_name 都可以使用，确认一下执行的 SQL
print(Tag.objects.all().extra(select={'tag_name': 'name'}).query.__str__())
# 我们发现查询的时候弄了两次 (name) AS "tag_name" 和 "blog_tag"."name"
# 如果我们只想其中一个能用，可以用 defer 排除掉原来的 name （后面有讲）
print(Tag.objects.all().extra(select={'tag_name': 'name'}).defer('name').query.__str__())
# 也许你会说为什么要改个名称，最常见的需求就是数据转变成 list，然后可视化等，我们在下面一个里面讲。

# 5. annotate 聚合 计数，求和，平均数等
# 5.1 计数
# 我们来计算一下每个作者的文章数（我们每个作者都导入的Article的篇数一样，所以下面的每个都一样）
from django.db.models import Count
print(Article.objects.all().values('author_id').annotate(count=Count('author')).values('author_id', 'count'))
# 这是怎么工作的呢？
print(Article.objects.all().values('author_id').annotate(count=Count('author')).values('author_id', 'count').query.__str__())
# 简化一下SQL: SELECT author_id, COUNT(author_id) AS count FROM blog_article GROUP BY author_id
# 我们也可以获取作者的名称 及 作者的文章数
print(Article.objects.all().values('author__name').annotate(count=Count('author')).values('author__name', 'count'))
# 细心的同学会发现，这时候实际上查询两张表，因为作者名称(author__name)在 blog_author 这张表中，而上一个例子中的 author_id 是 blog_article 表本身就有的字段

# 5.2 求和 与 平均值
# 5.2.1 求一个作者的所有文章的得分(score)平均值
from django.db.models import Avg
print(Article.objects.values('author_id').annotate(avg_score=Avg('score')).values('author_id', 'avg_score'))
print(Article.objects.values('author_id').annotate(avg_score=Avg('score')).values('author_id', 'avg_score').query.__str__())

# 5.2.2 求一个作者所有文章的总分
from django.db.models import Sum
print(Article.objects.values('author__name').annotate(sum_score=Sum('score')).values('author__name', 'sum_score'))
print(Article.objects.values('author__name').annotate(sum_score=Sum('score')).values('author__name', 'sum_score').query.__str__())

# 6.  select_related 优化一对一，多对一查询
# 开始之前我们修改一个 settings.py 让Django打印出在数据库中执行的语句
# settings.py 尾部加上
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG' if DEBUG else 'INFO',
#         },
#     },
# }
# 这样当 DEBUG 为 True 的时候，我们可以看出 django 执行了什么 SQL 语句
# python manage.py shell
from blog.models import *
Author.objects.all()

# 假如，我们取出10篇Django相关的文章，并需要用到作者的姓名
articles = Article.objects.all()[:10]
a1 = articles[0]  # 取第一篇
print(a1.title)
print(a1.author_id)
print(a1.author.name)   # 再次查询了数据库，注意！！！
# 这样的话我们遍历查询结果的时候就会查询很多次数据库，能不能只查询一次，把作者的信息也查出来呢？
# 当然可以，这时就用到 select_related，我们的数据库设计的是一篇文章只能有一个作者，一个作者可以有多篇文章。
# 现在要查询文章的时候连同作者一起查询出来，“文章”和“作者”的关系就是多对一，换句说说，就是一篇文章只可能有一个作者。
articles = Article.objects.all().select_related('author')[:10]
a1 = articles[0]        # 取第一篇
print(a1.title)
print(a1.author.name)   # 嘻嘻，没有再次查询数据库！！

# 7. prefetch_related 优化一对多，多对多查询
# 和 select_related 功能类似，但是实现不同。
# select_related 是使用 SQL JOIN 一次性取出相关的内容。
# prefetch_related 用于 一对多，多对多 的情况，这时 select_related 用不了，因为当前一条有好几条与之相关的内容。
# prefetch_related是通过再执行一条额外的SQL语句，然后用 Python 把两次SQL查询的内容关联（joining)到一起
# 我们来看个例子，查询文章的同时，查询文章对应的标签。“文章”与“标签”是多对多的关系。
articles = Article.objects.all().prefetch_related('tags')[:10]
print(articles)
# 遍历查询的结果：
# 不用 prefetch_related 时
articles = Article.objects.all()[:3]
for a in articles:
    print a.title, a.tags.all()

# 用 prefetch_related 我们看一下是什么样子
articles = Article.objects.all().prefetch_related('tags')[:3]
for a in articles:
    print a.title, a.tags.all()
# 我们可以看到第二条 SQL 语句，一次性查出了所有相关的内容。
# 8. defer 排除不需要的字段
# 在复杂的情况下，表中可能有些字段内容非常多，取出来转化成 Python 对象会占用大量的资源。
# 这时候可以用 defer 来排除这些字段，比如我们在文章列表页，只需要文章的标题和作者，没有必要把文章的内容也获取出来（因为会转换成python对象，浪费内存）
print(Article.objects.all())
print(Article.objects.all().defer('content'))

# 9. only 仅选择需要的字段
# 和 defer 相反，only 用于取出需要的字段，假如我们只需要查出 作者的名称
print(Author.objects.all().only('name'))
# 细心的同学会发现，我们让查 name ， id 也查了，这个 id 是 主键，能不能没有这个 id 呢？
# 试一下原生的 SQL 查询
# authors = Author.objects.raw('select name from blog_author limit 1')
# author = authors[0]
# 报错信息说 非法查询，原生SQL查询必须包含 主键！

# 再试试直接执行 SQL
# python manage.py dbshell
# select name from blog_author limit 1;
# 虽然直接执行SQL语句可以这样，但是 django queryset 不允许这样做，一般也不需要关心，反正 only 一定会取出你指定了的字段。

# 10. 自定义聚合功能
# 我们前面看到了 django.db.models 中有 Count, Avg, Sum 等，但是有一些没有的，比如 GROUP_CONCAT，它用来聚合时将符合某分组条件(group by)的不同的值，连到一起，作为整体返回。
# 我们来演示一下，如果实现 GROUP_CONCAT 功能。
# 新建一个文件 比如 my_aggregate.py