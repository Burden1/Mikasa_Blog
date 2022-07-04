"""
    该类为工具类
    里面封装：发送短信等..
"""
import hashlib
import os
import uuid

from time import time

import requests
from django.core.mail import send_mail
from qiniu import Auth, put_file

from MyBlog.settings import EMAIL_HOST_USER, MEDIA_ROOT
from user.models import UserProfile


def send_api(req, tools="requests"):
    """
    封装发送请求工具（可以使用urlib3/requests）
    :param tools:
    :param req:
    :return:
    """
    if tools == "requests":
        return requests.request(**req)


def send_msg(mobile):
    """
    第三方接口：网易云信,发送短信验证码
    :param mobile: 手机号
    :return:
    """
    # 请求头四部分组成 AppKey + CurTime + CheckSum + Nonce
    AppKey = 'f766841d36d8d5282602b64274d151b1'  # 拿你的应用的appkey
    Nonce = 'mikasa'  # 随机数(不大于128即可)
    CurTime = str(int((time() * 1000)))  # 采用时间戳
    AppSecret = 'fcadf4c7164f'  # 拿你的应用的appSecret

    # SHA1(AppSecret + Nonce + CurTime)，三个参数拼接的字符串，进行SHA1哈希计算，转化成16进制字符(String，小写)
    content = AppSecret + Nonce + CurTime
    CheckSum = hashlib.sha1(content.encode('utf-8')).hexdigest()

    req = {
        "method": "POST",
        "url": 'https://api.netease.im/sms/sendcode.action',
        "headers": {
            'AppKey': AppKey,
            'Nonce': Nonce,
            'CurTime': CurTime,
            'CheckSum': CheckSum,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        "data": {
            'mobile': mobile
        }
    }
    print("req：", req)
    res = send_api(req)
    print("第三方响应结果：", res.json())
    return res.json()


def send_email(email, request):
    """
    发送邮件：给网易126邮箱
    :return:
    """
    subject = 'Mikasa个人博客找回密码'
    # 通过邮箱号查找到对应的用户数据
    user = UserProfile.objects.filter(email=email).first()
    # 让加密后的uuid等于用户id，并保存在session中
    ran_code = uuid.uuid4()
    print("替换前：", ran_code)
    ran_code = str(ran_code)  # uuid类型转为字符串类型
    ran_code = ran_code.replace('-', '')  # 将中间的-去掉
    print("替换后：", ran_code)
    request.session[ran_code] = user.id
    message = '''
        亲爱的用户：
            您好！此链接用于【用户找回密码】，请点击链接：<a href = 'http://127.0.0.1:8000/user/update_pwd?c=%s'>更新密码</a>
            
            如果链接不能点击，请复制以下链接在浏览器中打开即可：
            http://127.0.0.1:8000/user/update_pwd?c=%s
            
                                                                                                        Mikasa个人博客团队
    ''' % (ran_code, ran_code)
    # 发送邮件
    result = send_mail(subject, message, EMAIL_HOST_USER, [email, ])
    return result


def upload_img(store_obj, img_path):
    """
    上传图片：七牛云存储
    :param img_path:
    :param store_obj:
    :return:
    """
    # 1、去七牛云后台拿到你的密钥
    access_key = 'YDY-gnHSFf4sBq99JnjWEu3B9YqxeoKIYN5ssoNV'
    secret_key = 'lPHugocZtlqLTnWcRP-UZfEw5fxCa5p9I4KZsX_E'
    # 2、构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间名称
    bucket_name = 'mikasa-blog-space'
    # 上传后保存的文件名
    key = store_obj.name
    # 生成上传Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    locla_file = os.path.join(MEDIA_ROOT, img_path)
    ret, info = put_file(token, key, locla_file)  # 第三个参数是二进制流
    print(ret, info)
    # 拿到文件名
    file_name = ret.get('key')
    save_path = 'http://rdbjlwxgm.hn-bkt.clouddn.com/' + file_name
    return save_path
