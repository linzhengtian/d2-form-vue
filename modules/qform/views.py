from rest_framework.response import Response
from ast import literal_eval
from django.conf import settings
import os
import uuid
from utils.commons import download_response
from apps.vadmin.op_drf.response import SuccessResponse, ErrorResponse
from apps.vadmin.op_drf.viewsets import CustomModelViewSet, mixins, GenericViewSet, ReadOnlyModelViewSet
from apps.vadmin.permission.permissions import CommonPermission
import xlsxwriter
import logging
from apps.vadmin.system.models import SaveFile, SaveFileRelation
from modules.qform.serializers import *
from modules.qform.filter import *
from apps.vadmin.utils.file_util import create_relative_files, update_relative_files, delete_relative_files, get_qform_delete_files
import random
from apps.vadmin.utils.file_util import delete_files
from django.db.models import Q
from django.db import transaction
from apps.vadmin.permission.models import Role
from rest_framework import status
from django.forms.models import model_to_dict
from django.http import Http404
from apps.vadmin.system.serializers import SaveFileSerializer
from modules.qform.tasks import clean_qform
from apps.vadmin.utils.backends import SessionAuthentication as SessionAuthentication2  # 忽略csrf校验
from utils.drf.commons import BaseNotAuthentication  # 忽略登录校验

logger = logging.getLogger(__name__)


def get_ten_random_digits():
    return int('{:.9f}'.format(random.random())[2:])


'''
1、管理员用户有所有权限
2、负责人有设计和增删改查权限，有分配用户的权限
3、有权用户有对应权限的增删改权限
4、有权角色有对应权限的增删改权限
5、问卷模式、负责人、有权用户和有权权限可以查看表单和数据
6、问卷模式下所有人都可以新建，有权用户、有权角色、创建用户（处理人）可以修改和删除数据
7、问卷模式支持匿名用户新建
'''

class FormInfoDesignChangePermission(CommonPermission):
    def check_queryset(self, request, instance):
        return super().check_queryset(request, instance) \
            if len(instance.forminfodesignpermissions_set.filter(form_user=request.user.id)) != 0 or request.user.username == "admin" else False


class FormInfoDesignDeletePermission(CommonPermission):
    def check_queryset(self, request, instance):
        return super().check_queryset(request, instance) \
            if len(instance[0].forminfodesignpermissions_set.filter(form_user=request.user.id)) != 0 or request.user.username == "admin" else False


class FormTemplateDesignCreatePermission(CommonPermission):
    def has_permission(self, request, view):
        return True if len(FormInfoDesignPermissions.objects.filter(form_info=request.data["source_form_id"], form_user=request.user.id)) != 0 or request.user.username == "admin" else False


class FormTemplateDesignChangePermission(CommonPermission):
    def check_queryset(self, request, instance):
        return super().check_queryset(request, instance) \
            if len(FormInfoDesignPermissions.objects.filter(form_info__form_info=instance.id, form_user=request.user.id)) != 0 or request.user.username == "admin" else False


class FormTemplateDesignDeletePermission(CommonPermission):
    def check_queryset(self, request, instance):
        return super().check_queryset(request, instance) \
            if len(FormInfoDesignPermissions.objects.filter(form_info__form_info=instance[0].id, form_user=request.user.id)) != 0 or request.user.username == "admin" else False


class PermissionCreatePermission(CommonPermission):
    def has_permission(self, request, view):
        return True if len(FormInfoDesignPermissions.objects.filter(form_info=request.data["form_info"], form_user=request.user.id)) != 0 or request.user.username == "admin" else False


class PermissionChangePermission(CommonPermission):
    def check_queryset(self, request, instance):
        return super().check_queryset(request, instance) \
            if len(FormInfoDesignPermissions.objects.filter(form_info=instance.form_info, form_user=request.user.id)) != 0 or request.user.username == "admin" else False


class PermissionDeletePermission(CommonPermission):
    def check_queryset(self, request, instance):
        return super().check_queryset(request, instance) \
            if len(FormInfoDesignPermissions.objects.filter(form_info=instance[0].form_info, form_user=request.user.id)) != 0 or request.user.username == "admin" else False


