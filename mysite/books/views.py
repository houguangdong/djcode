# -*- encoding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Book
# Create your views here.


# def search_form(request):
#     return render_to_response('book/search_form.html')


# def search1(request):
#     if 'q' in request.GET:
#         message = 'You searched for: %r' % request.GET['q']
#     else:
#         message = 'You submitted an empty form.'
#     return HttpResponse(message)


def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            books = Book.objects.filter(title__icontains=q)
            return render_to_response('book/search_results.html', {'books': books, 'query': q})
    return render_to_response('book/search_form.html', {'errors': errors})


# 第10章： 数据模型高级进阶
# 访问外键(Foreign Key)值
# 当你获取一个ForeignKey 字段时,你会得到相关的数据模型对象。 例如:
# python manager shell
# from mysite.books.models import Book
# b = Book.objects.get(id=50)
# b.publisher
# b.publisher.website
# 对于用`` ForeignKey`` 来定义的关系来说，在关系的另一端也能反向的追溯回来，只不过由于不对称性的关系而稍有不同。 通过一个`` publisher`` 对象，直接获取 books ，用 publisher.book_set.all() ，如下：
# p = Publisher.objects.get(name='Apress Publishing')
# p.book_set.all()
# 实际上，book_set 只是一个 QuerySet（参考第5章的介绍），所以它可以像QuerySet一样,能实现数据过滤和分切，例如：
# p = Publisher.objects.get(name='Apress Publishing')
# p.book_set.filter(name__icontains='django')
# 属性名称book_set是由模型名称的小写(如book)加_set组成的。

# 访问多对多值(Many-to-Many Values)
# 多对多和外键工作方式相同，只不过我们处理的是QuerySet而不是模型实例。 例如,这里是如何查看书籍的作者：
# b = Book.objects.get(id=50)
# b.authors.all()
# b.authors.filter(first_name='Adrian')
# b.authors.filter(first_name='Adam')
# 反向查询也可以。 要查看一个作者的所有书籍,使用author.book_set ,就如这样:
# a = Author.objects.get(first_name='Adrian', last_name='Holovaty')
# a.book_set.all()
# 这里,就像使用 ForeignKey字段一样，属性名book_set是在数据模型(model)名后追加_set。


# 更改数据库模式(Database Schema)
# 如果模型包含一个未曾在数据库里建立的字段，Django会报出错信息。 当你第一次用Django的数据库API请求表中不存在的字段时会导致错误（就是说，它会在运行时出错，而不是编译时）。
# Django不关心数据库表中是否存在未在模型中定义的列。
# Django不关心数据库中是否存在未被模型表示的表格。
# 改变模型的模式架构意味着需要按照顺序更改Python代码和数据库。

# 添加字段
# 首先，进入开发环境(也就是说，不是在发布环境里)：
# 在你的模型里添加字段。
# 运行 manage.py sqlall [yourapp] 来测试模型新的 CREATE TABLE 语句。 注意为新字段的列定义。
# 开启你的数据库的交互命令界面(比如, psql 或mysql , 或者可以使用 manage.py dbshell )。 执行 ALTER TABLE 语句来添加新列。
# 使用Python的manage.py shell，通过导入模型和选中表单(例如， MyModel.objects.all()[:5] )来验证新的字段是否被正确的添加 ,如果一切顺利,所有的语句都不会报错。

# BEGIN;
# --
# -- Add field num_pages to book
# --
# ALTER TABLE `books_book` ADD COLUMN `num_pages` integer NULL;
# ALTER TABLE `books_book` ALTER COLUMN `num_pages` DROP DEFAULT;
# --
# -- Alter field email on author
# --
# COMMIT;


