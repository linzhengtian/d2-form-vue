from django.shortcuts import render_to_response
from django.shortcuts import render


def page_not_found(request, exception=None):
    # 全局404处理函数
    response=render_to_response('404.html',{})
    response.status_code=404
    return response


def page_error(request, exception=None):
    # 全局500处理函数
    response=render_to_response('500.html',{})
    response.status_code=500
    return response


def dashboard(request):
    return render(request, 'dashboard.html', locals())