class FormDataDesignCreatePermission(CommonPermission):
    def has_permission(self, request, view):
        user = request.user
        form_id = FormTemplate.objects.get(id=request.data["form_template"]).source_form_id
        design_permission = True if len(FormInfoDesignPermissions.objects.filter(form_info=form_id, form_user=user.id)) != 0 or user.username == "admin" else False
        if design_permission:
            return True
        questionnaire_choice_permission = FormInfo.objects.filter(id=form_id, questionnaire_choice="1").exists()
        if questionnaire_choice_permission:
            return True
        roles = user.role.filter(status='1').values_list("id", flat=True)
        role_create_permission = FormInfoRolePermissions.objects.filter(form_info=form_id, form_role__in=roles, create_permission="1").exists()
        if role_create_permission:
            return True
        user_create_permission = FormInfoUserPermissions.objects.filter(form_info=form_id, form_user=user.id, create_permission="1").exists()
        return design_permission or questionnaire_choice_permission or user_create_permission or role_create_permission


class FormDataDesignChangePermission(CommonPermission):
    def check_queryset(self, request, instance):
        user = request.user
        form_id = FormTemplate.objects.get(id=instance.form_template_id).source_form_id
        design_permission = True if len(FormInfoDesignPermissions.objects.filter(form_info=form_id, form_user=user.id)) != 0 or user.username == "admin" else False
        if design_permission:
            return True
        questionnaire_choice_permission = FormInfo.objects.filter(id=form_id, questionnaire_choice="1").exists()
        if questionnaire_choice_permission and instance.creator == user:
            return True
        roles = user.role.filter(status='1').values_list("id", flat=True)
        role_modify_permission = FormInfoRolePermissions.objects.filter(form_info=form_id, form_role__in=roles, modify_permission="1").exists()
        if role_modify_permission:
            return True
        user_modify_permission = FormInfoUserPermissions.objects.filter(form_info=form_id, form_user=user.id, modify_permission="1").exists()
        return user_modify_permission


class FormDataDesignDeletePermission(CommonPermission):
    def check_queryset(self, request, instance):
        user = request.user
        form_id = FormTemplate.objects.get(id=instance[0].form_template_id).source_form_id
        design_permission = True if len(FormInfoDesignPermissions.objects.filter(form_info=form_id,
                                                                                 form_user=user.id)) != 0 or user.username == "admin" else False
        if design_permission:
            return True
        questionnaire_choice_permission = FormInfo.objects.filter(id=form_id, questionnaire_choice="1").exists()
        if questionnaire_choice_permission:
            for e in instance:
                if e.creator != user:
                    break
            else:
                return True
        roles = user.role.filter(status='1').values_list("id", flat=True)
        role_delete_permission = FormInfoRolePermissions.objects.filter(form_info=form_id, form_role__in=roles,
                                                                        delete_permission="1").exists()
        if role_delete_permission:
            return True
        user_delete_permission = FormInfoUserPermissions.objects.filter(form_info=form_id, form_user=user.id,
                                                                        delete_permission="1").exists()
        return user_delete_permission


class FormInfoViewSet(CustomModelViewSet):
    queryset = FormInfo.objects.all()
    serializer_class = FormInfoSerializer
    # create_serializer_class = FormInfoCreateUpdateSerializer
    # update_serializer_class = FormInfoCreateUpdateSerializer
    # filter_class = FormInfoFilter
    update_extra_permission_classes = (FormInfoDesignChangePermission,)
    partial_update_extra_permission_classes = (FormInfoDesignChangePermission,)
    destroy_extra_permission_classes = (FormInfoDesignDeletePermission,)
    create_extra_permission_classes = (CommonPermission,)

    def perform_create(self, serializer):
        form_id = serializer.save()
        FormInfoDesignPermissions.objects.create(**{
            "form_info": form_id,
            "form_user": self.request.user,
        })

    def perform_destroy(self, instance):
        ids = list(instance.values_list('id', flat=True))
        instance.delete()
        clean_qform.delay(ids)


class AnonymousViewSet():
    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.format_kwarg = self.get_format_suffix(**kwargs)
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg
        self.check_throttles(request)


class AnonymousFormInfoViewSet(ReadOnlyModelViewSet, AnonymousViewSet):
    queryset = FormInfo.objects.filter(questionnaire_choice="1")  # 控制只有问卷模式可以正常访问
    serializer_class = AnonymousFormInfoSerializer
    permission_classes = []


class FormInfoListViewSet(CustomModelViewSet):
    queryset = FormInfo.objects.all()
    serializer_class = FormInfoListSerializer
    filter_class = FormInfoListFilter
    search_fields = ('name',)
    # ordering = 'id'  # 默认排序
    ordering_fields = ('id', 'name',)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        roles = user.role.filter(status='1').values_list("id", flat=True)
        if self.request.user.username != "admin":
            queryset = queryset.filter(Q(forminforolepermissions__form_role__in=roles) | Q(forminfouserpermissions__form_user=user) | Q(forminfodesignpermissions__form_user=user) | Q(questionnaire_choice="1")).distinct()
        return queryset


