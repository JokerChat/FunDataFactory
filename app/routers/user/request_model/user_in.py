# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 18:14 
# @Author : junjie
# @File : user_schems.py

import hashlib
from pydantic import validator, Field, EmailStr
from app.constants import constants
from app.constants.enums import PermissionEnum
from app.commons.requests.request_model import BaseBody, ToolsSchemas


class RegisterUserBody(BaseBody):
    username: str  = Field(..., title="用户名", description="必传")
    password: str = Field(..., title="密码", description="必传")
    name: str = Field(..., title="姓名", description="必传")
    email: EmailStr = Field(..., title="邮箱号", description="必传")

    @validator('username', 'password', 'name', 'email')
    def check_field(cls, v):
        return ToolsSchemas.not_empty(v)

    @validator('password')
    def md5_paw(cls, value):
        m = hashlib.md5()
        m.update(f"{value}key={constants.TOKEN_KEY}".encode("utf-8"))
        return m.hexdigest()

class LoginUserBody(BaseBody):
    username: str = Field(..., title="用户名", description="必传")
    password: str = Field(..., title="密码", description="必传")

    @validator('username', 'password')
    def check_field(cls, v):
        return ToolsSchemas.not_empty(v)

    @validator('password')
    def md5_paw(cls, value):
        m = hashlib.md5()
        m.update(f"{value}key={constants.TOKEN_KEY}".encode("utf-8"))
        return m.hexdigest()

class UpdateUserBody(BaseBody):
    id: int = Field(..., title="用户id", description="必传")
    role: PermissionEnum = Field(None, title="用户权限", description="非必传")
    is_valid: bool = Field(None, title="是否冻结", description="非必传")

    @validator('id', 'role', 'is_valid')
    def check_field(cls, v):
        return ToolsSchemas.not_empty(v)


class SearchUserBody(BaseBody):
    keyword: str = Field(..., title="搜索内容", description="必传")

    @validator('keyword')
    def check_field(cls, v):
        return ToolsSchemas.not_empty(v)