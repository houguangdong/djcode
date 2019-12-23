#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/11 01:21
from django.db.models import Aggregate, CharField


class GroupConcat(Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s%(ordering)s%(separator)s)'

    def __init__(self, expression, distinct=False, ordering=None, separator=',', **extra):
        super(GroupConcat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            ordering=' ORDER BY %s' % ordering if ordering is not None else '',
            separator=' SEPARATOR "%s"' % separator,
            output_field=CharField(),
            **extra)

# 代码来自：http://stackoverflow.com/a/40478702/2714931（我根据一个回复改写的增强版本）
# 使用时先引入 GroupConcat 这个类，比如聚合后的错误日志记录有这些字段 time, level, info
# 我们想把 level, info 一样的 聚到到一起，按时间和发生次数倒序排列，并含有每次日志发生的时间。
# ErrorLogModel.objects.values('level', 'info').annotate(
#     count=Count(1), time=GroupConcat('time', ordering='time DESC', separator=' | ')
# ).order_by('-time', '-count')

# 聚合相关：https://docs.djangoproject.com/en/2.2/topics/db/aggregation/