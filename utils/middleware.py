# -*- coding: utf-8 -*-
import json
import datetime
from django.conf import settings
from apps.vadmin.permission.models.users import UserProfile
from django.shortcuts import redirect
from utils.db.mongo_ops import MongoOps
from django.utils.deprecation import MiddlewareMixin

pass_paths = ['/login/', '/logout/']  # 指定哪些路径不保存所有用户列表的session
accept_keys = ['api', 'users']


class RecordMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super(RecordMiddleware, self).__init__(*args, **kwargs)
        self.body = None
        self.mongo = MongoOps(settings.MONGODB_HOST, settings.MONGODB_PORT, settings.RECORD_DB, settings.RECORD_COLL,
                              settings.MONGODB_USER, settings.MONGODB_PASS, settings.MONGODB_AUTHSOURCE)

    def process_request(self, request):
        if request.POST:
            self.body = {k: v[0] if len(v) == 1 else v for k, v in request.POST.lists()}
        else:
            self.body = getattr(request, '_body', request.body)

    def process_response(self, request, response):
        if request.method == 'GET' and request.path not in pass_paths and response.status_code == 200:
            user_infos = []
            users = UserProfile.objects.all()
            for user in users:
                user_info = {
                    'user_id': user.id,
                    'username': user.username,
                    'avatar': str(user.avatar),
                }
                user_infos.append(user_info)
            request.session['user_infos'] = user_infos

        # elif request.method != 'GET' and all([key not in request.path for key in pass_keys]):
        elif request.method != 'GET' and any([key == request.path.split('/')[1] for key in accept_keys]):
            if isinstance(self.body, dict):
                data = self.body
            elif isinstance(self.body, bytes) and len(self.body) != 0:
                data = json.loads(self.body.decode('utf-8'))
            else:
                data = None

            if 'api' in request.path:
                code = response.status_code
            elif '_container' in response.__dict__:
                try:
                    code = json.loads(response.__dict__.get('_container')[0].decode('utf-8')).get('code')
                except:
                    code = None
            else:
                code = None

            if data and 'action' in data and 'show' in data.get('action'):
                pass
            else:
                request_data = {'username': request.user.username, 'path': request.path, 'method': request.method,
                                'request_data': data, 'code': code,
                                'ip': request.META['REMOTE_ADDR'], 'datetime': datetime.datetime.now()}
                self.mongo.insert_one(request_data)
        return response
