# Generated by Django 2.2.28 on 2023-08-11 00:16

import apps.vadmin.op_drf.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jsonfield_backport.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('permission', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FormTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modifier', apps.vadmin.op_drf.fields.ModifierCharField(blank=True, help_text='该记录最后修改者', max_length=255, null=True, verbose_name='修改者')),
                ('update_datetime', apps.vadmin.op_drf.fields.UpdateDateTimeField(auto_now=True, help_text='修改时间', null=True, verbose_name='修改时间')),
                ('create_datetime', apps.vadmin.op_drf.fields.CreateDateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('scheme', django_jsonfield_backport.models.JSONField(verbose_name='模板内容')),
                ('version', models.CharField(blank=True, max_length=14, null=True, verbose_name='版本号')),
                ('source_form_id', models.IntegerField(verbose_name='关联表单')),
                ('creator', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '表单模板表',
                'verbose_name_plural': '表单模板表',
                'db_table': 'qform_form_template',
                'unique_together': {('source_form_id', 'version')},
            },
        ),
        migrations.CreateModel(
            name='FormInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modifier', apps.vadmin.op_drf.fields.ModifierCharField(blank=True, help_text='该记录最后修改者', max_length=255, null=True, verbose_name='修改者')),
                ('update_datetime', apps.vadmin.op_drf.fields.UpdateDateTimeField(auto_now=True, help_text='修改时间', null=True, verbose_name='修改时间')),
                ('create_datetime', apps.vadmin.op_drf.fields.CreateDateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='表单名称')),
                ('description', models.CharField(blank=True, max_length=8000, null=True, verbose_name='表单描述')),
                ('questionnaire_choice', models.CharField(choices=[('0', '否'), ('1', '是')], default='1', max_length=1, verbose_name='是否问卷模式')),
                ('publish_choice', models.CharField(choices=[('0', '未发布'), ('1', '已发布'), ('2', '已结束')], default='0', max_length=2, verbose_name='发布状态')),
                ('creator', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('form_info', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='qform.FormTemplate', verbose_name='关联表单')),
            ],
            options={
                'verbose_name': '表单信息表',
                'verbose_name_plural': '表单信息表',
                'db_table': 'qform_form_info',
            },
        ),
        migrations.CreateModel(
            name='FormData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modifier', apps.vadmin.op_drf.fields.ModifierCharField(blank=True, help_text='该记录最后修改者', max_length=255, null=True, verbose_name='修改者')),
                ('update_datetime', apps.vadmin.op_drf.fields.UpdateDateTimeField(auto_now=True, help_text='修改时间', null=True, verbose_name='修改时间')),
                ('create_datetime', apps.vadmin.op_drf.fields.CreateDateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('fill_data', django_jsonfield_backport.models.JSONField(verbose_name='提交内容')),
                ('creator', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('form_template', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='qform.FormTemplate', verbose_name='关联模板')),
            ],
            options={
                'verbose_name': '表单内容表',
                'verbose_name_plural': '表单内容表',
                'db_table': 'qform_form_data',
            },
        ),
        migrations.CreateModel(
            name='FormInfoUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_permission', models.CharField(choices=[('0', '否'), ('1', '是')], default='0', max_length=1, verbose_name='是否有新增权限')),
                ('modify_permission', models.CharField(choices=[('0', '否'), ('1', '是')], default='0', max_length=1, verbose_name='是否有修改权限')),
                ('delete_permission', models.CharField(choices=[('0', '否'), ('1', '是')], default='0', max_length=1, verbose_name='是否有删除权限')),
                ('form_info', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='qform.FormInfo', verbose_name='关联表单')),
                ('form_user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
            options={
                'verbose_name': '表单用户权限表',
                'verbose_name_plural': '表单用户权限表',
                'db_table': 'qform_form_info_user_permissions',
                'unique_together': {('form_user', 'form_info')},
            },
        ),
        migrations.CreateModel(
            name='FormInfoRolePermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_permission', models.CharField(choices=[('0', '否'), ('1', '是')], default='0', max_length=1, verbose_name='是否有新增权限')),
                ('modify_permission', models.CharField(choices=[('0', '否'), ('1', '是')], default='0', max_length=1, verbose_name='是否有修改权限')),
                ('delete_permission', models.CharField(choices=[('0', '否'), ('1', '是')], default='0', max_length=1, verbose_name='是否有删除权限')),
                ('form_info', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='qform.FormInfo', verbose_name='关联表单')),
                ('form_role', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='permission.Role', verbose_name='关联角色')),
            ],
            options={
                'verbose_name': '表单角色权限表',
                'verbose_name_plural': '表单角色权限表',
                'db_table': 'qform_form_info_role_permissions',
                'unique_together': {('form_role', 'form_info')},
            },
        ),
        migrations.CreateModel(
            name='FormInfoDesignPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_info', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='qform.FormInfo', verbose_name='关联表单')),
                ('form_user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
            options={
                'verbose_name': '表单用户权限表',
                'verbose_name_plural': '表单用户权限表',
                'db_table': 'qform_form_info_design_permissions',
                'unique_together': {('form_user', 'form_info')},
            },
        ),
    ]
