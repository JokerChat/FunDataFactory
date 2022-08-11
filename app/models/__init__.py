# -*- coding: utf-8 -*- 
# @Time : 2022/5/3 08:57 
# @Author : junjie
# @File : __init__.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.commons.settings.config import Config

# Base是用来给模型类继承的
Base = declarative_base()

#创建同步数据库引擎
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_recycle=7200, pool_pre_ping=True)

#创建会话，autocommit自动提交，autoflush 自动刷新，bind 绑定创建的引擎
Session = sessionmaker(bind=engine)


