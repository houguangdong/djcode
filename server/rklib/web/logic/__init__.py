#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/14 20:45
import sys

from rklib.utils.importlib import import_by_name
from rklib.core import app


class RequestContext(object):

    def __init__(self):
        self._data = {}
        self._result = {}

    @property
    def data(self):
        """用于存储handler链处理过程中的临时数据"""
        return self._data

    @property
    def result(self):
        """返回给web层的数据"""
        return self._result

    @property
    def params(self):
        raise NotImplementedError

    def get_parameter(self, name, default=None):
        raise NotImplementedError

    @property
    def cookies(self):
        raise NotImplementedError

    def get_cookie(self, name, default=None):
        raise NotImplementedError

    @property
    def headers(self):
        raise NotImplementedError

    def get_header(self, name, default=None):
        raise NotImplementedError

    @property
    def path(self):
        raise NotImplementedError

    @property
    def query_string(self):
        raise NotImplementedError

    def get_host(self):
        raise NotImplementedError

    def get_http_method(self):
        raise NotImplementedError

    @property
    def raw_request(self):
        raise NotImplementedError


class ResponseContext(object):

    def __init__(self):
        pass

    @property
    def raw_response(self):
        raise NotImplementedError

    def set_cookie(self, key, value, expires, **kwargs):
        '''设置Cookies'''
        raise NotImplementedError

    def reset_to(self, content="", **kwargs):
        '''重置Response内容'''
        raise NotImplementedError


class Gateway(object):

    def configure(self, cfg_value):
        self._cfg = cfg_value
        self._api_method_name = cfg_value.get("api_method_name", "method")
        self._logic_package = cfg_value.get("logic_package", "apps.logics")

        self._global_pre_handlers = []
        self._api_pre_handlers = {}
        self._handlers = {}
        self._api_post_handlers = {}
        self._global_post_handlers = []

        # import and cache handler function
        self._prepare_api_handlers()
        self._prepare_global_handlers()

    def process(self, request_ctx):
        api_method = request_ctx.get_parameter(self._api_method_name)
        func = self._get_handler(api_method)

        # global pre handlers
        if self._global_pre_handlers:
            for pre_func in self._global_pre_handlers:
                pre_func(request_ctx)

        # api special pre handlers
        pre_handlers = self._api_pre_handlers.get(api_method)
        if pre_handlers:
            for pre_func in pre_handlers:
                pre_func(request_ctx)

        # api handler
        func(request_ctx)

        # api special post handlers
        post_handlers = self._api_post_handlers.get(api_method)
        if post_handlers:
            for post_handler in post_handlers:
                post_handler(request_ctx)

        # global post handlers
        if self._global_post_handlers:
            for post_func in self._global_post_handlers:
                post_func(request_ctx)

        return request_ctx.result

    def _prepare_api_handlers(self):
        def _import_handlers(handlers, handlers_cfg):
            for method in handlers_cfg:
                method_cfg = handlers_cfg[method]
                funcs = []
                for func_name in method_cfg:
                    try:
                        func = import_by_name(func_name)
                        funcs.append(func)
                    except:
                        print >> sys.stderr, "Import failed! [%s][%s]" % (method, func_name)
                        raise
                handlers[method] = funcs

        _import_handlers(self._api_pre_handlers, self._cfg.get("api_pre_handlers"))
        _import_handlers(self._api_post_handlers, self._cfg.get("api_post_handlers"))

    def _prepare_global_handlers(self):
        def _import_handlers(handlers, handlers_cfg):
            for func_name in handlers_cfg:
                try:
                    func = import_by_name(func_name)
                    handlers.append(func)
                except:
                    print >> sys.stderr, "Import failed! [%s]" % func_name
                    raise

        _import_handlers(self._global_pre_handlers, self._cfg.get("global_pre_handlers"))
        _import_handlers(self._global_post_handlers, self._cfg.get("global_post_handlers"))

    def _get_handler(self, api_method):
        func = self._handlers.get(api_method)
        if func is not None:
            return func
        try:
            print self._logic_package + "." + api_method
            func = import_by_name(self._logic_package + "." + api_method)
            self._handlers[api_method] = func
        except ImportError:
            # print >> sys.stderr, "Import failed! [%s]" % (self._logic_package + "." + api_method)
            raise ApiMethodNotExists(self._logic_package, api_method)
        except AttributeError:
            raise ApiMethodNotExists(self._logic_package, api_method)

        return func


class ApiMethodNotExists(Exception):

    def __init__(self, package, method):
        self.package = package
        self.method = method

    def __str__(self):
        return 'The API method %s.%s does not exist.' % (self.package, self.method)


gateway = Gateway()
gateway.configure(app.logic_config.handlers)