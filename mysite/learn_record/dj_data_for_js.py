#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/20 15:12

# Django传递数据给JS
# 有时候我们想把一个 list 或 dict等 JSON对象 传到网页的 javascript，用 JS 进行处理，比如用 js 将数据可视化显示到网页上。
# 请注意：如果不需要处理，直接显示到网页上，用Django模板就可以了，请看前面的教程。
# 这里讲述两种方法：
# 一，页面加载完成后，在页面上操作，在页面上通过 ajax 方法得到新的数据（再向服务器发送一次请求）并显示在网页上，这种情况适用于页面不刷新的情况下，动态加载一些内容。比如用户输入一个值或者点击某个地方，动态地把相应内容显示在网页上。
# 这种请问详见 Django Ajax 一节的内容。
# 二，直接在视图函数（views.py中的函数）中将 JSON对象 和网页其它内容一起传递到Django模板（一次性地渲染，还是同一次请求）。
# 请看下面的示例：
# views.py
#
# from __future__ import unicode_literals
# from django.shortcuts import render
#
#
# def home(request):
#     List = ['自强学堂', '渲染Json到模板']
#     return render(request, 'home.html', {'List': List})
#
# home.html 中的一部分
# <script type="text/javascript">
#     var List = {{ List }};
#     alert(List);
# </script>

# 需要注意的是，我们如果直接这么做，传递到 js 的时候，网页的内容会被转义，得到的格式会报错。
# 访问时会得到 Uncaught SyntaxError: Unexpected token ILLEGAL

# 需要注意两点：
# 1. 视图函数中的字典或列表要用 json.dumps()处理。
# 2. 在模板上要加 safe 过滤器。
# views.py
# -*- coding: utf-8 -*-

# from __future__ import unicode_literals
#
# import json
# from django.shortcuts import render
#
#
# def home(request):
#     List = ['自强学堂', '渲染Json到模板']
#     Dict = {'site': '自强学堂', 'author': '涂伟忠'}
#     return render(request, 'home.html', {
#         'List': json.dumps(List),
#         'Dict': json.dumps(Dict)
#     })

# home.html 只给出了 js 核心部分：
# //列表
# var List = {{ List|safe }};
# //字典
# var Dict = {{ Dict|safe }};
# 如果你对 js 比较熟悉，到此为止，后面的不用看了。
# 如果不太熟悉，可以参考下面的更详细的代码。
# html 完全代码及完整代码下载（最后面）：
# < !DOCTYPE
# html >
# < html >
# < head >
# < title > 欢迎光临
# 自强学堂！ < / title >
# < script
# src = "http://apps.bdimg.com/libs/jquery/1.10.2/jquery.min.js" > < / script >
# < / head >
# < body >
# < div
# id = "list" > 学习 < / div >
# < div
# id = 'dict' > < / div >
# < script
# type = "text/javascript" >
# // 列表
# var
# List = {{List | safe}};
#
# // 下面的代码把List的每一部分放到头部和尾部
# $('#list').prepend(List[0]);
# $('#list').append(List[1]);
#
# console.log('--- 遍历 List 方法 1 ---')
# for (i in List){
#     console.log(i); // i为索引
# }
#
# console.log('--- 遍历 List 方法 2 ---')
# for (var i = List.length - 1; i >= 0; i--) {
# // 鼠标右键，审核元素，选择 console 可以看到输入的值。
# console.log(List[i]);
# };
#
# console.log('--- 同时遍历索引和内容，使用 jQuery.each() 方法 ---')
# $.each(List, function(index, item)
# {
#     console.log(index);
# console.log(item);
# });
#
# // 字典
# var
# Dict = {{Dict | safe}};
# console.log("--- 两种字典的取值方式  ---")
# console.log(Dict['site']);
# console.log(Dict.author);
#
# console.log("---  遍历字典  ---");
# for (i in Dict) {
#     console.log(i + Dict[i]); // 注意，此处 i 为键值
# }
# < / script >
# < / body >
# < / html >