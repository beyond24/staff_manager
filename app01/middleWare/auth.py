# 自定义django中间件

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
import re

WHITE_LIST = [
    '/login/',
    '/image/code/',
    '/admin/',
    '/index/.*$'    # 也可以进行正则匹配
]

class M1(MiddlewareMixin):
    """ 中间件1 """

    def process_request(self, request):
        # 1.排除那些不需要登录就能访问的页面
        # request.path_info获取当前用户请求的URL
        path = request.path_info
        for i in WHITE_LIST:
            res = re.match(i, path)
            if res:
                return
        # 2.登录验证，若存在session，说明登录过，继续往下一个中间件走
        info_dict = request.session.get('info')
        if info_dict:
            return
        # 3.若没有登录，重定向
        return redirect('/login/')

    def process_response(self, request, response):

        return response