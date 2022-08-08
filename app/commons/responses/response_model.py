# -*- coding: utf-8 -*- 
# @Time : 2022/8/7 18:49 
# @Author : junjie
# @File : response_model.py

from pydantic import  Field
from typing import  TypeVar, Generic
from datetime import datetime
from pydantic.generics import GenericModel
from pydantic import BaseModel


DataT = TypeVar("DataT")

class ResponseDto(GenericModel, Generic[DataT]):
    code: int = Field(200, title="返参code")
    msg: str = Field('请求成功', title="返参msg")
    data: DataT = Field(None, title="返参data")  # 可能data没数据，没数据为null

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

class ListDto(GenericModel, Generic[DataT]):
    total: int = 0
    lists: DataT

class ListResponseDto(ResponseDto, Generic[DataT]):
    data: ListDto[DataT] = None


class BaseDto(BaseModel):
    # 返参基础模型
    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

def list_object_exclude(fields: list):
    exclude_map = {"data": {"__all__": {*fields}}}
    return exclude_map


def object_exclude(fields: list):
    exclude_map = {"data": {*fields}}
    return exclude_map


def list_exclude(fields: list):
    exclude_map = {"data": {"__all__": {*fields}}}
    return exclude_map