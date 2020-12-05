# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'apps'

    def ready(self):
        pass
