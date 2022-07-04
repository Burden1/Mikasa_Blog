import logging

from captcha.models import CaptchaStore
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.views import login
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from article.models import Article
from user import utils
from user.forms import RegisterForm, LoginForm, CaptchaTestForm
from user.models import UserProfile, LeaveMessage
from user.utils import send_email, upload_img

"""
    视图函数
"""


def index(request):
    """
    返回首页
    :param request:
    :return:
    """
    # 首页推荐文章：按照点赞数降序排列，默认拿前3条
    figure_articles = Article.objects.all().order_by('-click_num')[:3]
    # 时间轴文章：首页按时间降序排列，默认显示前4条
    darticles = Article.objects.all().order_by('-date')[:4]
    return render(request, "index.html", context={'figure_articles': figure_articles, 'darticles': darticles})


def about_me(request):
    """
    返回【关于我】页面
    :param request:
    :return:
    """
    return render(request, 'user/about.html')


def user_register(request):
    """
    用户注册
    :param request:
    :return:
    """
    if request.method == 'GET':  # 注意get一定要大写，不然无法将表单渲染在页面上
        return render(request, 'user/register.html')
    else:
        rform = RegisterForm(request.POST)  # 使用form获取数据
        print('--------》', rform)
        print("errors", rform.errors)
        if rform.is_valid():  # 进行数据的校验
            # 从干净的数据中取值，即通过前端校验的数据
            username = rform.cleaned_data.get('username')
            email = rform.cleaned_data.get('email')
            mobile = rform.cleaned_data.get('mobile')
            password = rform.cleaned_data.get('password')
            # 如果用户名/手机号不存在的话，才进行添加数据操作
            if not UserProfile.objects.filter(Q(username=username) | Q(mobile=mobile)).exists():
                # 注册到数据库中
                password = make_password(password)  # 密码进行加密
                user = UserProfile.objects.create(username=username, password=password, email=email, mobile=mobile)
                if user:
                    # 如果用户创建成功，则提示注册成功
                    return HttpResponse('注册成功')
            else:
                # 否则用户名/手机号已存在
                return render(request, 'user/register.html', context={'msg': '用户名或者手机号已经存在！'})
        # 数据校验失败，就提示注册失败
        return render(request, 'user/register.html', context={'msg': '用户名或者手机号已经存在，请重新填写！'})


def user_login(request):
    """
    用户登陆
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'user/login.html')
    else:
        lform = LoginForm(request.POST)
        print('--------》', lform)
        print("errors", lform.errors)
        if lform.is_valid():
            username = lform.cleaned_data.get('username')
            password = lform.cleaned_data.get('password')
            # 查询数据库,如果加密后的两个密码一致的话登录成功
            user = UserProfile.objects.filter(username=username).first()
            flag = check_password(password, user.password)
            if flag:
                # 登陆成功后，保存session信息，并进入首页
                # session信息会保存到django_session表中，并进行base64加密
                request.session['username'] = username
                return redirect(reverse('index'))
        return render(request, 'user/login.html', context={'errors': lform.errors, 'user': user})


def user_logout(request):
    """
    用户注销
    :param request:
    :return:
    """
    # 方法一、可自行清空session，再重定向到首页
    # request.session.clear() # 仅删除字典
    # 用户注销后，把session给清空，并且重定向回首页
    # request.session.flush()  # 删除django_session +cookie + 字典
    # return redirect(reverse('index'))

    # 方法二、若model类继承了AbstractUser，可直接使用系统自带的退出登录，即logout；不需要自己去清空session
    logout(request)
    return redirect(reverse('index'))


def send_code(request):
    """
    发送短信验证码：调用第三方网易云信
    :param request:
    :return:
    """
    # 1、获取到填写的手机号
    mobile = request.GET.get("mobile")
    data = {}
    if UserProfile.objects.filter(mobile=mobile).exists():
        # 2、判断手机号是否存在，存在则发送验证码给第三方，并拿到返回结果
        json_result = utils.send_msg(mobile)
        status = json_result.get("code")
        # 3、封装一下网易云信的返回信息
        if status == 200:
            check_code = json_result.get('obj')
            # 把验证码保存在session里面
            request.session['msg_code'] = check_code
            data['status'] = 200
            data['result'] = "验证码发送成功！"
        else:
            data['status'] = 500
            data['result'] = "验证码发送失败！"
    else:
        data['status'] = 501
        data['result'] = "用户不存在"
    return JsonResponse(data)


def code_login(request):
    """
    手机验证码登录：拿到第三方返回的短信验证码后，与页面输入的验证码进行校验
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'user/codelogin.html')
    else:
        # 1、拿到页面表单传的值
        mobile = request.POST.get('mobile')
        code = request.POST.get('code')

        # 2、根据mobile去session中取值
        check_code = request.session.get('msg_code')
        print("正确验证码：", check_code)
        # 校验验证码是否正确
        if code == check_code:
            # 若验证码正确，根据手机号查询数据库
            user = UserProfile.objects.filter(mobile=mobile).first()
            username = user.username
            if user:
                # 若用户存在，则登录
                login(request, user)
                request.session['username'] = username  # 拿到数据库里面的username，保存在session中返回给页面显示
                return redirect(reverse('index'))
            else:
                return HttpResponse("验证失败！")
        else:
            return render(request, 'user/codelogin.html', context={'msg': "验证码有误！"})


