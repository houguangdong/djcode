#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/14 20:25
import time
import arrow
from django.utils.deprecation import MiddlewareMixin


class TimeviewMiddleware(MiddlewareMixin):

    def process_request(self, request):
        self.start_time = time.time()

    def process_response(self, request, response):
        end_time = time.time()
        path_name = request.path.strip('/').replace('/', '.')

        if not hasattr(self, 'start_time'):
            return response

        exec_time = (end_time - self.start_time) * 1000
        exec_time = "%.3f s" % (end_time - self.start_time) if exec_time >= 1000 else "%.3f ms" % exec_time
        if exec_time != 0:
            tmp = None

            if request.method == 'GET':
                tmp = dict(request.GET.iteritems())

            if request.method == 'POST':
                tmp = dict(request.POST.iteritems())

            if tmp is None:
                return response

            method = tmp.get('method')

            if method is None:
                print '%s timeit view: %s: %s' % \
                      (arrow.utcnow().format('YYYY-MM-DD HH:mm:ss'), path_name, exec_time)
            else:
                print '%s timeit view: %s.%s: %s' % \
                      (arrow.utcnow().format('YYYY-MM-DD HH:mm:ss'), path_name, method, exec_time)

        return response