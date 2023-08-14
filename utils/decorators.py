# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      decorators
   Description:
   Author:          LinZhengTian
   date：           2018-12-20
-------------------------------------------------
   Change Activity:
                    2018-12-20:
-------------------------------------------------
"""
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test


def admin_auth(func):
    """
    验证用户是否是超级管理员
    """
    @wraps(func)
    def returned_wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return returned_wrapper


def staff_auth(func):
    """
    验证用户是否处于职员状态
    """
    @wraps(func)
    def returned_wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return returned_wrapper


def permission_alternate_required(perm, login_url=None, raise_exception=False):
    """
    Override for alternate permission check.
    """
    def check_perms(user):
        if isinstance(perm, str):
            perms = (perm, )
        else:
            perms = perm
        for p in perms:
            if user.has_perm(p):
                return True
        if raise_exception:
            raise PermissionDenied
        return False
    return user_passes_test(check_perms, login_url=login_url)

