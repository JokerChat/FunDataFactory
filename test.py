# -*- coding: utf-8 -*- 
# @Time : 2022/7/30 22:50 
# @Author : junjie
# @File : test.py

from pydantic import BaseModel, Field, EmailStr, ValidationError


class RegisterUserBody(BaseModel):

    username: str  = Field(..., title="用户名", description="必传")
    password: str = Field(..., title="密码", description="必传")
    name: str = Field(..., title="姓名", description="必传")
    email: EmailStr = Field(..., title="邮箱号", description="必传")
    class Config:
        error_msg_templates = {
            'value_error.missing': '不能为空'
        }
try:
    RegisterUserBody(username='x')
except ValidationError as e:
    print(e)