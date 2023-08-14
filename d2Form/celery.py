# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      celery
   Description:
   Author:          LinZhengTian
   date：           2018-07-16
-------------------------------------------------
   Change Activity:
                    2018-07-16:
-------------------------------------------------
"""
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'd2Form.settings')

app = Celery('d2Form')

app.conf.timezone = 'Asia/Shanghai'
app.conf.enable_utc = False

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')  # 4.0及以上版本

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()  # 4.0及以上版本
