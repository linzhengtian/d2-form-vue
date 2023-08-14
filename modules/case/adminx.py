import xadmin
from modules.case.models import *


class CaseMainAdmin(object):
    list_display = ('id', 'name', 'plan')
    list_display_links = ['name']
    search_fields = ['name']

xadmin.site.register(CaseMain, CaseMainAdmin)


class CaseRoleAdmin(object):
    list_display = ('id', 'role_name', 'description')
    list_display_links = ['role_name']
    search_fields = ['role_name']

xadmin.site.register(CaseRole, CaseRoleAdmin)
