from django.core.cache import cache
from django.conf import settings
from django_filters import CharFilter

from apps.vadmin.system.models import DictDetails


def get_dict_details_label_value(dict_type, reverse=True, value_type=str):
    """
    根据数据字典type标签，返回字典内容所有label、value键值对
    :param dict_type:
    :param reverse: True表示'dictValue'在前'dictLabel'在后，False反之
    :return: 形如[(1,XX),(2,XX)...]
    """
    dict_details_dic = cache.get('system_dict_details', {}) if getattr(settings, "REDIS_ENABLE", False) else {}
    if not dict_details_dic:
        obj = DictDetails.objects.filter(dict_data__dictType=dict_type).order_by('sort')
        return list(map(lambda x: (value_type(x[0]), x[1]), obj.values_list('dictValue', 'dictLabel'))) if reverse else list(map(lambda x: (value_type(x[0]), x[1]), obj.values_list('dictLabel', 'dictValue')))
    else:
        dicts = dict_details_dic.get(dict_type, [])
        if len(dicts) > 0:
            return list(map(lambda x: (value_type(x["dictValue"]), x["dictLabel"]) if reverse else (x["dictLabel"], value_type(x["dictValue"])), dicts))
    return []


class DictCharFilter(CharFilter):
    """
    多选筛选，例如：1,3输入与1,2,3,4字段值进行匹配，匹配结果为真
    """
    def __init__(self, *args, **kwargs):
        self.dict_type = kwargs.pop('dict_type', '')
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        # 存储格式形如X,X
        if not value:
            return qs
        if not isinstance(value, str):
            return qs
        value = value.replace('\\', "\\\\").replace('"', "\\\"")
        values = value.split(",")
        for v in values:
            qs &= qs.extra(where=['FIND_IN_SET("%s", %s)' % (v, self.field_name)])
        return qs.distinct() if self.distinct else qs
