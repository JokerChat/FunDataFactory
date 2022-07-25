# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 18:14 
# @Author : junjie
# @File : user.py
import json
from fastapi import APIRouter
from app.routers.user.user_schema import RegisterUserBody, LoginUserBody, UserTokenDto, UserDto, UpdateUserBody, SearchUserBody
from app.curd.user.UserDao import UserDao
from app.models.base import ResponseDto, ListResponseDto, list_object_exclude
from app.commons.utils.jwt_utils import UserToken
from typing import List
from fastapi import Request
from app.commons.utils.context_utils import REQUEST_CONTEXT



router = APIRouter()

@router.post("/register", name="用户注册", description="用户注册", response_model=ResponseDto)
def register(data: RegisterUserBody):
    UserDao.register_user(**data.dict())
    return ResponseDto(msg="注册成功")


@router.post("/login", name="用户登录", description="用户登录", response_model=ResponseDto[UserTokenDto])
def login(data: LoginUserBody):
    user = UserDao.user_login(data)
    # 将类加载数据到模型中
    user_model = UserDto.from_orm(user)
    # xx.dict() 返回模型的字段和值的字典
    # 返回表示 dict() 的 JSON 字符串，只有当转换为json，模型里面的编码规则(json_encoders)才生效
    user_data = user_model.json()
    token = UserToken.get_token(json.loads(user_data))
    setattr(user, "token", token)
    return ResponseDto(data = user)


@router.get("/list", name="用户列表", response_model=ListResponseDto[List[UserDto]])
def info_list(page: int = 1, limit: int = 10, search: str = None):
    cur_request = REQUEST_CONTEXT.get()
    print(cur_request.user)
    total, user_infos = UserDao.get_user_infos(page, limit, search)
    return ListResponseDto(data=dict(total=total, lists=user_infos))


@router.get("/logout",name="退出登录", description="退出登录", response_model=ResponseDto)
def logout():
    # todo 退出登录删除清空redis token数据
    return ResponseDto(msg="退出成功")


@router.post("/update", name="更新用户", response_model=ResponseDto)
def banch_role(request: Request, data: UpdateUserBody):
    user = request.user
    UserDao.update_user(data, user)
    return ResponseDto(msg="修改成功")



@router.post("/search", name="搜索用户", response_model=ResponseDto[List[UserDto]], response_model_exclude = list_object_exclude(["role", "is_valid", "create_time", "last_login_time"]))
def banch_role(body: SearchUserBody):
    user_list = UserDao.search_user(body)
    return ResponseDto(data=user_list)