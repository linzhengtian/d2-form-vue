from django.core.cache import cache
from rest_framework import serializers

from django.conf import settings
from apps.vadmin.op_drf.serializers import CustomModelSerializer
from modules.case.models import *
from utils.drf.commons import MultipleChoiceCharField


class CaseRoleSerializer(CustomModelSerializer):
    """
    简单序列化器
    """

    class Meta:
        model = CaseRole
        fields = '__all__'


class CaseMainSerializer(CustomModelSerializer):
    """
    简单序列化器
    """
    role_name = serializers.CharField(source='case_role.role_name', default='', read_only=True)
    # multi_cities = MultipleChoiceCharField(choices=[]) # 返回列表

    class Meta:
        model = CaseMain
        fields = '__all__'
        attachment_fields = ["attachments"]


class ExportCaseMainSerializer(CustomModelSerializer):
    """
    导出时的序列化器
    """
    role_name = serializers.CharField(source='case_role.role_name', default='')

    class Meta:
        model = CaseMain
        fields = ('id', 'role_name', 'name', 'creator')


class CaseMainCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的序列化器
    """

    class Meta:
        model = CaseMain
        fields = '__all__'
        attachment_fields = ["attachments"]
