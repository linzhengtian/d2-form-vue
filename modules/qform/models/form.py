from django.db import models
from django_jsonfield_backport.models import JSONField
from apps.vadmin.op_drf.models import MainModel, SET_NULL
from modules.qform.models import enums
from django.conf import settings
from apps.vadmin.permission.models import Role


publish_choice_ = enums.publish_choice_
questionnaire_choice_ = enums.questionnaire_choice_
permission_choice_ = enums.permission_choice_


class FormInfo(MainModel):
    # 如果由模板新建表单，则新增一个表单，模板标签为否
    name = models.CharField(max_length=255, verbose_name='表单名称', unique=True)
    description = models.CharField(max_length=8000, null=True, blank=True, verbose_name='表单描述')  # 限制2000个汉字
    questionnaire_choice = models.CharField(max_length=1, choices=questionnaire_choice_, verbose_name='是否问卷模式', default='1')
    publish_choice = models.CharField(max_length=2, choices=publish_choice_, verbose_name='发布状态', default='0')
    form_info = models.ForeignKey('FormTemplate', verbose_name='关联表单', null=True, blank=True, on_delete=SET_NULL,
                                  db_constraint=False)

    class Meta:
        db_table = 'qform_form_info'
        verbose_name = '表单信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id) + self.name


class FormInfoDesignPermissions(models.Model):
    form_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='关联用户', on_delete=models.CASCADE, db_constraint=False)
    form_info = models.ForeignKey('FormInfo', verbose_name='关联表单', on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = 'qform_form_info_design_permissions'
        verbose_name = '表单用户权限表'
        verbose_name_plural = verbose_name
        unique_together = (('form_user', 'form_info'),)

    def __str__(self):
        return str(self.form_user) + '-' + str(self.form_info)


class FormInfoUserPermissions(models.Model):
    form_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='关联用户', on_delete=models.CASCADE, db_constraint=False)
    form_info = models.ForeignKey('FormInfo', verbose_name='关联表单', on_delete=models.CASCADE, db_constraint=False)
    create_permission = models.CharField(max_length=1, choices=permission_choice_, verbose_name='是否有新增权限', default='0')
    modify_permission = models.CharField(max_length=1, choices=permission_choice_, verbose_name='是否有修改权限', default='0')
    delete_permission = models.CharField(max_length=1, choices=permission_choice_, verbose_name='是否有删除权限', default='0')

    class Meta:
        db_table = 'qform_form_info_user_permissions'
        verbose_name = '表单用户权限表'
        verbose_name_plural = verbose_name
        unique_together = (('form_user', 'form_info'),)

    def __str__(self):
        return str(self.form_user) + '-' + str(self.form_info)


class FormInfoRolePermissions(models.Model):
    form_role = models.ForeignKey(Role, verbose_name='关联角色', on_delete=models.CASCADE, db_constraint=False)
    form_info = models.ForeignKey('FormInfo', verbose_name='关联表单', on_delete=models.CASCADE, db_constraint=False)
    create_permission = models.CharField(max_length=1, choices=permission_choice_, verbose_name='是否有新增权限', default='0')
    modify_permission = models.CharField(max_length=1, choices=permission_choice_, verbose_name='是否有修改权限', default='0')
    delete_permission = models.CharField(max_length=1, choices=permission_choice_, verbose_name='是否有删除权限', default='0')

    class Meta:
        db_table = 'qform_form_info_role_permissions'
        verbose_name = '表单角色权限表'
        verbose_name_plural = verbose_name
        unique_together = (('form_role', 'form_info'),)

    def __str__(self):
        return str(self.form_role) + '-' + str(self.form_info)


class FormTemplate(MainModel):
    scheme = JSONField(verbose_name='模板内容')
    version = models.CharField(max_length=14, null=True, blank=True, verbose_name='版本号')
    source_form_id = models.IntegerField(verbose_name='关联表单')

    class Meta:
        db_table = 'qform_form_template'
        verbose_name = '表单模板表'
        verbose_name_plural = verbose_name
        unique_together = (('source_form_id', 'version'),)

    def __str__(self):
        return str(self.source_form_id) + "-" + self.version


class FormData(MainModel):
    form_template = models.ForeignKey('FormTemplate', verbose_name='关联模板', null=True, blank=True, on_delete=SET_NULL, db_constraint=False)
    fill_data = JSONField(verbose_name='提交内容')

    class Meta:
        db_table = 'qform_form_data'
        verbose_name = '表单内容表'
        verbose_name_plural = verbose_name
