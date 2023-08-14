import os

# 数据库地址
DATABASE_HOST = os.environ.get("MYSQL_HOST", "localhost")
# 数据库端口
DATABASE_PORT = os.environ.get("MYSQL_PORT", 3306)
# 数据库用户名
DATABASE_USER = os.environ.get("MYSQL_USER", "root")
# 数据库密码
DATABASE_PASSWORD = os.environ.get("MYSQL_PASSWORD", "admin")
# 数据库名
DATABASE_NAME = os.environ.get("MYSQL_DATABASE", "d2form")
# Redis信息
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 2
CELERY_REDIS_DB = 3
REDIS_PASSWORD = "admin"
# 调试标签
DEBUG = False
# 是否开启非对称加密
CRYPT_CHECK = True
# 是否开启验证码
CAPTCHA_STATE = True
