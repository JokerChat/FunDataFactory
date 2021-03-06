# -*- coding: utf-8 -*- 
# @Time : 2022/5/3 08:58 
# @Author : junjie
# @File : config.py

import os


#fastapi 启动配置文件
class Config(object):
    """配置类"""
    #数据库连接信息
    HOST = "127.0.0.1"
    PORT = "3306"
    PWD = "root"
    USER = "root"
    DBNAME = "datafactory"

    # 数据库配置
    SQLALCHEMY_DATABASE_URI: str = f"mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DBNAME}"

    KEY = "funDataFactory" # md5 盐值 / token key

    EXPIRED_HOUR = 12 # token过期时长

    AES_KEY = 'SVuRc6B7xsZnUWQO' # AES 秘钥
    AES_IV  = 'MUnDCU0aADgs4hd1' # AES 偏移量


class Text(object):
    """描述配置"""
    TITLE = "Fun数据工厂"
    VERSION = "v1.0"
    DESCRIPTION = "欢迎来到方总的数据工厂"


class FilePath(object):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # 后端服务项目目录

    LOG_FILE_PATH = os.path.join(BASE_DIR, "logs") # 日志文件路径
    if not os.path.isdir(LOG_FILE_PATH): os.mkdir(LOG_FILE_PATH)

    LOG_NAME = os.path.join(LOG_FILE_PATH, 'FunDataFactory.log')

    APP_PATH = os.path.join(BASE_DIR, "app") # app 路径

    CURD_PATH = os.path.join(APP_PATH, "curd")  # curd路径

    RSA_PUB_KEY = os.path.join(BASE_DIR, 'rsa_pub_key')

    RSA_PRI_KEY = os.path.join(BASE_DIR, 'rsa_pri_key')

class Permission(object):
    MEMBERS  = 0 # 普通用户
    LEADER = 1  # 组长
    ADMIN = 2  # 超管

HTTP_MSG_MAP = {
    404 : '请求路径找不到',
    405 : '请求方法不支持',
    408 : '请求超时',
    500 : '服务器内部错误',
    302 : '请求方法不支持'
}