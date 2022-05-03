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
    DBNAME = "fun"

    # 数据库配置
    SQLALCHEMY_DATABASE_URI: str = f"mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DBNAME}"

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