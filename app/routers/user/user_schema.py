# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 18:14 
# @Author : junjie
# @File : user_schems.py

from pydantic import BaseModel, validator, Field, EmailStr
from config import Config
import hashlib
from app.models.base import ToolsSchemas
from datetime import datetime
from app.models.base import ResponseDto


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


class UserDto(BaseModel):
    username: str
    name: str
    email: str
    role: int
    is_valid: bool
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

