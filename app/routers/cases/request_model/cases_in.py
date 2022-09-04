# -*- coding: utf-8 -*- 
# @Time : 2022/8/24 21:45 
# @Author : junjie
# @File : cases_in.py

import json
from pydantic import validator, Field
from app.commons.requests.request_model import BaseBody, ToolsSchemas

class AddCasesParams(BaseBody):
    cases_id: int = Field(..., title="造数场景id", description="必传")
    name: str = Field(..., title="参数组合名称", description="必传")
    params: str = Field(..., title="参数组合", description="必传")

    @validator('cases_id', 'name', 'params')
    def not_empty(cls, v):
        return ToolsSchemas.not_empty(v)

    @validator('params')
    def is_json(cls, v):
        try:
            json_object = json.loads(v)
        except:
            raise ValueError("params必须为json格式")
        return json.dumps(json_object)

class EditCasesParmas(AddCasesParams):
    id : int=Field(..., title="参数id", description="主键id")

    @validator('id')
    def id_not_empty(cls, v):
        return ToolsSchemas.not_empty(v)

