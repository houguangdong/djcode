#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/14 20:45

import weakref
from rklib.utils.djangoweb import get_response
from rklib.web.logic import RequestContext
from rklib.web.logic import ResponseContext


class DjangoRequestContext(RequestContext):

    def __init__(self, django_request):
        super(DjangoRequestContext, self).__init__()
        self._request = weakref.proxy(django_request)
        self._params = None
        self._cookies = None
        self._headers = None

    @property
    def params(self):
        if self._params is None:

            if self._request.method == 'GET':
                self._params = dict(self._request.GET.iteritems())

            if self._request.method == 'POST':
                self._params = dict(self._request.POST.iteritems())

        return self._params

    def get_parameter(self, name, default=None):
        return self.params.get(name, default)

    @property
    def cookies(self):
        if self._cookies is None:
            self._cookies = self._request.COOKIES

        return self._cookies

    def get_cookie(self, name, default=None):
        return self.cookies.get(name, default)

    @property
    def headers(self):
        if self._headers is None:
            self._headers = self._request.META

        return self._headers

    def get_header(self, name, default=None):
        return self.headers.get(name, default)

    @property
    def path(self):
        return self._request.path

    @property
    def query_string(self):
        return self.headers.get('QUERY_STRING')

    def get_host(self):
        return self._request.get_host()

    def get_http_method(self):
        return self._request.method

    @property
    def raw_request(self):
        return self._request


class DjangoResponseContext(ResponseContext):

    def __init__(self, django_response):
        super(DjangoResponseContext, self).__init__()
        if django_response is None:
            self._response = None
        else:
            self._response = weakref.proxy(django_response)

    @property
    def raw_response(self):
        return self._response

    def set_cookie(self, key, value, expires, domain=None, secure=None):
        '''
        :param key: cookie key
        :param value: cookie value
        :param expires: expiration (DatetimeDelta object)
        :param domain: domain setting
        :param secure: secure setting
        :return:
        '''
        return self._response.set_cookie(key, value, expires=expires, domain=domain, secure=secure)

    def reset_to(self, content="", mimetype=None, status=200, content_type=None):
        '''
        @parameters
            django style
        '''
        if content_type is not None:
            self._response = get_response(content, mimetype, status, content_type)
        else:
            self._response = get_response(content, mimetype, status)

        return self