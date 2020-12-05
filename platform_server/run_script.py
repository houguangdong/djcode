# -*- coding:utf-8 -*-
import os
import sys
import runpy
import django

print '--------------------------------------------------------------------------------'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "platform_server.settings")
django.setup()
script_path = sys.argv[1]
runpy.run_path(script_path, run_name="__main__")
print '--------------------------------------------------------------------------------'