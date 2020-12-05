#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mini_demo.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(cur_dir, ".."))

    # print 'path:', sys.path
    from rklib.core import app
    from django.conf import settings
    app.debug = settings.DEBUG
    app.init(storage_cfg_file=cur_dir+"/config/storage.conf", cache_cfg_file=cur_dir+"/config/cache.conf",
             model_cfg_file=cur_dir+"/config/model.conf", logic_cfg_file=cur_dir+"/config/logic.conf")

    execute_from_command_line(sys.argv)