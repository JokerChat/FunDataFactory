# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 18:14 
# @Author : junjie
# @File : user_schems.py

from pydantic import BaseModel, validator, Field, EmailStr
from config import Config, Permission
import hashlib
from app.models.base import ToolsSchemas
from datetime import datetime
from app.models.base import ResponseDto,ListDto
from typing import List


class RegisterUserBody(BaseModel):

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
        m.update(f"{value}key={Config.KEY}".encode("utf-8"))
        return m.hexdigest()

class LoginUserBody(BaseModel):
    username: str = Field(..., title="用户名", description="必传")
    password: str = Field(..., title="密码", description="必传")

    @validator('username', 'password')
    def check_field(cls, v):
        return ToolsSchemas.not_empty(v)

    @validator('password')
    def md5_paw(cls, value):
        m = hashlib.md5()
        m.update(f"{value}key={Config.KEY}".encode("utf-8"))
        return m.hexdigest()

class UpdateUserBody(BaseModel):
    id: int = Field(..., title="用户id", description="必传")
    role: int = Field(None, title="用户权限", description="非必传")
    is_valid: bool = Field(None, title="是否冻结", description="非必传")

    @validator('id', 'role', 'is_valid')
    def check_field(cls, v):
        return ToolsSchemas.not_empty(v)

    @validator('role')
    def check_role_map(cls, value):
        if value not in vars(Permission).values():
            raise ValueError('角色类型有误')
        return value

class UserDto(BaseModel):
    id: int
    username: str
    name: str
    email: str
    role: int
    is_valid: bool
    create_time: datetime
    last_login_time: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }


class UserTokenDto(UserDto):
    token: str


class LoginResDto(ResponseDto):
    msg: str = '登录成功'
    data: UserTokenDto

class UserList(ListDto):
    lists: List[UserDto]

class UserListResDto(ResponseDto):
    data: UserList
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }