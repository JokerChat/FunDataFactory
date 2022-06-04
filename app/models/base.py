# -*- coding: utf-8 -*- 
# @Time : 2022/5/15 22:06 
# @Author : junjie
# @File : base.py

from pydantic import BaseModel
from typing import Union
from datetime import datetime


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