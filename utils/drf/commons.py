from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django.db.models.functions import Lower
from functools import reduce
import operator, six
from django.db import models
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
import six
from rest_framework import serializers as rfserializers
from rest_framework.response import Response
from collections import OrderedDict
from datetime import datetime
from rest_framework import status
from rest_framework.authentication import BaseAuthentication


class SearchFilterMixins(filters.SearchFilter):
    def custom_filter_queryset(self, request, queryset, view, **kwargs):
        # 扩展filter_queryset方法
        search_fields_ = getattr(view, 'search_fields', None)
        search_terms = self.get_search_terms(request)
        search_fields = []
        for search_field in search_fields_:
            if search_field in kwargs:
                search_fields.append(kwargs[search_field])
            else:
                search_fields.append(search_field)
        if not search_fields or not search_terms:
            return queryset
        orm_lookups = [
            self.construct_search(six.text_type(search_field))
            for search_field in search_fields
        ]
        conditions = []
        for search_term in search_terms:
            queries = [
                models.Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator.or_, queries))
        return queryset.filter(reduce(operator.or_, conditions)).distinct()


class OrderingFilterMixins(filters.OrderingFilter):
    def custom_filter_queryset(self, request, queryset, view, **kwargs):
        # 扩展filter_queryset方法
        ordering = self.get_ordering(request, queryset, view)
        if ordering is not None:
            for o in ordering:
                if o.startswith('-'):
                    n = o[1:]
                    if n in kwargs.keys():
                        n = n.replace(n, kwargs[n])
                    queryset = queryset.order_by(Lower(n)).reverse()
                else:
                    if o in kwargs.keys():
                        o = o.replace(o, kwargs[o])
                    queryset = queryset.order_by(Lower(o))
        return queryset


class d2FormPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('result', OrderedDict([
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('data', data),
                ('pageSize', self.page_size),
                ("pageNo", self.request.query_params.get(self.page_query_param, 1)),
                ("totalCount", self.page.paginator.count),
                ("totalPage", self.page.paginator.num_pages),
            ])),
            ('timestamp', int(datetime.timestamp(datetime.now())*1000)),
            ('status', status.HTTP_200_OK),
            ('message', ""),
        ]))


class ExamplePagination(d2FormPagination): #使用自定义pagination无法显示filters按钮
    page_size = 10
    page_size_query_param = 'pageSize'
    page_query_param = "pageNo"
    max_page_size = 100


class CommonPagination(PageNumberPagination):
    # 分页字段调整的公共模块
    page_size = 10
    page_size_query_param = 'pageSize'
    page_query_param = "pageNo"
    max_page_size = 100


class CommonFormViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    """
    不提供列表展示功能，只提供具体视图的增删改查功能
    """
    pass



class MultipleChoiceCharField(rfserializers.MultipleChoiceField):
    """
    生成string,string格式的多选输出
    """
    def to_internal_value(self, data):
        return (",".join(super().to_internal_value(data)))

    def to_representation(self, value):
        vs = value.split(",") if isinstance(value, str) else value
        return [
            self.choice_strings_to_values.get(six.text_type(item), item) for item in vs
        ]


def many_to_many_update(mo, data):
    # manytomany关联表单处理联动数据
    records = mo.all()
    data_dict = dict(map(lambda x:(x.id, x),data))
    try:
        count = len(records)
    except:
        count = 0
    if count > 0:
        for r in records:
            if r.id not in data_dict:
                mo.remove(r)
            else:
                del data_dict[r.id]
    for v in data_dict.values():
        mo.add(v)


class BaseNotAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 忽略登录校验
        return
