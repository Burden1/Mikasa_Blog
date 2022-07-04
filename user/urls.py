"""
    用户相关的路径
"""
from django.urls import path

from user.views import user_register, user_login, user_logout, code_login, send_code, forget_pwd, valid_code, \
    update_pwd, user_center, user_center1, about_me, leave_message, add_leave_msg

urlpatterns = [
    # 注册
    path('register', user_register, name='register'),
    # 登录
    path('login', user_login, name='login'),
    # 注销
    path('logout', user_logout, name='logout'),
    # 发送手机验证码
    path('send_code', send_code, name='send_code'),
    # 验证码登录
    path('codelogin', code_login, name='codelogin'),
    # 忘记密码
    path('forget_pwd', forget_pwd, name='forget_pwd'),
    # 校验图片验证码
    path('valid_code', valid_code, name='valid_code'),
    # 更新密码
    path('update_pwd', update_pwd, name='update_pwd'),
    # 用户个人中心
    path('user_center', user_center, name='user_center'),  # 本地存储
    path('user_center1', user_center1, name='user_center1'),  # 云存储

    # 关于我
    path('about', about_me, name='about'),

    # 留言列表
    path('leave_message', leave_message, name='leave_message'),
    # 添加留言
    path('add_leave_msg', add_leave_msg, name='add_leave_msg'),

]
