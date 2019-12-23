#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/12 16:08

# Django 表单
# 有时候我们需要在前台用 get 或 post 方法提交一些数据，所以自己写一个网页，用到 html 表单的知识。
# 第一节：
# 比如写一个计算 a和 b 之和的简单应用，网页上这么写
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def add(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    return HttpResponse(str(a + b))


from django import forms


class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()


# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse

# 引入我们创建的表单类
from blog.forms import AddForm


def index1(request):
    if request.method == 'POST':  # 当提交表单时

        form = AddForm(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a) + int(b)))

    else:  # 当正常访问时
        form = AddForm()
    return render(request, 'index.html', {'form': form})


# 手可能觉得这样变得更麻烦了，有些情况是这样的，但是 Django 的 forms 提供了：
# 模板中表单的渲染
# 数据的验证工作，某一些输入不合法也不会丢失已经输入的数据。
# 还可以定制更复杂的验证工作，如果提供了10个输入框，必须必须要输入其中两个以上，在 forms.py 中都很容易实现
# 也有一些将 Django forms 渲染成 Bootstrap 的插件，也很好用，很方便。