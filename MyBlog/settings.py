import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hf&ss)e1pr49yngt1s9ql%7wgotm91vsvw&88$67@3p@hlm%^e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 自己的应用
    'user.apps.UserConfig',
    # 图形验证码
    'captcha',
    # 文章应用
    'article',
    # xadmin,注意用xadmin的话，以下两个都要配置
    'xadmin',
    'crispy_forms'
    # ckeditor富文本
    # 'ckeditor',  # 不带图片上传功能
    # 'ckeditor_uploader',  # 带图片上传功能
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 配置自定义中间件
    # 'middleware.MyMiddleware.MiddleWare1',
    # 'middleware.MyMiddleware.MiddleWare2'

]

ROOT_URLCONF = 'MyBlog.urls'

# 如果用户继承了AbstractUser，修改原生auth_user的模型的话就需要加这个配置
AUTH_USER_MODEL = 'user.UserProfile'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 如果要在页面里面进行引用图片的话，就必须在这里添加配置
                'django.template.context_processors.media'  # 在模板中可以使用{{MEDIA_URL}}
            ],
        },
    },
]

WSGI_APPLICATION = 'MyBlog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

# 配置语言，时区
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
# 配置静态文件夹路径
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# 配置媒体文件路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# 配置富文本文件上传
CKEDITOR_UPLOAD_PATH = 'uploads/'

# 发送邮件配置
EMAIL_HOST = 'smtp.126.com'  # 发送邮件的邮箱的SMTP服务器，这里用的是163邮箱
EMAIL_PORT = 25  # 发件箱的SMTP服务器端口，默认是25
EMAIL_HOST_USER = 'mikasa0610@126.com'  # 发送邮件的邮箱地址
EMAIL_HOST_PASSWORD = 'JVPMNQPPSMIIFQET'  # 之前保存的授权码
EMAIL_USE_TLS = True  # 是否使用TLS安全传输协议(用于在两个通信应用程序之间提供保密性和数据完整性)
EMAIL_USE_SSL = False  # 是否使用SSL加密，qq企业邮箱要求使用，163邮箱设置为True的时候会报ssl的错误
