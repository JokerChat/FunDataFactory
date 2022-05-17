# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 18:14 
# @Author : junjie
# @File : user.py

from fastapi import APIRouter
from app.routers.user.user_schema import RegisterUserBody
from app.curd.user.UserDao import UserDao
from app.utils.exception_utils import NormalException
from app.models.base import ResponseDto

router = APIRouter()

@router.post('/register', name='用户注册', description='用户注册', response_model=ResponseDto)
def register(data: RegisterUserBody):
    try:
        UserDao.register_user(**data.dict())
        return ResponseDto(msg='注册成功')
    except Exception as e:
        raise NormalException(str(e))