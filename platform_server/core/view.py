# -*- coding:utf-8 -*-
import json

from django.http import QueryDict, HttpResponse
from rest_framework.request import Request
from rest_framework.views import APIView


class View(APIView):
    def __init__(self, **kwargs):
        super(View, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        """
        get 请求
        """
        return self.HttpResponse(503)

    def post(self, request, *args, **kwargs):
        """
        post 请求
        """
        return self.HttpResponse(503)

    def put(self, request, *args, **kwargs):
        """
        put 请求
        """
        return self.HttpResponse(503)

    def delete(self, request, *args, **kwargs):
        """
        delete 请求
        """
        return self.HttpResponse(503)

    @classmethod
    def json_loads(cls, data):
        """
        load 数据
        """
        return json.loads(data)

    @property
    def parameters(self):
        """
        获取请求中的参数
        """
        if not isinstance(self.request, Request):
            return {}

        query_params = self.request.query_params
        if isinstance(query_params, QueryDict):
            query_params = query_params.dict()
        result_data = self.request.data
        if isinstance(result_data, QueryDict):
            result_data = result_data.dict()

        if query_params != {}:
            return query_params
        return result_data

    @classmethod
    def HttpResponse(cls, data):
        """
        返回数据
        :param data: json 前的数据
        """
        if isinstance(data, int):
            return HttpResponse(status=data)
        if isinstance(data, str) or isinstance(data, unicode):
            return HttpResponse(data)
        return HttpResponse(json.dumps(data))