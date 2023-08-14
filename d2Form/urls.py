"""d2Form URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from common import views
import xadmin
from django.contrib import admin
# from ninja import NinjaAPI
# from api.views import api_router
admin.autodiscover()
xadmin.autodiscover()
# from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v3',
        description="Test description",
        terms_of_service="https://fourier.com/",
        contact=openapi.Contact(email="d2formv2@qq.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# apiv2 = NinjaAPI()
# apiv2.add_router("api", api_router)

urlpatterns = [
    path(r'xadmin/', xadmin.site.urls),
    path(r'', views.dashboard),
    # path(r'v2/', apiv2.urls),
    re_path(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r'^api/admin/', include('apps.vadmin.urls')),
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^api/media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    ]

# 全局404页面配置
handler404='common.views.page_not_found'
# 全局500页面配置
handler500='common.views.page_error'
