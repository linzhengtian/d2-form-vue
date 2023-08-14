# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      asgi
   Description:
   Author:          LinZhengTian
   date：           2018/6/6
-------------------------------------------------
   Change Activity:
                    2018/6/6:
-------------------------------------------------
"""
import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d2Form.settings")
django.setup()
application = get_default_application()
