#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/12 10:19


# Django下models自定义Field的使用
# 一、自定义Field介绍
# 在上一个博客中简单罗列了一下Django下models常用的Field，但是有时候这些Field不能满足我们的存储数据的需求，
# 这个时候我们就可以使用自定义Field
# 二、自定义Field编写
# 具体思路是基于原有的Field，自定义Field首先去继承原有的Field，然后进行重写
# 需要重写明确以下几点：
# 第一、需要继承的models下的原有Field
# 第二、明确自己想要存储什么样的数据
# 第三、编写父类的__init__
# 第四、重写父类的to_python函数（将数据库内容转化为python对象）
# 第五、重写父类的get_prep_value函数（将python对象保存到数据库中，用于objects.create插入数据）
# 第六、重写父类的value_to_string函数（将python对象转为字符串，用于objects.get查询并输出数据）

from django.db import models

# 自定义Field
class MyField(models.TextField):

    # 自定义Field主体内容
    # 以存储列表数据为例
    def __init__(self, *args, **kwargs):
        super(MyField, self).__init__(*args, **kwargs)      # 调用父类初始化

    # 重写父类方法
    # 自定义Field001--将数据库内容转化为python对象
    def to_python(self, value):
        if not value:
            value = []
        if isinstance(value, list):
            return value
        return value

    # 自定义Field002--将python对象保存到数据库中, 用于objects.create插入数据
    def get_prep_value(self, value):
        if value is None:
            return value
        return str(value)                               # 强行转为字符串再写入数据库

    # 自定义Field003--python对象转为字符串，用于objects.get查询数据
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


# 三、创建自定义Field对应的数据库
# 针对上面的自定义Field，我们需要创建与之对应的数据库，并设置数据字段以及查询数据输出的格式
# 创建表来使用自定义字段类型

class Testmyfield(models.Model):

    myid = models.IntegerField()
    contents = MyField()
    # 设置返回数据库数据的格式
    def __str__(self):
        return '{},{}'.format(str(self.myid), str(self.contents))

# 四、自定义Field调试
# 在编写完毕自定义Field之后，我们需要进行调试，看是否能存储数据以及查询数据
# 1、调试存储数据
# 第一，在Terminal或者cmd中先进入到django项目目录当中
# 第二，输入python manage.py shell进入python的ide
# 第三，导入models下的自定义类数据库
# 第四、输入命令：自定义类数据库.objects.create(参数)
# from bbs.models import Testmyfield
Testmyfield.objects.create(myid=2,contents=['hello','hi','python'])
# 2、查询存储数据
# 第一，在Terminal或者cmd中先进入到django项目目录当中
# 第二，输入python manage.py shell进入python的ide
# 第三，导入models下的自定义类数据库
# 第四，输入命令：自定义类数据库.objects.get(查询条件)
# from bbs.models import Testmyfield
Testmyfield.objects.get(myid=2)