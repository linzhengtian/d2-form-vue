"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.conf.urls import url
from django.urls import re_path, include
from rest_framework.views import APIView
from utils.crypt_pwd import CryptPwd
from apps.vadmin.permission.views import GetUserProfileView, GetRouters
from apps.vadmin.utils.login import LoginView, LogoutView
from apps.vadmin.op_drf.response import SuccessResponse
from modules.urls import urlpatterns as modulesurl
from django.conf import settings


class CaptchaRefresh(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        new_key = CaptchaStore.pick()
        to_json_response = {
            "key": new_key,
            "image_url": captcha_image_url(new_key).replace("/api", "", 1) if settings.CAPTCHA_STATE else None
        }
        return SuccessResponse(to_json_response)


class PublicKeyRefresh(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        to_json_response = dict.fromkeys(["pid", "key"], "")
        if settings.CRYPT_CHECK:
            to_json_response = CryptPwd.gen_pri_pub_key_cache()
        return SuccessResponse(to_json_response)


urlpatterns = [
    re_path('api-token-auth/', LoginView.as_view(), name='api_token_auth'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^login/$', LoginView.as_view()),
    re_path(r'^logout/$', LogoutView.as_view()),
    re_path(r'^getInfo/$', GetUserProfileView.as_view()),
    re_path(r'^getRouters/$', GetRouters.as_view()),
    url(r"captcha/refresh/$", CaptchaRefresh.as_view(), name="captcha-refresh"),  # 刷新验证码
    url(r"public/refresh/$", PublicKeyRefresh.as_view(), name="public-refresh"),  # 刷新公钥
    re_path('captcha/', include('captcha.urls')),  # 图片验证码 路由
    re_path(r'^permission/', include('apps.vadmin.permission.urls')),
    re_path(r'^system/', include('apps.vadmin.system.urls')),
    re_path(r'^celery/', include('apps.vadmin.celery.urls')),
    re_path(r'^monitor/', include('apps.vadmin.monitor.urls')),
]

urlpatterns += modulesurl
