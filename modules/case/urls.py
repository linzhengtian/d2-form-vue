from django.urls import re_path
from rest_framework.routers import DefaultRouter

from modules.case.views import CaseRoleModelViewSet, CaseMainModelViewSet

router = DefaultRouter()
router.register(r'caserole', CaseRoleModelViewSet)
router.register(r'casemain', CaseMainModelViewSet)


urlpatterns = [
    re_path('casemain/export/', CaseMainModelViewSet.as_view({'get': 'export'})),
]
urlpatterns += router.urls
