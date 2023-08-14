from rest_framework import serializers
import datetime
from django.db.models import Q
import re
from modules.qform.models import *
from apps.vadmin.op_drf.serializers import CustomModelSerializer
from apps.vadmin.utils.dict_util import get_dict_details_label_value
from apps.vadmin.permission.models import Role, UserProfile


class FormInfoDesignPermissionsListSerializer(CustomModelSerializer):
    """
    简单序列化器
    """
    all_name = serializers.SerializerMethodField()

    class Meta:
        model = FormInfoDesignPermissions
        fields = ["form_user", "all_name"]

    def get_all_name(self, obj):
        user = obj.form_user
        name = user.name
        username = user.username
        dept_name = user.dept.deptName if user.dept else ""
        return "%s（%s）-%s" % (name, username, dept_name)

class FormInfoDesignPermissionsSerializer(CustomModelSerializer):
    """
    简单序列化器
    """
    designers = serializers.SerializerMethodField()
    ids = serializers.SerializerMethodField()

    class Meta:
        model = FormInfo
        fields = ["id", "designers", "ids"]

    def get_designers(self, obj):
        results = FormInfoDesignPermissionsListSerializer(instance=obj.forminfodesignpermissions_set.all(), many=True).data
        return results

    def get_ids(self, obj):
        # 用于更新FormInfoDesignPermissions
        return ""


class FormInfoUserPermissionsSerializer(CustomModelSerializer):
    """
    简单序列化器
    """
    name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    dept_name = serializers.SerializerMethodField()

    class Meta:
        model = FormInfoUserPermissions
        fields = '__all__'

    def get_name(self, obj):
        user = obj.form_user
        name = user.name
        username = user.username
        dept_name = user.dept.deptName if user.dept else ""
        return "%s（%s）-%s" % (name, username, dept_name)

    def get_username(self, obj):
        user = obj.form_user
        name = user.name
        username = user.username
        return "%s（%s）" % (name, username)

    def get_dept_name(self, obj):
        user = obj.form_user
        dept_name = user.dept.deptName if user.dept else ""
        return dept_name


class FormInfoRolePermissionsSerializer(CustomModelSerializer):
    """
    简单序列化器
    """
    role_name = serializers.CharField(source='form_role.roleName', default='', read_only=True)

    class Meta:
        model = FormInfoRolePermissions
        fields = '__all__'


class AnonymousFormInfoSerializer(CustomModelSerializer):
    """
    简单序列化器
    """

    class Meta:
        model = FormInfo
        fields = '__all__'


class FormInfoSerializer(CustomModelSerializer):
    """
    简单序列化器
    """

    class Meta:
        model = FormInfo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user = self.context["request"].user

    def to_representation(self, instance):
        '''
        全局自定义输出字段
        '''
        data = super().to_representation(instance)
        forminfouserpermissions = instance.forminfouserpermissions_set.filter(form_user=self.current_user).values("create_permission", "modify_permission", "delete_permission")
        forminfouserpermission = forminfouserpermissions[0] if len(forminfouserpermissions) != 0 else {}
        designpermission = "1" if len(instance.forminfodesignpermissions_set.filter(form_user=self.current_user)) != 0 \
                                  or self.current_user.username == "admin" else "0"
        design_users = instance.forminfodesignpermissions_set.all().values("form_user__name", "form_user__username")
        data.update(
            designpermission = designpermission,
            create_permission = forminfouserpermission.get("create_permission", "0") if designpermission == "0" else "1",
            modify_permission = forminfouserpermission.get("modify_permission", "0") if designpermission == "0" else "1",
            delete_permission = forminfouserpermission.get("delete_permission", "0") if designpermission == "0" else "1",
            design_users = "，".join(list(map(lambda x: "%s（%s）" % (x["form_user__name"], x["form_user__username"]), design_users)))
        )
        return data


class FormInfoListSerializer(CustomModelSerializer):
    """
    简单序列化器
    """
    design_permission = serializers.SerializerMethodField()

    class Meta:
        model = FormInfo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user = self.context["request"].user

    def get_design_permission(self, obj):
        return "1" if len(obj.forminfodesignpermissions_set.filter(form_user=self.current_user)) != 0 or self.current_user.username == "admin" else "0"


class FormTemplateSerializer(CustomModelSerializer):
    """
    简单序列化器
    """

    class Meta:
        model = FormTemplate
        fields = '__all__'


class FormTemplateVersionSerializer(CustomModelSerializer):
    """
    简单序列化器
    """

    class Meta:
        model = FormTemplate
        fields = ['id', 'version', "source_form_id"]


class FormDataSerializer(CustomModelSerializer):
    """
    简单序列化器
    """

    class Meta:
        model = FormData
        fields = '__all__'


class QRoleSerializer(CustomModelSerializer):
    """
    简单序列化器
    """

    class Meta:
        model = Role
        fields = ["id", "roleName"]


class UserSerializer(CustomModelSerializer):
    """
    简单序列化器
    """
    all_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ["id", "username", "name", "dept", "all_name"]

    def get_all_name(self, obj):
        name = obj.name
        username = obj.username
        dept_name = obj.dept.deptName if obj.dept else ""
        return "%s（%s）-%s" % (name, username, dept_name)


class FormCopySerializer(CustomModelSerializer):
    """
    简单序列化器
    """
    new_name = serializers.CharField(max_length=255)
    id = serializers.IntegerField()

    class Meta:
        model = FormInfo
        fields = ["id", "new_name"]