class FormTemplateViewSet(CustomModelViewSet):
    queryset = FormTemplate.objects.all()
    serializer_class = FormTemplateSerializer
    # create_serializer_class = FormTemplateCreateUpdateSerializer
    # update_serializer_class = FormTemplateCreateUpdateSerializer
    create_extra_permission_classes = (FormTemplateDesignCreatePermission,)
    partial_update_extra_permission_classes = (FormTemplateDesignChangePermission,)
    update_extra_permission_classes = (FormTemplateDesignChangePermission,)
    destroy_extra_permission_classes = (FormTemplateDesignDeletePermission,)

    @classmethod
    def get_ngimage_info(cls, scheme):
        ids = {}

        def get_ngimage(scheme):
            # 展示图片缓存图片关联关系
            if isinstance(scheme, list):
                for l in scheme:
                    get_ngimage(l)
                return
            if "list" not in scheme and "tds" in scheme:
                return get_ngimage(scheme["tds"])
            for l in scheme["list"]:
                if l["type"] == "NgImage":
                    ids[l["model"]] = []
                    for u in l["options"]["imageUrl"]:
                        ids[l["model"]].append(u["id"])
                elif l["type"] == "grid":
                    for col in l["columns"]:
                        get_ngimage(col)
                elif l["type"] == "table":
                    for tr in l["trs"]:
                        get_ngimage(tr)

        get_ngimage(scheme)
        return ids

    def perform_create(self, serializer):
        serializer.save()
        id = serializer.data["id"]
        ids = self.get_ngimage_info(serializer.data["scheme"])
        for k, vs in ids.items():
            for v in vs:
                SaveFileRelation.objects.create(**{
                    "file_id": v,
                    "model_name": "formtemplate",
                    "relation_id": id,
                    "field_name": k,
                })

    def perform_update(self, serializer):
        serializer.save()
        id = serializer.data["id"]
        ids = self.get_ngimage_info(serializer.data["scheme"])
        for k, vs in ids.items():
            old_ngimages = SaveFileRelation.objects.filter(
                model_name="formtemplate",
                relation_id=id,
                field_name=k
            )
            for v in vs:
                old_ngimages.exclude(file_id__in=vs).delete()
                if not old_ngimages.filter(file_id=v).exists():
                    SaveFileRelation.objects.create(**{
                        "file_id": v,
                        "model_name": "formtemplate",
                        "relation_id": id,
                        "field_name": k,
                    })

    def perform_destroy(self, instance):
        form_template = instance[0]
        form_id = form_template.source_form_id
        form_template_id = form_template.id
        form_info = FormInfo.objects.filter(id=form_id)[0]
        form_datas = FormData.objects.filter(form_template=form_template_id)
        for relation_id in form_datas.values_list('id', flat=True):
            SaveFileRelation.objects.filter(model_name="formdata", relation_id=relation_id).delete()
            SaveFileRelation.objects.filter(model_name="formtemplate", relation_id=relation_id).delete()
        form_datas.delete()
        instance.delete()
        if form_info.form_info_id == form_template_id:
            other_form_template = FormTemplate.objects.filter(source_form_id=form_id)
            if len(other_form_template) == 0:
                form_info.form_info = None
                form_info.publish_choice = "0"
            else:
                form_info.form_info = other_form_template.order_by('-update_datetime')[0]
            form_info.save()


class FormTemplateVersionViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = FormTemplate.objects.all()
    serializer_class = FormTemplateVersionSerializer
    permission_classes = (CommonPermission,)
    filter_class = FormTemplateFilter
    ordering = '-update_datetime'  # 默认排序


class AnonymousFormTemplateViewSet(ReadOnlyModelViewSet, AnonymousViewSet):
    queryset = FormTemplate.objects.all()
    serializer_class = FormTemplateSerializer
    permission_classes = []


def handle_special_types(scheme, ignore_control=False):
    # 递归解析表单结构
    scheme_types = {}

    def search_special_type(scheme):
        if isinstance(scheme, list):
            for y in scheme:
                if "tds" in y:
                    search_special_type(y["tds"])
                else:
                    search_special_type(y)
        else:
            for x in scheme["list"]:
                if x["type"] == "grid":
                    search_special_type(x["columns"])
                elif x["type"] == "table":
                    search_special_type(x["trs"])
                elif x["type"] == "control" and not ignore_control:
                    search_special_type(x)
                else:
                    if "model" in x:
                        scheme_types[x["model"]] = x

    search_special_type(scheme)
    return scheme_types


class AnonymousFormDataViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = FormData.objects.all()
    serializer_class = FormDataSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        # 控制问卷模式提交权限
        if FormInfo.objects.filter(form_info=request.data["form_template"], questionnaire_choice="1").count() == 0:
            raise Http404('forbidden')
        try:
            form_template = FormTemplate.objects.get(id=request.data["form_template"])
            upload_labels = list(map(lambda x: x["model"], filter(lambda x: x["type"] in ["uploadFile", "uploadImg"], handle_special_types(form_template.scheme).values())))
        except:
            upload_labels = []
        # 为附件设置唯一id
        for dk, dv in request.data["fill_data"].items():
            if dk in upload_labels:
                for uv in dv:
                    if "id" not in uv:
                        uv["id"] = get_ten_random_digits()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = FormData.objects.create(**serializer.validated_data)
        instance_dict = model_to_dict(instance)
        for k, v in instance_dict.get("fill_data", {}).items():
            if k in upload_labels:
                ids = []
                for ele in v:
                    ids.append(ele["id"])
                if len(ids):
                    create_relative_files("formdata", k, instance_dict.get("id"), ids)
        headers = self.get_success_headers(instance_dict)
        return SuccessResponse(instance_dict, status=status.HTTP_201_CREATED, headers=headers)


class AnonymousSaveFileViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = SaveFile.objects.all()
    serializer_class = SaveFileSerializer
    authentication_classes = [SessionAuthentication2, BaseNotAuthentication]
    permission_classes = []

    def create(self, request, *args, **kwargs):
        # 控制问卷模式提交权限
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        files = request.FILES.get('file')
        serializer.validated_data['name'] = files.name
        serializer.validated_data['size'] = files.size
        serializer.validated_data['type'] = files.content_type
        serializer.validated_data['address'] = '本地存储'
        serializer.validated_data['source'] = '用户上传'
        instance = SaveFile.objects.create(**serializer.validated_data)
        instance_dict = model_to_dict(instance)
        r = {}
        r["id"] = instance_dict["id"]
        r["name"] = instance_dict["name"]
        r["size"] = instance_dict["size"]
        r["file_url"] = r["file"] = instance_dict["file"].url
        headers = self.get_success_headers(instance)
        return SuccessResponse(r, status=status.HTTP_201_CREATED, headers=headers)


