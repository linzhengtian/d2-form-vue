"""
-------------------------------------------------
   File Name：      tasks
   Description:
   Author:          LinZhengTian
   date：           2018-07-16
-------------------------------------------------
   Change Activity:
                    2018-07-16:
-------------------------------------------------
"""
from django.conf import settings
from utils.db.redis_ops import RedisOps
import time


# redis锁处理
def get_lock(unique_key="allocation"):
    redis_instance = RedisOps(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)
    counts = 60
    while counts and redis_instance.get(unique_key):
        time.sleep(1)
        counts -= 1
    return False if counts == 0 else True


def release_lock(unique_key="allocation"):
    redis_instance = RedisOps(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)
    if redis_instance.get(unique_key):
        redis_instance.delete(unique_key)


def set_lock(unique_key="allocation"):
    redis_instance = RedisOps(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)
    if not redis_instance.get(unique_key):
        redis_instance.set(unique_key, 1)
