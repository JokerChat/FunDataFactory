# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 16:16 
# @Author : junjie
# @File : user.py

from datetime import datetime
from sqlalchemy import Column, String, INT, DATETIME, SMALLINT, func, Boolean
from app.models import Base
from config import Permission

class DataFactoryUser(Base):
    __tablename__ = "data_factory_user"

    id = Column(INT, primary_key=True, comment="主键id")
    username = Column(String(16), unique=True, nullable=False, comment="用户名")
    name =  Column(String(16), nullable=True, comment="姓名")
    password = Column(String(32), unique=False, comment="密码(md5加密)")
    email = Column(String(128),unique=True, nullable=True, comment="邮箱号")
    role = Column(SMALLINT, default=0, comment="0: 普通用户 1: 组长 2: 超管")
    last_login_time = Column(DATETIME, nullable=True, comment="上次登录时间")
    is_valid = Column(Boolean, nullable=False, default=False, comment="是否冻结")
    create_time = Column(DATETIME, nullable=False, comment="创建时间")
    update_code = Column(String(20), nullable=True, comment="更新人编码")
    update_name = Column(String(20), nullable=True, comment="更新人")
    update_time = Column(DATETIME, onupdate=func.now(), nullable=False, comment="更新时间")

    def __init__(self, username, name, password, email):
        self.username = username
        self.name = name
        self.password = password
        self.email = email
        self.role = Permission.MEMBERS
        self.is_valid = False
        self.create_time = datetime.now()
        self.update_time = datetime.now()
        self.last_login_time = datetime.now()
