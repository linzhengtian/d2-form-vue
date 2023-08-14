"""
Django settings for d2Form project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys
import datetime
from mongoengine import connect
from kombu import Exchange, Queue
from .env import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e02$n$tpsi&rvjj7=5y!pi7b2$ku-+@5+6%#va7=oypuglxkn#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = locals().get('DEBUG', True)

ALLOWED_HOSTS = ["*"]

ASGI_APPLICATION = "d2Form.routing.application"

# Redis信息
# REDIS_HOST = '192.168.230.129'
# REDIS_PORT = 6379
# REDIS_DB = 2
# REDIS_PASSWORD = 'admin'

# channel配置
CHANNEL_LAYERS = {
    "default": {
        # This example app uses the Redis channel layer implementation channels_redis
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
            "symmetric_encryption_keys": [REDIS_PASSWORD],
        },
    },
}

# celery配置
CELERY_DB = locals().get('CELERY_REDIS_DB', 3)
CELERYD_FORCE_EXECV = True  # 降低死锁概率
CELERY_WORKER_CONCURRENCY = 2  # 设置并发worker数量
CELERY_TASK_ACKS_LATE = True
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_WORKER_MAX_TASKS_PER_CHILD = 40  # 每个worker最多执行多少个任务后销毁，防止内存泄漏
CELERY_TASK_TIME_LIMIT = 30 * 60  # 单个任务的最大允许时间
CELERY_TASK_TRACK_STARTED = True
CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD if REDIS_PASSWORD else ""}@{REDIS_HOST}:' \
             f'{REDIS_PORT}/{CELERY_DB}'  # Broker使用Redis
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_TASK_QUEUES = {  # celery5
    Queue("default", exchange=Exchange("default"), routing_key="default"),
    Queue("d2Form", exchange=Exchange("d2Form"), routing_key="d2Form"),
    Queue("beat_tasks", exchange=Exchange("beat_tasks"), routing_key="beat_tasks")
}
CELERY_TASK_ROUTES = {  # celery5
    'default': {'queue': 'default', 'routing_key': 'default'},
    'configuration.tasks.*': {'queue': 'd2Form', 'routing_key': 'd2Form'},
    'beat_tasks': {'queue': 'beat_tasks', 'routing_key': 'beat_tasks'},
}
# 设置默认队列
CELERY_TASK_DEFAULT_QUEUE = "d2Form"  # celery5
CELERY_TASK_DEFAULT_EXCHANGE = 'd2Form'  # celery5
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = 'direct'  # celery5，根据消息中routing_key发送给指定comsumer监听的queue中。
CELERY_TASK_DEFAULT_ROUTING_KEY = 'd2Form'  # celery5

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'django_celery_results',
    'django_filters',
    'django_jsonfield_backport',
    'rest_framework',
    'corsheaders', # 跨域
    'channels',
    'xadmin',
    'crispy_forms',
    'reversion',
    'ninja',
    'drf_yasg',  # swagger接口
    'captcha',
    'common.apps.CommonConfig',
    # app公共模块
    'apps.vadmin.permission',
    'apps.vadmin.op_drf',
    'apps.vadmin.system',
    'apps.vadmin.celery',
    'apps.vadmin.monitor',
    'modules.case',
    'modules.qform',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # 放在中间件的最上面，就是给响应头加上了一个响应头跨域
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'utils.middleware.RecordMiddleware',
    'apps.vadmin.op_drf.middleware.ApiLoggingMiddleware',  # 用于记录API访问日志
    'apps.vadmin.op_drf.middleware.PermissionModeMiddleware',  # 权限中间件

]

ROOT_URLCONF = 'd2Form.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'd2Form.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'permission.UserProfile'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_URL = '/login/'

TIME_FORMAT = '%Y-%m-%d %X'

# ================================================= #
# ************** REST_FRAMEWORK 配置  ************** #
# ================================================= #
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.vadmin.utils.authentication.RedisOpAuthJwtAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'apps.vadmin.op_drf.pagination.Pagination',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'EXCEPTION_HANDLER': 'apps.vadmin.utils.exceptions.op_exception_handler',
}

# 设置JWT过期时间
JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=60 * 60 * 24),  # JWT有效时间24小时
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',  # JWT的Header认证头以'JWT '开始
    'JWT_AUTH_COOKIE': 'AUTH_JWT',
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_PAYLOAD_HANDLER': 'apps.vadmin.utils.jwt_util.jwt_payload_handler',
    'JWT_GET_USER_SECRET_KEY': 'apps.vadmin.utils.jwt_util.jwt_get_user_secret_key',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'apps.vadmin.utils.jwt_util.jwt_response_payload_handler',
}

# CORS组的配置信息
CORS_ALLOW_CREDENTIALS = True  #所有域名都可以跨域访问

CORS_ORIGIN_ALLOW_ALL = True  #所有域名都可以跨域访问

CORS_ORIGIN_WHITELIST = ( ['http://*'] )

X_FRAME_OPTIONS = "ALLOW-FROM"

# # 实际请求所允许的请求方式列表。默认为：
# CORS_ALLOW_METHODS = (
#     'DELETE',
#     'GET',
#     'OPTIONS',
#     'PATCH',
#     'POST',
#     'PUT',
#     'VIEW',
# )
#
# # 发出实际请求时可以使用的非标准HTTP标头的列表。默认为:
# CORS_ALLOW_HEADERS = (
#     'XMLHttpRequest',
#     'X_FILENAME',
#     'accept-encoding',
#     'authorization',
#     'content-type',
#     'dnt',
#     'origin',
#     'user-agent',
#     'x-csrftoken',
#     'x-requested-with',
#     'Pragma',
# )

"""
日志配置
"""
# log 配置部分BEGIN #
SERVER_LOGS_FILE = os.path.join(BASE_DIR, 'logs', 'server.log')
ERROR_LOGS_FILE = os.path.join(BASE_DIR, 'logs', 'error.log')
if not os.path.exists(os.path.join(BASE_DIR, 'logs')):
    os.makedirs(os.path.join(BASE_DIR, 'logs'))

# 格式:[2020-04-22 23:33:01][micoservice.apps.ready():16] [INFO] 这是一条日志:
# 格式:[日期][模块.函数名称():行号] [级别] 信息
STANDARD_LOG_FORMAT = '[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s'
CONSOLE_LOG_FORMAT = '[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': STANDARD_LOG_FORMAT
        },
        'console': {
            'format': CONSOLE_LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'file': {
            'format': CONSOLE_LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': SERVER_LOGS_FILE,
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 5,  # 最多备份5个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': ERROR_LOGS_FILE,
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 3,  # 最多备份3个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        }
    },
    'loggers': {
        # default日志
        '': {
            'handlers': ['console', 'error', 'file'],
            'level': 'INFO',
        },
        # 数据库相关日志
        'django.db.backends': {
            'handlers': [],
            'propagate': True,
            'level': 'INFO',
        },
    }
}

# redis 缓存
REDIS_URL = f'redis://:{REDIS_PASSWORD if REDIS_PASSWORD else ""}@{os.getenv("REDIS_HOST") or REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
# 是否启用redis
REDIS_ENABLE = True
if locals().get("REDIS_ENABLE", True):
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
    }
    # CACHES = {
    #     'default': {
    #         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    #         'LOCATION': '/var/tmp/django_cache',
    #     }
    # }
    #
    # CACHE_MIDDLEWARE_KEY_PREFIX = ''
    # CACHE_MIDDLEWARE_SECONDS = 30
    # CACHE_MIDDLEWARE_ALIAS = 'default'
# ================================================= #
# ************** 登录方式配置  ************** #
# ================================================= #
AUTHENTICATION_BACKENDS = (
    'apps.vadmin.utils.backends.CustomBackend',
    'apps.vadmin.utils.backends.SessionAuthentication',
)
# username_field
USERNAME_FIELD = 'username'

# ================================================= #
# ************** 登录验证码配置  ************** #
# ================================================= #
CAPTCHA_STATE = locals().get('CAPTCHA_STATE', False)
# 字母验证码
CAPTCHA_IMAGE_SIZE = (160, 60)  # 设置 captcha 图片大小
CAPTCHA_LENGTH = 4  # 字符个数
CAPTCHA_TIMEOUT = 1  # 超时(minutes)
# 加减乘除验证码
CAPTCHA_OUTPUT_FORMAT = '%(image)s %(text_field)s %(hidden_field)s '
CAPTCHA_FONT_SIZE = 40  # 字体大小
CAPTCHA_FOREGROUND_COLOR = '#0033FF'  # 前景色
CAPTCHA_BACKGROUND_COLOR = '#F5F7F4'  # 背景色
CAPTCHA_NOISE_FUNCTIONS = (
    # 'captcha.helpers.noise_arcs', # 线
    # 'captcha.helpers.noise_dots', # 点
)
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'

# 是否开启非对称加密
CRYPT_CHECK = locals().get('CRYPT_CHECK', False)

API_LOG_ENABLE = True
# API_LOG_METHODS = 'ALL' # ['POST', 'DELETE']
# API_LOG_METHODS = ['POST', 'DELETE'] # ['POST', 'DELETE']
# ================================================= #
# ********************* 其他配置 ******************** #
# ================================================= #
# 接口权限
INTERFACE_PERMISSION = True
# 是否开启登录ip转换成城市位置
ENABLE_LOGIN_LOCATION = False
