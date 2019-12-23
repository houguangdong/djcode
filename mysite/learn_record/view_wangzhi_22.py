# -*- encoding: utf-8 -*-
# 在网页上做加减法
# 1. 采用 /add/?a=4&b=5 这样GET方法进行
# 自动生成目录大致如下（因不同的 Django 版本有一些差异，如果差异与这篇文章相关，我会主动提出来，没有说的，暂时可以忽略他们之间的差异，后面的教程也是这样做）：
# Django 1.7.x 及以下的同学可能看到的是这样的：
# url(r'^add/$', 'calc.views.add', name='add'),  # 注意修改了这一行
# Django 1.8.x及以上，Django 官方鼓励（或说要求）先引入，再使用。
# url(r'^add/$', calc_views.add, name='add'),  # 注意修改了这一行


# 2. 采用 /add/3/4/ 这样的网址的方式
# Django 1.7.x 及以下：
# url(r'^add/(\d+)/(\d+)/$', 'calc.views.add2', name='add2'),
# Django 1.8.x － Django 1.11.x：
# url(r'^add/(\d+)/(\d+)/$', calc_views.add2, name='add2'),
# 我们可以看到网址中多了 (\d+), 正则表达式中 \d 代表一个数字，+ 代表一个或多个前面的字符，写在一起 \d+ 就是一个或多个数字，用括号括起来的意思是保存为一个子组（更多知识请参见 Python 正则表达式），每一个子组将作为一个参数，被 views.py 中的对应视图函数接收。