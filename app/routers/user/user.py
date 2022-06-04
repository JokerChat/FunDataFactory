# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 18:14 
# @Author : junjie
# @File : user.py
import json

from fastapi import APIRouter
from app.routers.user.user_schema import RegisterUserBody, LoginUserBody, LoginResDto, UserDto, UserListResDto, UpdateUserBody
from app.curd.user.UserDao import UserDao
from app.utils.exception_utils import NormalException
from app.models.base import ResponseDto
from app.utils.auth_utils import UserToken, Auth
from fastapi import Depends
from config import Permission


router = APIRouter()

@router.post("/register", name="用户注册", description="用户注册", response_model=ResponseDto)
def register(data: RegisterUserBody):
    try:
        UserDao.register_user(**data.dict())
        return ResponseDto(msg="注册成功")
    except Exception as e:
        raise NormalException(str(e))


@router.post("/login", name="用户登录", description="用户登录", response_model=LoginResDto)
def login(data: LoginUserBody):
    try:
        user = UserDao.user_login(data)
        # 将类加载数据到模型中
        user_model = UserDto.from_orm(user)
        # xx.dict() 返回模型的字段和值的字典
        # 返回表示 dict() 的 JSON 字符串，只有当转换为json，模型里面的编码规则(json_encoders)才生效
        user_data = user_model.json()
        token = UserToken.get_token(json.loads(user_data))
        setattr(user, "token", token)
        return LoginResDto(data=user)
    except Exception as e:
        raise NormalException(str(e))


@router.get("/list", name="用户列表", response_model=UserListResDto)
def info_list(page: int = 1, limit: int = 10, search: str = None, _: dict= Depends(Auth())):
    try:
        total, user_infos = UserDao.get_user_infos(page, limit, search)
        return UserListResDto(data=dict(total=total, lists=user_infos))
    except Exception as e:
        raise NormalException(str(e))


@router.get("/logout",name="退出登录", description="退出登录", response_model=ResponseDto)
def logout(_: dict= Depends(Auth())):
    try:
        # todo 退出登录删除清空redis token数据
        return ResponseDto(msg="退出成功")
    except Exception as e:
        raise NormalException(str(e))


@router.post("/update", name="更新用户", response_model=ResponseDto)
def banch_role(data: UpdateUserBody, user = Depends(Auth(Permission.ADMIN))):
    try:
        UserDao.update_user(data, user)
        return ResponseDto(msg="修改成功")
    except Exception as e:
        raise NormalException(str(e))