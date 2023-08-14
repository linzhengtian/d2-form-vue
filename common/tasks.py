# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      tasks
   Description:
   Author:          LinZheng
   date：           2018-07-16
-------------------------------------------------
   Change Activity:
                    2018-07-16:
-------------------------------------------------
"""
from d2Form.celery import app
import os, shutil
from django.conf import settings
from django.db import connection
from apps.vadmin.utils.file_util import get_all_files, delete_files
import datetime
from apps.vadmin.system.models import SaveFile


@app.task
def test():
    print("success")


def remove_temp(name):
    try:
        temp = os.path.join(settings.MEDIA_ROOT, name)
        if os.path.exists(temp):
            shutil.rmtree(temp)
        os.mkdir(temp, mode=0o777)
        return True
    except:
        return False


@app.task
def clean_temp():
    """
        clean tempfile periodly
    """
    return 'success' if remove_temp('tmp') else 'fail'


def clear_all_files(targetDir, n=0):
    """
    递归清理所有文件目录形成列表
    :param targetDir: 待清理路径
    :param n: 清理数量
    :return:
    """
    listFiles = os.listdir(targetDir)
    for i in range(0, len(listFiles)):
        path = os.path.join(targetDir, listFiles[i])
        if os.path.isdir(path):
            n = clear_all_files(path, n)
        elif os.path.isfile(path):
            if SaveFile.objects.filter(file=path.replace(settings.MEDIA_ROOT + os.sep, "", 1).replace(os.sep, "/")).count() == 0:
                os.remove(path)
                n += 1
    return n


@app.task
def clear_savefile():
    """
    清理废弃文件
    """
    # 清理无用关联文件标签
    with connection.cursor() as cur:
        cur.execute("""DELETE ss 
                        FROM
                            system_savefile ss
                            LEFT JOIN system_savefilerelation ssr ON ss.id = ssr.file_id 
                        WHERE
                            ssr.id IS NULL;""")
        cur.execute("""DELETE ssr 
                        FROM
                            system_savefilerelation ssr
                            LEFT JOIN system_savefile ss ON ssr.file_id = ss.id 
                        WHERE
                            ss.id IS NULL;""")
        cur.execute("commit;")
    # 获取废弃文件列表
    clear_all_files(os.path.join(settings.MEDIA_ROOT, 'system'))
    return 'success'
