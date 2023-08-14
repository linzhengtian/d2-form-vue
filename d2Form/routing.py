# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      routing
   Description:
   Author:          LinZhengTian
   date：           2018/6/6
-------------------------------------------------
   Change Activity:
                    2018/6/6:
-------------------------------------------------
"""
from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack


application = ProtocolTypeRouter({

    "websocket": AuthMiddlewareStack(
        URLRouter([
            # URLRouter just takes standard Django path() or url() entries.

        ]),
    ),
})
