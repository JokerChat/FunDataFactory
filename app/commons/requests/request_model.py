# -*- coding: utf-8 -*- 
# @Time : 2022/8/7 22:02 
# @Author : junjie
# @File : request_model.py
from pydantic import BaseModel
from app.constants.constants import ERROR_MSG_TEMPLATES


class BaseBody(BaseModel):
    # 入参基础模型
    class Config:
        error_msg_templates = ERROR_MSG_TEMPLATES


class ToolsSchemas(object):
    @staticmethod
    def not_empty(v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ValueError("不能为空")
        if not isinstance(v, int):
            if not v:
                raise ValueError("不能为空")
        return v
