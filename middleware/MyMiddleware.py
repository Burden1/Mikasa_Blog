"""
    自定义中间件
    中间件是一个面向对象的类，有五个方法
        1、Request预处理函数：process_request(self, request)
            运行时间：在请求后，在process_view 之前，在执行views之前
        2、View预处理函数： process_view(self, request, callback, callback_args,callback_kwargs)
            运行时间：在process_request之后，在views之前
        3、Template模版渲染函数：process_template_response()
            运行时间：默认不执行，只有在视图函数的返回结果对象中有render方法才会执行，
            并把对象的render方法的返回值返回给用户（注意不返回视图函数的return的结果了，
            而是返回视图函数 return值（对象）中rende方法的结果）
        4、Exception后处理函数：process_exception(self, request, exception)
            运行时间：这个方法只有在 request 处理过程中出了问题
            并且view函数抛出了一个未捕获的异常时才会被调用。这个钩子可以用来发送错误通知，
            将现场相关信息输出到日志文件，或者甚至尝试从错误中自动恢复。
        5、Response后处理函数：process_response(self, request, response)
            运行时间：这个方法的调用时机在 Django 执行 view 函数并生成 response 之后。
            该处理器能修改response 的内容；一个常见的用途是内容压缩，如gzip所请求的HTML页面
"""
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse

# 中间件使用方法：
#   方法1、
#       --> 首先需要自定义类继承MiddlewareMixin类；然后重写里面的5方法
#       --> setting.py中配置自定义中间件类

# 定义需要登录状态的路由list
login_list = ['/user/user_center', ]


class MiddleWare1(MiddlewareMixin):
    def process_request(self, request):
        print('---------------->1')
        """
            Request预处理函数,重写方法
        """
        # 我们可以通过request对象获取里请求里面的相关值，request对象其实就是view function函数的request
        # 相关获取例如：request.META、request.META['REMOTE_HOST']、request.path
        print(request.META['REMOTE_ADDR'])  # 获取请求的远程地址
        path = request.path  # 拿到当前的请求路径
        if path in login_list:  # 判断当前请求路径是否在定义的路由list中
            # todo : 待解决bug， 这个已登录对象user的值没有拿到
            print("user:", request.user)  # AnoymousUser：即匿名对象，未登录
            # 如果在，判断请求user认证是否通过，不通过的话我们就直接重定向到登录界面，类似做了一层拦截访问
            if not request.user.is_authenticated:
                return redirect(reverse('user:login'))


class MiddleWare2(MiddlewareMixin):
    # 重写方法
    def process_request(self, request):
        print('------------------->2')
