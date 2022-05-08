# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 18:14 
# @Author : junjie
# @File : user.py

from fastapi import APIRouter
from app.routers.user.user_schema import RegisterUserBody
from app.curd.user.UserDao import UserDao

router = APIRouter()

@router.post('/register', name='用户注册', description='用户注册')
def register(data: RegisterUserBody):
    UserDao.register_user(**data.dict())
    return dict(code=200, msg='注册成功')