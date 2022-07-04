from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

import xadmin
from MyBlog.settings import MEDIA_ROOT
from user.views import index, about_me

"""
全局路径
"""
urlpatterns = [
    # path('admin/', admin.site.urls),
    # 配置xadmin路径
    path('xadmin/', xadmin.site.urls),
    # 首页
    path('', index, name='index'),

    # 配置user路径
    path('user/', include(('user.urls', 'user'), namespace='user')),
    # 配置article路径
    path('article/', include(('article.urls', 'article'), namespace='article')),
    # 配置captcha路由
    re_path(r'^captcha/', include('captcha.urls')),
    # 配置media路由
    # media直接去访问头像是访问不到的会报404，是因为我们没有配置media的路由
    # 参数1：正则表达式，匹配以media底下的所有path路径，参数2：serve，指定访问哪个文件夹
    # 参数3、指向文件夹的具体根路径
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 设置图片路由
    re_path(r'^ckeditor', include('ckeditor_uploader.urls')),

]
