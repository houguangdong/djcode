# -*- coding:utf-8 -*-


class BaseModel(object):
    def __init__(self):
        pass

    def load(self):
        print(self.__dict__)