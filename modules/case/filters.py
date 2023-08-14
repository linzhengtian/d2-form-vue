import django_filters
from apps.vadmin.utils.dict_util import DictCharFilter
from modules.case.models import *


class CaseRoleFilter(django_filters.rest_framework.FilterSet):
    """
    过滤器
    """
    role_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CaseRole
        fields = ['id', 'role_name']


class CaseMainFilter(django_filters.rest_framework.FilterSet):
    """
    过滤器
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    role_name = django_filters.CharFilter(field_name='case_role__role_name', lookup_expr='icontains')
    multi_cities = DictCharFilter(dict_type='case_cities')

    class Meta:
        model = CaseMain
        fields = '__all__'
