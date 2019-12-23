#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/12 16:21
from django import forms


class AddForm(forms.Form):

    a = forms.IntegerField()
    b = forms.IntegerField()