class FormDataViewSet(CustomModelViewSet):
    queryset = FormData.objects.all()
    serializer_class = FormDataSerializer
    filter_class = FormDataFilter
    create_extra_permission_classes = (FormDataDesignCreatePermission,)
    update_extra_permission_classes = (FormDataDesignChangePermission,)
    destroy_extra_permission_classes = (FormDataDesignDeletePermission,)
    ordering = '-update_datetime'  # 默认排序
    # ordering_fields = ('id', 'name',)

    def export(self, request):
        ids = request.query_params.get("ids", None)
        source_form_id = request.query_params.get("source_form_id", None)
        instance = self.filter_queryset(self.get_queryset())
        if ids:
            instance = instance.filter(id__in=ids.split(","))
        try:
            form_template_id = FormInfo.objects.get(id=source_form_id).form_info_id
            form_template = FormTemplate.objects.get(id=form_template_id)
            # 暂时忽略弹性容器
            export_labels = dict(map(lambda x: (x["model"], x), filter(lambda x: x["type"] not in ["uploadFile", "uploadImg", "control"], handle_special_types(form_template.scheme, True).values())))
        except:
            return ErrorResponse(msg="导出失败")
        datas = instance.values("id", "fill_data")
        tmp_dir = os.path.join(os.path.join(settings.BASE_DIR, 'media'), 'tmp')
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)
        filepath = os.path.join(tmp_dir, str(uuid.uuid1()).replace('-', '') + '.xlsx')
        workbook = xlsxwriter.Workbook(filepath)
        array_types = ["address", "checkbox", "select", "state", "cascader", "radio"]
        try:
            worksheet = workbook.add_worksheet(u'服务器资源清单')
            title = workbook.add_format(
                {'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#007ee5', 'border': 1, })
            content = workbook.add_format({'text_wrap': True, 'align': 'center', 'valign': 'vcenter', 'border': 1, })
            worksheet.set_column(0, 0, 8)
            worksheet.write(0, 0, 'ID', title)
            i = 1
            orders = []
            for k, v in export_labels.items():
                worksheet.set_column(i, i, 20)
                worksheet.write(0, i, v["label"], title)
                orders.append(v["model"])
                i += 1
            worksheet.freeze_panes(1, 0)
            worksheet.autofilter(0, 0, 0, i-1)
            j = 1
            for convert_data in datas:
                worksheet.set_row(j, 30)
                worksheet.write(j, 0, convert_data["id"], content)
                n = 1
                for o in orders:
                    if export_labels[o]["type"] in array_types:
                        worksheet.write_string(j, n, str(convert_data["fill_data"].get(o + "_label", "")), content)
                    else:
                        worksheet.write_string(j, n, str(convert_data["fill_data"].get(o, "")), content)
                    n += 1
                j += 1
        finally:
            workbook.close()
        response = download_response(filepath)
        return response

    def handle_request(self, request):
        # 获取附件列表
        try:
            form_template = FormTemplate.objects.get(id=request.data["form_template"])
            upload_labels = list(map(lambda x: x["model"], filter(lambda x: x["type"] in ["uploadFile", "uploadImg"], handle_special_types(form_template.scheme).values())))
        except:
            upload_labels = []
        # 为附件设置唯一id
        for dk, dv in request.data["fill_data"].items():
            if dk in upload_labels:
                for uv in dv:
                    if "id" not in uv:
                        uv["id"] = get_ten_random_digits()
        return upload_labels

    def create(self, request, *args, **kwargs):
        upload_labels = self.handle_request(request)
        resp = super().create(request, *args, **kwargs)
        # 附件存入关联表
        if resp.data.get("code", 0) == 200 and "data" in resp.data:
            for k, v in resp.data["data"].get("fill_data", {}).items():
                if k in upload_labels:
                    ids = []
                    for ele in v:
                        ids.append(ele["id"])
                    if len(ids):
                        create_relative_files("formdata", k, resp.data["data"]["id"], ids)
        return resp

    def update(self, request, *args, **kwargs):
        upload_labels = self.handle_request(request)
        file_paths = []
        for k, v in request.data.get("fill_data", {}).items():
            if k in upload_labels:
                ids = []
                for ele in v:
                    ids.append(ele["id"])
                file_paths += get_qform_delete_files("formdata", k, request.data["id"], ids)
        resp = super().update(request, *args, **kwargs)
        # 关联表更新附件
        if resp.data.get("code", 0) == 200 and "data" in resp.data:
            for k, v in resp.data["data"].get("fill_data", {}).items():
                if k in upload_labels:
                    ids = []
                    for ele in v:
                        ids.append(ele["id"])
                    if len(ids):
                        update_relative_files("formdata", k, resp.data["data"]["id"], ids)
                    else:
                        delete_relative_files("formdata", k, resp.data["data"]["id"])
        delete_files(file_paths)
        return resp

    def perform_destroy(self, instance):
        # 字典处理
        query = instance.values("id", "form_template", "fill_data")[0]
        try:
            form_template = FormTemplate.objects.get(id=query["form_template"])
            upload_labels = list(map(lambda x: x["model"], filter(lambda x: x["type"] in ["uploadFile", "uploadImg"], handle_special_types(form_template.scheme).values())))
        except:
            upload_labels = []
        file_paths = []
        for k, v in query.get("fill_data", {}).items():
            if k in upload_labels:
                for ele in v:
                    file_path = ele.get('file_url', "")
                    if file_path:
                        file_paths.append(os.path.join(settings.BASE_DIR, file_path.lstrip("/").lstrip("\\")))
            delete_relative_files("formdata", k, query["id"])
        delete_files(file_paths)
        instance.delete()


class FormInfoRolePermissionsViewSet(CustomModelViewSet):
    queryset = FormInfoRolePermissions.objects.all()
    serializer_class = FormInfoRolePermissionsSerializer
    filter_class = FormInfoRolePermissionsFilter
    ordering = '-id'  # 默认排序
    create_extra_permission_classes = (PermissionCreatePermission,)
    partial_update_extra_permission_classes = (PermissionChangePermission,)
    update_extra_permission_classes = (PermissionChangePermission,)
    destroy_extra_permission_classes = (PermissionDeletePermission,)

    def create(self, request, *args, **kwargs):
        '''
        用于前置数据校验和预处理
        '''
        if FormInfoRolePermissions.objects.filter(form_info=request.data["form_info"], form_role=request.data["form_role"]).exists():
            return ErrorResponse(msg="该角色已经存在")
        return super().create(request, *args, **kwargs)


class RoleModelViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    CRUD视图
    """
    queryset = Role.objects.filter(status="1")
    serializer_class = QRoleSerializer
    filter_class = RoleFilter
    ordering = '-id'  # 默认排序


class FormInfoUserPermissionsViewSet(CustomModelViewSet):
    queryset = FormInfoUserPermissions.objects.all()
    serializer_class = FormInfoUserPermissionsSerializer
    filter_class = FormInfoUserPermissionsFilter
    ordering = '-id'  # 默认排序
    create_extra_permission_classes = (PermissionCreatePermission,)
    partial_update_extra_permission_classes = (PermissionChangePermission,)
    update_extra_permission_classes = (PermissionChangePermission,)
    destroy_extra_permission_classes = (PermissionDeletePermission,)

    def create(self, request, *args, **kwargs):
        '''
        用于前置数据校验和预处理
        '''
        if FormInfoUserPermissions.objects.filter(form_info=request.data["form_info"], form_user=request.data["form_user"]).exists():
            return ErrorResponse(msg="该角色已经存在")
        return super().create(request, *args, **kwargs)


class UserModelViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    CRUD视图
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    ordering = '-id'  # 默认排序


class FormInfoDesignPermissionsViewSet(CustomModelViewSet):
    queryset = FormInfo.objects.all()
    serializer_class = FormInfoDesignPermissionsSerializer
    partial_update_extra_permission_classes = (FormInfoDesignChangePermission,)
    update_extra_permission_classes = (FormInfoDesignChangePermission,)
    destroy_extra_permission_classes = (FormInfoDesignDeletePermission,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        initial_data = serializer.initial_data
        ids = literal_eval("[%s]" % initial_data["ids"])
        forminfodesignpermissions = instance.forminfodesignpermissions_set.all()
        for permission in forminfodesignpermissions:
            if permission.form_user_id not in ids:
                permission.delete()
            else:
                ids.remove(permission.form_user_id)
        for id in ids:
            FormInfoDesignPermissions.objects.create(**{
                "form_info": instance,
                "form_user": UserProfile.objects.get(id=id)
            })
        return Response(serializer.data)


class FormCopyViewSet(GenericViewSet):
    serializer_class = FormCopySerializer
    permission_classes = (CommonPermission,)

    @transaction.atomic
    def copy(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        forminfo = FormInfo.objects.filter(id=request.data["id"])
        user = self.request.user
        roles = user.role.filter(status='1').values_list("id", flat=True)
        if self.request.user.username != "admin" and forminfo.filter(Q(forminforolepermissions__form_role__in=roles) | \
            Q(forminfouserpermissions__form_user=user) | Q(forminfodesignpermissions__form_user=user) | Q(questionnaire_choice="1")).count() == 0:
            return ErrorResponse(msg="当前用户没有权限复制该表单")
        if forminfo.count() == 0:
            return ErrorResponse(msg="表单不存在，请刷新页面")
        if FormInfo.objects.filter(name=request.data["new_name"]).count() > 0:
            return ErrorResponse(msg="表单名称已存在，请重新输入")
        forminfo_new = forminfo[0]
        forminfo_new.id = None
        forminfo_new.name = request.data["new_name"]
        forminfo_new.creator = request.user
        forminfo_new.publish_choice = "0"
        forminfo_new.save()
        FormInfoDesignPermissions.objects.create(**{
            "form_user": request.user,
            "form_info": forminfo_new
        })
        if forminfo_new.form_info:
            form_template_new = forminfo[0].form_info
            form_template_new.id = None
            form_template_new.source_form_id = forminfo_new.id
            forminfo_new.creator = request.user
            form_template_new.save()
            forminfo_new.forminfo = form_template_new
            forminfo_new.save()
            ids = FormTemplateViewSet.get_ngimage_info(form_template_new.scheme)
            for k, vs in ids.items():
                for v in vs:
                    SaveFileRelation.objects.create(**{
                        "file_id": v,
                        "model_name": "formtemplate",
                        "relation_id": form_template_new.id,
                        "field_name": k,
                    })
        instance_dict = model_to_dict(forminfo_new)
        return SuccessResponse(instance_dict, status=status.HTTP_201_CREATED)