# 添加 非NULL 字段
# 这里有个微妙之处值得一提。 在我们添加字段num_pages的时候，我们使用了 blank=True 和 null=True 选项。 这是因为在我们第一次创建它的时候，这个数据库字段会含有空值。
# 然而，想要添加不能含有空值的字段也是可以的。 要想实现这样的效果，你必须先创建 NULL 型的字段，然后将该字段的值填充为某个默认值，然后再将该字段改为 NOT NULL 型。 例如：
# BEGIN;
# ALTER TABLE books_book ADD COLUMN num_pages integer;
# UPDATE books_book SET num_pages=0;
# ALTER TABLE books_book ALTER COLUMN num_pages SET NOT NULL;
# COMMIT;
# 如果你这样做，记得你不要在模型中添加 blank=True 和 null=True 选项。
# 执行ALTER TABLE之后，我们要验证一下修改结果是否正确。启动python并执行下面的代码：
# from mysite.books.models import Book
# Book.objects.all()[:5]
# 如果没有异常发生，我们将切换到生产服务器，然后在生产环境的数据库中执行命令ALTER TABLE 然后我们更新生产环境中的模型，最后重启web服务器。

# 删除字段
# 从Model中删除一个字段要比添加容易得多。 删除字段，仅仅只要以下几个步骤：
# 删除字段，然后重新启动你的web服务器。
# 用以下命令从数据库中删除字段：
# ALTER TABLE books_book DROP COLUMN num_pages;
# 请保证操作的顺序正确。 如果你先从数据库中删除字段，Django将会立即抛出异常。

# 删除多对多关联字段
# 由于多对多关联字段不同于普通字段，所以删除操作是不同的。
# 从你的模型中删除ManyToManyField，然后重启web服务器。
# 用下面的命令从数据库删除关联表：
# DROP TABLE books_book_authors;
# 像上面一样，注意操作的顺序。

# 删除模型
# 删除整个模型要比删除一个字段容易。 删除一个模型只要以下几个步骤：
# 从文件中删除你想要删除的模型，然后重启web 服务器models.py
# 然后用以下命令从数据库中删除表：
# DROP TABLE books_book;
# 当你需要从数据库中删除任何有依赖的表时要注意（也就是任何与表books_book有外键的表 ）。
# 正如在前面部分，一定要按这样的顺序做。

# Managers
# 下面是你创建自定义manager的两个原因： 增加额外的manager方法，和/或修manager返回的初始QuerySet。
# 增加额外的Manager方法
# 增加额外的manager方法是为模块添加表级功能的首选办法。

# 修改初始Manager QuerySets
# 模型方法
# from django.contrib.localflavor.us.models import USStateField
# from django.db import models
#
# class Person(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     birth_date = models.DateField()
#     address = models.CharField(max_length=100)
#     city = models.CharField(max_length=50)
#     state = USStateField() # Yes, this is U.S.-centric...
#
#     def baby_boomer_status(self):
#         "Returns the person's baby-boomer status."
#         import datetime
#         if datetime.date(1945, 8, 1) <= self.birth_date <= datetime.date(1964, 12, 31):
#             return "Baby boomer"
#         if self.birth_date < datetime.date(1945, 8, 1):
#             return "Pre-boomer"
#         return "Post-boomer"
#
#     def is_midwestern(self):
#         "Returns True if this person is from the Midwest."
#         return self.state in ('IL', 'WI', 'MI', 'IN', 'OH', 'IA', 'MO')
#
#     def _get_full_name(self):
#         "Returns the person's full name."
#         return u'%s %s' % (self.first_name, self.last_name)
#     full_name = property(_get_full_name)
#
# p = Person.objects.get(first_name='Barack', last_name='Obama')
# p.birth_date
# p.baby_boomer_status()
# p.is_midwestern()
# p.full_name  # Note this isn't a method -- it's treated as an attribute


# 执行原始SQL查询
# from django.db import connection
# cursor = connection.cursor()
# cursor.execute("""
#    SELECT DISTINCT first_name
#    FROM people_person
#    WHERE last_name = %s""", ['Lennon'])
# row = cursor.fetchone()
# print row


# 不要把你的视图代码和django.db.connection语句混杂在一起，把它们放在自定义模型或者自定义manager方法中是个不错的主意。 比如，上面的例子可以被整合成一个自定义manager方法，就像这样：
# from django.db import connection, models
# class PersonManager(models.Manager):
#     def first_names(self, last_name):
#         cursor = connection.cursor()
#         cursor.execute("""
#             SELECT DISTINCT first_name
#             FROM people_person
#             WHERE last_name = %s""", [last_name])
#         return [row[0] for row in cursor.fetchone()]
#
# class Person(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     objects = PersonManager()
#
# # 然后这样使用:
# Person.objects.first_names('Lennon')