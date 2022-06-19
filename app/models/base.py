# -*- coding: utf-8 -*- 
# @Time : 2022/5/15 22:06 
# @Author : junjie
# @File : base.py

from pydantic import BaseModel
from typing import Union
from datetime import datetime
from sqlalchemy import INT, DATETIME, Column, SMALLINT, func, String
from app.models import Base

class ResponseDto(BaseModel):
    code: int = 200
    msg: str = '请求成功'
    data: Union[dict, list, None] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

class ListDto(BaseModel):
    total: int = 0
    lists: list = []

class ToolsSchemas(object):

    @staticmethod
    def not_empty(v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ValueError("不能为空")
        if not isinstance(v, int):
            if not v:
                raise ValueError("不能为空")
        return v


class FunBaseModel(Base):
    id = Column(INT, primary_key=True, comment="主键id")
    create_time = Column(DATETIME, nullable=False, comment="创建时间")
    update_time = Column(DATETIME, onupdate=func.now(), nullable=False, comment="更新时间")
    del_flag = Column(SMALLINT, default=0, nullable=False, comment="0: 未删除 1: 已删除")
    create_code = Column(INT, nullable=True, comment="创建人id")
    create_name = Column(String(20), nullable=True, comment="创建人")
    update_code = Column(INT, nullable=True, comment="更新人id")
    update_name = Column(String(20), nullable=True, comment="更新人")
    #设置为True，代表为基类，不会被创建为表
    __abstract__ = True

    def __init__(self, create_code=None, create_name=None, update_code=None, update_name=None, del_flag=0, id = None):
        self.id = id
        self.create_time = datetime.now()
        self.update_time = datetime.now()
        self.del_flag = del_flag
        self.create_code = create_code
        self.create_name= create_name
        self.update_code = update_code
        self.update_name = update_name