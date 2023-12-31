from django.utils.functional import cached_property
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer
from rest_framework.utils.serializer_helpers import BindingDict

from apps.vadmin.utils.file_util import get_relative_files, create_relative_files, update_relative_files


class CustomModelSerializer(ModelSerializer):
    """
    增强DRF的ModelSerializer,可自动更新模型的审计字段记录
    (1)仅当op_drf.generics.GenericAPIView的子类里使用时有效
    (2)非op_drf.generics.GenericAPIView里使用时, 与ModelSerializer作用一样,没人任何增强
    (3)self.request能获取到rest_framework.request.Request对象
    """
    # 修改人的审计字段名称, 默认modifier, 继承使用时可自定义覆盖
    modifier_field_name = 'modifier'
    # 创建人的审计字段名称, 默认creator, 继承使用时可自定义覆盖
    creator_field_name = 'creator'
    # 数据所属部门字段
    dept_belong_id_field_name = 'dept_belong_id'
    # 添加默认时间返回格式
    create_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    creator_name = serializers.SlugRelatedField(slug_field="username", source="creator", read_only=True)

    def __init__(self, instance=None, data=empty, request=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.request: Request = request
        self.attachment_fields = self.find_attachment_fields()

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        if self.context.get('request'):
            self.request = self.context.get('request')
        if self.request:
            username = self.get_request_username()
            if self.modifier_field_name in self.fields.fields:
                validated_data[self.modifier_field_name] = username
            if self.creator_field_name in self.fields.fields:
                validated_data[self.creator_field_name] = self.request.user
            if self.dept_belong_id_field_name in self.fields.fields:
                validated_data[self.dept_belong_id_field_name] = getattr(self.request.user, 'dept_id', None)
        data = super().create(validated_data)
        # 字典处理
        for attachment in self.attachment_fields:
            create_relative_files(data._meta.model_name, attachment, data.id, self.initial_data.get(attachment, ""))
        return data

    def update(self, instance, validated_data):
        if self.request:
            if hasattr(self.instance, self.modifier_field_name):
                self.instance.modifier = self.get_request_username()
        data = super().update(instance, validated_data)
        # 字典处理
        for attachment in self.attachment_fields:
            update_relative_files(data._meta.model_name, attachment, data.id, self.initial_data.get(attachment, ""))
        return data

    def get_request_username(self):
        if getattr(self.request, 'user', None):
            return getattr(self.request.user, 'username', None)
        return None

    @cached_property
    def fields(self):
        fields = BindingDict(self)
        for key, value in self.get_fields().items():
            fields[key] = value

        if not hasattr(self, '_context'):
            return fields
        is_root = self.root == self
        parent_is_list_root = self.parent == self.root and getattr(self.parent, 'many', False)
        if not (is_root or parent_is_list_root):
            return fields

        try:
            request = self.request or self.context['request']
        except KeyError:
            return fields
        params = getattr(
            request, 'query_params', getattr(request, 'GET', None)
        )
        if params is None:
            pass
        try:
            filter_fields = params.get('_fields', None).split(',')
        except AttributeError:
            filter_fields = None

        try:
            omit_fields = params.get('_omit', None).split(',')
        except AttributeError:
            omit_fields = []

        existing = set(fields.keys())
        if filter_fields is None:
            allowed = existing
        else:
            allowed = set(filter(None, filter_fields))

        omitted = set(filter(None, omit_fields))
        for field in existing:
            if field not in allowed:
                fields.pop(field, None)
            if field in omitted:
                fields.pop(field, None)

        return fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 显示附件字段内容，格式为X,X,X
        for attachment in self.attachment_fields:
            # 默认取serializer定义字段
            data[attachment] = getattr(data, attachment, None) or get_relative_files(instance._meta.model_name, attachment, instance.id)
        return data

    @classmethod
    def find_attachment_fields(cls):
        """
        attachment_fields must be list or tuple.
        """
        # 自动处理附件字段，包括增删改查，需要serializer中定义attachment_fields
        attachment_fields = getattr(cls.Meta, "attachment_fields", [])
        assert isinstance(attachment_fields, (list, tuple)), (
            "attachment_fields must be list or tuple."
        )
        return attachment_fields
