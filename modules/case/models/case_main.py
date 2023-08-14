from django.db import models
from apps.vadmin.op_drf.models import CoreModel, BaseModel


employee_choice_ = (
    ('f', '正式'),
    ('u', '非正式'),
)


class CaseMain(CoreModel):
    case_role = models.ForeignKey('CaseRole', verbose_name='关联角色', on_delete=models.CASCADE)
    name = models.CharField(max_length=256, verbose_name='任务名称', help_text='填写任务名称')
    plan = models.TextField(max_length=1024, null=True, blank=True, verbose_name='执行计划', help_text='填写执行计划')
    employee_choice = models.CharField(max_length=1, choices=employee_choice_, verbose_name='员工类型', default='f')
    multi_cities = models.CharField(max_length=12, null=True, blank=True, verbose_name='城市')
    status = models.BooleanField(default=False, verbose_name='运行状态')

    class Meta:
        db_table = 'case_case_main'
        verbose_name = '示例主体表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id) + self.name


class CaseRole(BaseModel):
    role_name = models.CharField(max_length=16, verbose_name='角色名字')

    class Meta:
        db_table = 'case_case_role'
        verbose_name = '示例角色表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id) + self.role_name
