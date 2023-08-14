from django.db import models
import datetime


is_deleted_choice_ = (
    ('0', '否'),
    ('1', '是'),
)


class BaseModel(models.Model):
    """
    基础model
    """
    creator = models.CharField(verbose_name='创建人', null=True, blank=True
                               , max_length=50)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    is_deleted = models.CharField(verbose_name='已删除', max_length=1, choices=is_deleted_choice_, default="0")

    def get_dict(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        dict_result = {}
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                dict_result[attr] = getattr(self, attr)
        return dict_result

    class Meta:
        abstract = True