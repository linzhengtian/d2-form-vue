from django.urls import re_path, path
from rest_framework.routers import DefaultRouter

from modules.qform.views import *

router = DefaultRouter()
router.register(r'forminfo', FormInfoViewSet)
router.register(r'anonymousforminfo', AnonymousFormInfoViewSet)
router.register(r'forminfolist', FormInfoListViewSet)
router.register(r'formtemplate', FormTemplateViewSet)
router.register(r'formtemplateversion', FormTemplateVersionViewSet)
router.register(r'anonymousformtemplate', AnonymousFormTemplateViewSet)
router.register(r'anonymousformdata', AnonymousFormDataViewSet)
router.register(r'anonymoussavefile', AnonymousSaveFileViewSet)
router.register(r'formdata', FormDataViewSet)
router.register(r'forminforolepermissions', FormInfoRolePermissionsViewSet)
router.register(r'formrole', RoleModelViewSet)
router.register(r'forminfouserpermissions', FormInfoUserPermissionsViewSet)
router.register(r'forminfodesignpermissions', FormInfoDesignPermissionsViewSet)
router.register(r'formuser', UserModelViewSet)


urlpatterns = [
    path(r'formcopy/copy/', FormCopyViewSet.as_view({'post': 'copy'}), name='copy'),
    path(r'formdata/export/', FormDataViewSet.as_view({'get': 'export'}), name='formdata-export'),
]
urlpatterns += router.urls
