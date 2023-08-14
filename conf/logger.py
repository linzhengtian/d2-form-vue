# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      logger
   Description:
   Author:          LinZhengTian
   date：           2018/6/2
-------------------------------------------------
   Change Activity:
                    2018/6/2:
-------------------------------------------------
"""
import logging
from logging.config import fileConfig
from django.conf import settings
import os

logger_file = os.path.join(settings.BASE_DIR, 'conf', 'logger.conf')

fileConfig(logger_file)
user_logger = logging.getLogger('user')
configuration_logger = logging.getLogger('configuration')
