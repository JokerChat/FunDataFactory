# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 18:14 
# @Author : junjie
# @File : user.py
import json

from fastapi import APIRouter
from app.routers.user.user_schema import RegisterUserBody, LoginUserBody, LoginResDto, UserDto
from app.curd.user.UserDao import UserDao
from app.utils.exception_utils import NormalException
from app.models.base import ResponseDto
from app.utils.auth_utils import UserToken


router = APIRouter()

@router.post('/register', name='用户注册', description='用户注册', response_model=ResponseDto)
def register(data: RegisterUserBody):
    try:
        UserDao.register_user(**data.dict())
        return ResponseDto(msg='注册成功')
    except Exception as e:
        raise NormalException(str(e))


@router.post('/login', name='用户登录', description='用户登录', response_model=LoginResDto)
def login(data: LoginUserBody):
    try:
        user = UserDao.user_login(data)
        # 将类加载数据到模型中
        user_model = UserDto.from_orm(user)
        # xx.dict() 返回模型的字段和值的字典
        # 返回表示 dict() 的 JSON 字符串，只有当转换为json，模型里面的编码规则(json_encoders)才生效
        user_data = user_model.json()
        token = UserToken.get_token(json.loads(user_data))
        setattr(user, 'token', token)
        return LoginResDto(data=user)
    except Exception as e:
        raise NormalException(str(e))