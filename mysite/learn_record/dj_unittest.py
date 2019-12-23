#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/20 23:01

# Django 单元测试
# 自强学堂Django一系列教程，前面的例子都是我们写好代码后，运行开发服务器，在浏览器上自己点击测试，看写的代码是否正常，但是这样做很麻烦，
# 因为以后如果有改动，可能会影响以前本来正常的功能，这样以前的功能又得测试一遍，非常不方便，Django中有完善的单元测试，
# 我们可以对开发的每一个功能进行单元测试，这样只要运行一个命令 python manage.py test，就可以测试功能是否正常。
# 一言以蔽之，测试就是检查代码是否按照自己的预期那样运行。
# 测试驱动开发: 有时候，我们知道自己需要的功能（结果），并不知道代码如何书写，这时候就可以利用测试驱动开发（Test Driven Development)，
# 先写出我们期待得到的结果（把测试代码先写出来），再去完善代码，直到不报错，我们就完成了。
# 《改善Python的91个建议》一书中说：单元测试绝不是浪费时间的无用功，它是高质量代码的保障之一，在软件开发的一节中值得投入精力和时间去把好这一关。
# 1. Python 中 单元测试简介：
# 下面是一个 Python的单元测试简单的例子：
# 假如我们开发一个除法的功能，有的同学可能觉得很简单，代码是这样的：
def division_funtion(x, y):
    return x / y

# 但是这样写究竟对还是不对呢，有些同学可以在代码下面这样测试：
# def division_funtion(x, y):
#     return x / y
#
#
# if __name__ == '__main__':
#     print division_funtion(2, 1)
#     print division_funtion(2, 4)
#     print division_funtion(8, 3)
#
# 但是这样运行后得到的结果，自己每次都得算一下去核对一遍，很不方便，Python中有 unittest 模块，可以很方便地进行测试，详情可以文章最后的链接，看官网文档的详细介绍。
# 下面是一个简单的示例：
# import unittest
#
#
# def division_funtion(x, y):
#     return x / y
#
#
# class TestDivision(unittest.TestCase):
#     def test_int(self):
#         self.assertEqual(division_funtion(9, 3), 3)
#
#     def test_int2(self):
#         self.assertEqual(division_funtion(9, 4), 2.25)
#
#     def test_float(self):
#         self.assertEqual(division_funtion(4.2, 3), 1.4)
#
#
# if __name__ == '__main__':
#     unittest.main()
# 我简单地写了三个测试示例（不一定全面，只是示范，比如没有考虑除数是0的情况），运行后发现：
# 汗！发现了没，竟然两个都失败了，测试发现：
# 4.2除以3 等于 1.4000000000000001 不等于期望值 1.4
# 9除以4等于2，不等于期望的 2.25
# 下面我们就是要修复这些问题，再次运行测试，直到运行不报错为止。
# 譬如根据实际情况，假设我们只需要保留到小数点后6位，可以这样改：
# def division_funtion(x, y):
#     return round(float(x) / y, 6)
# 再次运行就不报错了:
# Python 单元测试 官方文档：
# Python 2 (https://docs.python.org/2/library/unittest.html)
# Python 3 (https://docs.python.org/3/library/unittest.html)

# 2. Django 中 单元测试：(不断完善中，后期会增加对前面讲解的内容的测试）
# 2.1 简单测试例子：
from django.test import TestCase
from myapp.models import Animal


class AnimalTestCase(TestCase):
    def setUp(self):
        Animal.objects.create(name="lion", sound="roar")
        Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')

# 这个例子是测试myapp.models 中的 Animal 类相关的方法功能。
# 2.2 用代码访问网址的方法：
from django.test import Client
c = Client()
response = c.post('/login/', {'username': 'john', 'password': 'smith'})
print response.status_code

response = c.get('/customer/details/')
print response.content

# 我们可以用 django.test.Client 的实例来实现 get 或 post 内容，检查一个网址返回的网页源代码。
# 默认情况下CSRF检查是被禁用的，如果测试需要，可以用下面的方法：
# from django.test import Client
# csrf_client = Client(enforce_csrf_checks=True)
# 使用 csrf_client 这个实例进行请求即可。
# 指定浏览USER-AGENT:
# c = Client(HTTP_USER_AGENT='Mozilla/5.0')
# 模拟post上传附件：
from django.test import Client

c = Client()

with open('wishlist.doc') as fp:
    c.post('/customers/wishes/', {'name': 'fred', 'attachment': fp})

# 测试网页返回状态：
from django.test import TestCase


class SimpleTest(TestCase):
    def test_details(self):
        response = self.client.get('/customer/details/')
        self.assertEqual(response.status_code, 200)

    def test_index(self):
        response = self.client.get('/customer/index/')
        self.assertEqual(response.status_code, 200)

# 我们用 self.client 即可，不用 client = Client() 这样实例化，更方便，我们还可以继承 Client，添加一些其它方法:
from django.test import TestCase, Client


class MyTestClient(Client):
    # Specialized methods for your environment
    # ...
    pass


class MyTest(TestCase):
    client_class = MyTestClient

    def test_my_stuff(self):
        # Here self.client is an instance of MyTestClient...
        # call_some_test_code()
        pass

# 定制 self.client 的方法：
from django.test import Client, TestCase


class MyAppTests(TestCase):
    def setUp(self):
        super(MyAppTests, self).setUp()
        self.client = Client(enforce_csrf_checks=True)

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)