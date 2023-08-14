import django_filters
from apps.vadmin.utils.dict_util import DictCharFilter
from modules.qform.models import *
from django.db.models import Q
import json
import re
from ast import literal_eval
from apps.vadmin.permission.models import Role, UserProfile


class FormTemplateFilter(django_filters.rest_framework.FilterSet):
    """
    过滤器
    """
    version = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = FormTemplate
        fields = ['id', 'version', "source_form_id"]


class FormDataFilter(django_filters.rest_framework.FilterSet):
    """
    过滤器
    """
    source_form_id = django_filters.CharFilter(label='source_form_id', method='filter_source_form_id')

    class Meta:
        model = FormData
        fields = ['id', 'form_template', "source_form_id"]

    def filter_source_form_id(self, queryset, name, value):
        return queryset.filter(form_template__source_form_id=value)

    @property
    def qs(self):
        scheme_types = {}

        def handle_special_types(scheme):
            if isinstance(scheme, list):
                for y in scheme:
                    if "tds" in y:
                        handle_special_types(y["tds"])
                    else:
                        handle_special_types(y)
            else:
                for x in scheme["list"]:
                    if x["type"] == "grid":
                        handle_special_types(x["columns"])
                    elif x["type"] == "table":
                        handle_special_types(x["trs"])
                    else:
                        if "model" in x:
                            scheme_types[x["model"]] = x

        parent = super().qs
        search_filter = self.request.query_params.get('searchFilter', None)
        source_form_id = self.request.query_params.get('source_form_id', None)
        scheme_types = {}
        if source_form_id:
            scheme = FormInfo.objects.filter(id=source_form_id).values_list("form_info__scheme", flat=True)[0]
            handle_special_types(scheme)
        filters = {}
        if search_filter:
            filters = json.loads(search_filter)
        conditions = {}
        extras = []
        for k, v in filters.items():
            if v:
                if isinstance(v, list):
                    if len(v) == 2 and scheme_types[k]["type"] in ['datePicker', 'date'] \
                            and re.compile('^[1-9]\d{3}-([1-9]|0[1-9]|1[0-2])-([1-9]|0[1-9]|[1-2][0-9]|3[0-1])$').match(v[0]) \
                            and re.compile('^[1-9]\d{3}-([1-9]|0[1-9]|1[0-2])-([1-9]|0[1-9]|[1-2][0-9]|3[0-1])$').match(v[1]):
                        # 兼容带时分秒查询条件
                        conditions["fill_data__" + k + "__gte"] = v[0]
                        conditions["fill_data__" + k + "__lte"] = v[1] + " 23:59:59"
                    elif (scheme_types[k]["type"] == "select" and scheme_types[k]["options"]["multiple"]) or \
                            scheme_types[k]["type"] == "checkbox" or scheme_types[k]["type"] == "cascader":
                        extras.append("json_contains(fill_data ->> '$."+k+"', json_array('"+"','".join(v)+"'))")
                    else:
                        conditions["fill_data__"+k+"__in"] = v
                else:
                    conditions["fill_data__"+k+"__icontains"] = v
        if conditions:
            parent = parent.filter(Q(**conditions))
        if extras:
            parent = parent.extra(where=extras)
        return parent


class FormInfoListFilter(django_filters.rest_framework.FilterSet):
    """
    过滤器
    """
    publish_choice = django_filters.CharFilter(label='publish_choice', method='filter_publish_choice')
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = FormInfo
        fields = ['name', 'questionnaire_choice', "publish_choice"]

    def filter_publish_choice(self, queryset, name, value):
        ids = literal_eval("[" + value + "]")
        return queryset.filter(publish_choice__in=ids)


class FormInfoRolePermissionsFilter(django_filters.rest_framework.FilterSet):
    """
    过滤器
    """

    class Meta:
        model = FormInfoRolePermissions
        fields = '__all__'


class RoleFilter(django_filters.rest_framework.FilterSet):
    """
    过滤器
    """

    class Meta:
        model = Role
        fields = ["id", "roleName"]


class UserFilter(django_filters.rest_framework.FilterSet):
    """
    过滤器
    """
    all_name = django_filters.CharFilter(label='all_name', method='filter_all_name')

    class Meta:
        model = UserProfile
        fields = ["id", "all_name"]

    def filter_all_name(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(username__icontains=value))


class FormInfoUserPermissionsFilter(django_filters.rest_framework.FilterSet):
    """
    过滤器
    """

    class Meta:
        model = FormInfoUserPermissions
        fields = '__all__'
