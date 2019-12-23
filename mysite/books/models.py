# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# python manage.py makemigrations   # 生成建表sql
# python manage.py  migrate  数据库创建表

# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __unicode__(self):
        return self.name
    # Django让你可以指定模型的缺省排序方式：
    class Meta:
        ordering = ['name']


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(blank=True, verbose_name='e-mail')
    # 但这不适用于ManyToManyField和ForeignKey字段，因为它们第一个参数必须是模块类。
    # 那种情形，必须显式使用verbose_name这个参数名称。
    # email = models.EmailField(**'e-mail', **blank = True)
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)


class BookManager(models.Manager):
    def title_count(self, keyword):
        return self.filter(title__icontains=keyword).count()


class DahlBookManager(models.Manager):
    def get_query_set(self):
        return super(DahlBookManager, self).get_query_set().filter(author='Roald Dahl')


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField(blank=True, null=True)  # 如果 null=True, 表示数据库的该字段可以为空。，
                                                                # 如果 blank=True，表示你的表单填写该字段的时候可以不填
    # manage.py dbshell    ALTER TABLE books_book ALTER COLUMN publication_date DROP NOT NULL;
    num_pages = models.IntegerField(blank=True, null=True)
    objects1 = BookManager()
    objects = models.Manager()
    dahl_objects = DahlBookManager()
    # 注意我们明确地将objects设置成manager的实例，因为如果我们不这么做，那么唯一可用的manager就将是dah1_objects。
    def __unicode__(self):
        return self.title


class MaleManager(models.Manager):
    def get_query_set(self):
        return super(MaleManager, self).get_query_set().filter(sex='M')

class FemaleManager(models.Manager):
    def get_query_set(self):
        return super(FemaleManager, self).get_query_set().filter(sex='F')

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
    people = models.Manager()
    men = MaleManager()
    women = FemaleManager()

# python manage.py shell
# from books.models import Publisher
# p1 = Publisher(name='Apress', address='2855 Telegraph Avenue', city='Berkeley', state_province='CA', country='U.S.A.', website='http://www.apress.com/')
# p1.save()
# p2 = Publisher(name="O'Reilly", address='10 Fawcett St.', city='Cambridge', state_province='MA', country='U.S.A.', website='http://www.oreilly.com/')
# p2.save()
# publisher_list = Publisher.objects.all()
# publisher_list

# p1 = Publisher.objects.create(name='Apress', address='2855 Telegraph Avenue', city='Berkeley', state_province='CA', country='U.S.A.', website='http://www.apress.com/')
# p2 = Publisher.objects.create(name="O'Reilly", address='10 Fawcett St.', city='Cambridge', state_province='MA', country='U.S.A.', website='http://www.oreilly.com/')
# publisher_list = Publisher.objects.all()
# publisher_list

# 插入和更新数据
# p = Publisher(name='Apress', address='2855 Telegraph Ave.', city='Berkeley', state_province='CA', country='U.S.A.', website='http://www.apress.com/')
# p.name = 'Apress Publishing'
# p.save()

# 选择对象
# Publisher.objects.all()

# 数据过滤
# Publisher.objects.filter(name='Apress')
# Publisher.objects.filter(country="U.S.A.", state_province="CA")

# Publisher.objects.filter(name__contains="press")e
# SELECT id, name, address, city, state_province, country, website FROM books_publisher WHERE name LIKE '%press%';
# 其他的一些查找类型有：icontains(大小写无关的LIKE),startswith和endswith, 还有range(SQLBETWEEN查询）。

# 获取单个对象
# Publisher.objects.get(name="Apress")
# 多余一个 or 没有数据都抛异常
# Publisher.objects.get(country="U.S.A.")
# Publisher.objects.get(name="Penguin")

# 这个 DoesNotExist 异常 是 Publisher 这个 model 类的一个属性，即 Publisher.DoesNotExist。在你的应用中，你可以捕获并处理这个异常，像这样：
# try:
#     p = Publisher.objects.get(name='Apress')
# except Publisher.DoesNotExist:
#     print "Apress isn't in the database yet."
# else:
#     print "Apress is in the database."

# 数据排序
# 在你的 Django 应用中，你或许希望根据某字段的值对检索结果排序，比如说，按字母顺序。 那么，使用 order_by() 这个方法就可以搞定了。
# Publisher.objects.order_by("name")
# 跟以前的 all() 例子差不多，SQL语句里多了指定排序的部分：
# SELECT id, name, address, city, state_province, country, website FROM books_publisher ORDER BY name;
# Publisher.objects.order_by("address")
# Publisher.objects.order_by("state_province")
# Publisher.objects.order_by("state_province", "address")

# 我们还可以指定逆向排序，在前面加一个减号 - 前缀：
# Publisher.objects.order_by("-name")

# 连锁查询
# Publisher.objects.filter(country="U.S.A.").order_by("-name")
# SELECT id, name, address, city, state_province, country, website FROM books_publisher WHERE country = 'U.S.A' ORDER BY name DESC;

# 限制返回的数据
# Publisher.objects.order_by('name')[0]
# SELECT id, name, address, city, state_province, country, website FROM books_publisher ORDER BY name LIMIT 1;

# Publisher.objects.order_by('name')[0:2]
# SELECT id, name, address, city, state_province, country, website FROM books_publisher ORDER BY name OFFSET 0 LIMIT 2;

# 注意，不支持Python的负索引(negative slicing)：
# Publisher.objects.order_by('name')[-1]
# 虽然不支持负索引，但是我们可以使用其他的方法。 比如，稍微修改 order_by() 语句来实现：
# Publisher.objects.order_by('-name')[0]

# 更新多个对象
# p = Publisher.objects.get(name='Apress')
# p.name = 'Apress Publishing'
# p.save()

# SELECT id, name, address, city, state_province, country, website FROM books_publisher WHERE name = 'Apress';
# UPDATE books_publisher SET
#     name = 'Apress Publishing',
#     address = '2855 Telegraph Ave.',
#     city = 'Berkeley',
#     state_province = 'CA',
#     country = 'U.S.A.',
#     website = 'http://www.apress.com'
# WHERE id = 52;
# （注意在这里我们假设Apress的ID为52）

# Publisher.objects.filter(id=52).update(name='Apress Publishing')
# UPDATE books_publisher SET name = 'Apress Publishing' WHERE id = 52;

# Publisher.objects.all().update(country='USA')
# update()方法会返回一个整型数值，表示受影响的记录条数。 在上面的例子中，这个值是2。

# 删除对象
# 删除数据库中的对象只需调用该对象的delete()方法即可：
# p = Publisher.objects.get(name="O'Reilly")
# p.delete()
# Publisher.objects.all()

# 同样我们可以在结果集上调用delete()方法同时删除多条记录。这一点与我们上一小节提到的update()方法相似：
# Publisher.objects.filter(country='USA').delete()
# Publisher.objects.all().delete()
# Publisher.objects.all()

# 删除数据时要谨慎！ 为了预防误删除掉某一个表内的所有数据，Django要求在删除表内所有数据时显示使用all()。 比如，下面的操作将会出错：
# Publisher.objects.delete()  # 会报错，没有此方法
# 而一旦使用all()方法，所有数据将会被删除：
# Publisher.objects.all().delete()
# 如果只需要删除部分的数据，就不需要调用all()方法。再看一下之前的例子：
# Publisher.objects.filter(country='USA').delete()