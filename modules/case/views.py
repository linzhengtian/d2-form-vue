import os
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.vadmin.op_drf.filters import DataLevelPermissionsFilter
from apps.vadmin.op_drf.response import SuccessResponse
from apps.vadmin.op_drf.viewsets import CustomModelViewSet, mixins, GenericViewSet
from apps.vadmin.permission.permissions import CommonPermission
from modules.case.filters import *
from modules.case.models import *
from modules.case.serializers import *
from apps.vadmin.utils.export_excel import export_excel_save_model


class CaseRoleModelViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    CRUD视图
    """
    queryset = CaseRole.objects.all()
    serializer_class = CaseRoleSerializer
    extra_filter_backends = [DataLevelPermissionsFilter]
    filter_class = CaseRoleFilter
    search_fields = ('role_name',)
    ordering = 'id'  # 默认排序


class CaseMainModelViewSet(CustomModelViewSet):
    """
    CRUD视图
    """
    queryset = CaseMain.objects.all()
    serializer_class = CaseMainSerializer
    create_serializer_class = CaseMainCreateUpdateSerializer
    update_serializer_class = CaseMainCreateUpdateSerializer
    extra_filter_backends = [DataLevelPermissionsFilter]
    filter_class = CaseMainFilter
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    search_fields = ('name',)
    # ordering = 'id'  # 默认排序
    ordering_fields = ('id', 'name',)
    export_field_data = ['主键', '关联角色', '名称', '创建者']
    export_serializer_class = ExportCaseMainSerializer
