"""
封装文件操作:
  ● 递归读取所有文件目录形成列表
  ● 递归删除空目录
  ● 批量删除文件
"""
import os
from apps.vadmin.system.models.save_file import SaveFile, SaveFileRelation
from ast import literal_eval
import logging
from modules.qform.models import FormData
from django.conf import settings


logger = logging.getLogger(__name__)

def get_all_files(targetDir):
    """
    递归读取所有文件目录形成列表
    :param targetDir:
    :return:
    """
    files = []
    listFiles = os.listdir(targetDir)
    for i in range(0, len(listFiles)):
        path = os.path.join(targetDir, listFiles[i])
        if os.path.isdir(path):
            files.extend(get_all_files(path))
        elif os.path.isfile(path):
            files.append(path)
    return files


def remove_empty_dir(path):
    """
    递归删除空目录
    :param path:
    :return:
    """
    for root, dirs, files in os.walk(path, topdown=False):
        if not files and not dirs:
            os.rmdir(root)


def delete_files(delete_list: list):
    """
    批量删除文件
    :param delete_list:
    :return:
    """
    for file_path in delete_list:
        try:
            os.remove(file_path)
        except(FileNotFoundError):
            pass


def get_relative_files(model_name, field_name, id):
    return ",".join(list(map(lambda x: str(x), SaveFileRelation.objects
                   .filter(model_name=model_name, field_name=field_name, relation_id=id)
                   .values_list('file_id', flat=True))))


def parse_file_ids(ids):
    # 防止注入
    if isinstance(ids, (str, int)):
        ids = "[{}]".format(ids)
        ids = literal_eval(ids)
    if not isinstance(ids, (list, tuple)):
        return []
    return ids


def create_relative_files(model_name, field_name, id, ids):
    # 防止注入
    ids = parse_file_ids(ids)
    try:
        for file_id in ids:
            SaveFileRelation.objects.create(**{
                "file_id": file_id,
                "model_name": model_name,
                "relation_id": id,
                "field_name": field_name,
            })
    except Exception as e:
        logger.error(e)
        return False
    return True


def update_relative_files(model_name, field_name, id, ids):
    ids = parse_file_ids(ids)
    try:
        relations = SaveFileRelation.objects.filter(model_name=model_name, relation_id=id, field_name=field_name)
        if len(ids) == 0:
            relations.delete()
        else:
            for relation in relations:
                file_id = relation.file_id
                if file_id in ids:
                    ids.remove(file_id)
                else:
                    SaveFile.objects.filter(id=file_id).delete()
                    relation.delete()
        for file_id in ids:
            SaveFileRelation.objects.create(**{
                "file_id": file_id,
                "model_name": model_name,
                "relation_id": id,
                "field_name": field_name,
            })
    except Exception as e:
        logger.error(e)
        return False
    return True


def delete_relative_files(model_name, field_name, id):
    try:
        relations = SaveFileRelation.objects.filter(model_name=model_name, field_name=field_name, relation_id=id)
        ids = relations.values_list("file_id", flat=True)
        SaveFile.objects.filter(id__in=ids).delete()
        relations.delete()
    except Exception as e:
        logger.error(e)
        return False
    return True


def get_qform_delete_files(model_name, field_name, id, ids):
    ids = parse_file_ids(ids)
    file_paths = []
    try:
        relations = SaveFileRelation.objects.filter(model_name=model_name, relation_id=id, field_name=field_name)
        form_datas = FormData.objects.filter(id=id).values_list("fill_data__" + field_name, flat=True)[0]
        attachments = dict(list(map(lambda x: (x["id"], x["file_url"]), form_datas))) if list(form_datas) else {}
        for relation in relations:
            file_id = relation.file_id
            if file_id not in ids:
                file_paths.append(os.path.join(settings.BASE_DIR, attachments[file_id].lstrip("/").lstrip("\\")))
    except Exception as e:
        logger.error(e)
        return []
    return file_paths