def forget_pwd(request):
    """
    忘记密码
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = CaptchaTestForm()
        return render(request, 'user/forget_pwd.html', context={'form': form})
    else:
        # 获取提交的邮箱，发送邮件，通过发送的邮箱链接设置新的密码
        email = request.POST.get('email')
        # 给此邮箱发送邮件
        result = send_email(email, request)
        if result == 1:
            return HttpResponse("您好，邮件发送成功！请尽快去邮箱查收。")


def valid_code(request):
    """
    校验图片验证码：采用了captcha图片验证码插件
    :param request:
    :return:
    """
    if request.is_ajax():
        # 1、拿到页面上的hashkey以及输入的验证码code
        key = request.GET.get('key')
        code = request.GET.get('code')
        # 2、CaptchaStore模型对象：根据key在表里找到对应的验证码数据
        captcha = CaptchaStore.objects.filter(hashkey=key).first()
        if captcha.response == code.lower():
            # 验证码正确
            data = {'status': 1}
        else:
            # 验证码错误
            data = {'status': 0}
        return JsonResponse(data)


def update_pwd(request):
    """
    更新密码
    :param request:
    :return:
    """
    if request.method == 'GET':
        c = request.GET.get('c')
        return render(request, 'user/update_pwd.html', context={'c': c})
    else:
        # 拿到页面的code
        code = request.POST.get('code')
        # 拿到之前保存在session里面的code
        uid = request.session.get(code)
        # 根据code查询数据库对应的用户数据
        user = UserProfile.objects.get(pk=uid)
        # 获取密码
        pwd = request.POST.get('password')
        repwd = request.POST.get('repassword')
        if pwd == repwd and user:
            pwd = make_password(pwd)
            user.password = pwd
            user.save()
            return render(request, 'user/update_pwd.html', context={'msg': '用户密码更新成功，请重新登陆！'})
        else:
            return render(request, 'user/update_pwd.html', context={'msg': '用户密码更新失败！'})


# @login_required
def user_center(request):
    """
    用户的个人中心：个人头像存储本地
    :param request:
    :return:
    """
    # 拿到之前登录时存在session里面的username
    username = request.session['username']
    user = UserProfile.objects.filter(username=username).first()
    if request.method == 'GET':
        return render(request, 'user/user_center.html', context={'user': user})
    else:
        # 获取到页面表单提交的属性
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        # icon是文件类型
        icon = request.FILES.get('icon')
        # 将获取到的属性设置给user对象里
        user.username = username
        user.email = email
        user.mobile = mobile
        if icon is None:
            # ImageField(upload_to='') 直接赋值icon过来，就会自动在static下面创建文件夹，
            # 这里创建的文件夹是之前我们在form表单里面定义的imagefield路径
            user.icon = user.icon
        else:
            user.icon = icon
        # 保存
        user.save()
        return render(request, 'user/user_center.html', context={'user': user})


# @login_required
def user_center1(request):
    """
    用户的个人中心1：个人头像存储七牛云
    :param request:
    :return:
    """
    # 拿到之前登录时存在session里面的username
    username = request.session['username']
    user = UserProfile.objects.filter(username=username).first()
    if request.method == 'GET':
        return render(request, 'user/user_center1.html', context={'user': user})
    else:
        # 获取到页面表单提交的属性
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        icon = request.FILES.get('icon')  # icon是内存存储对象
        user.username = username
        user.email = email
        user.mobile = mobile
        user.icon = icon
        user.save()

        # 将头像上传图片到七牛云
        # 注意：直接用user.icon会报错，因为他是一个ImageFieldFile对象，我们需要把他转为字符串
        sava_path = upload_img(icon, str(user.icon))  # 拿到七牛云存储的路径
        user.yunicon = sava_path
        # 保存
        user.save()
        return render(request, 'user/user_center1.html', context={'user': user})


def leave_message(request):
    """
    返回留言界面
    :param request:
    :return:
    """
    # 查询所有留言
    leave_msgs = LeaveMessage.objects.all().order_by('-create_time')
    return render(request, 'user/leave_message.html', context={'leave_msgs': leave_msgs})


def add_leave_msg(request):
    """
    添加留言
    :param request:
    :return:
    """
    # 拿到前端传的值
    nickname = request.GET.get('nickname')
    content = request.GET.get('saytext')
    # 昵称和内容都不为空时，保存数据库
    data = {}
    if nickname is not None and content is not None:
        leave_msg = LeaveMessage.objects.create(nickname=nickname, content=content)
        if leave_msg:
            data = {
                'status': 1,
                'msg': '留言成功'
            }
        else:
            data = {
                'status': 0,
                'msg': '留言成功'
            }
    else:
        logging.info("添加留言失败，请填写昵称和留言内容再添加噢！")
    return JsonResponse(data)
