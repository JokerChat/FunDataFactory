# -*- coding: utf-8 -*- 
# @Time : 2022/8/7 21:59 
# @Author : junjie
# @File : __init__.py.py


from fastapi import APIRouter
from typing import List
from app.commons.responses.response_model import ResponseDto, ListResponseDto
from app.routers.user.apis import user_api
from app.routers.user.response_model.user_out import UserDto, UserTokenDto, SearchUserDto




router = APIRouter()

router.add_api_route("/register",
                     user_api.user_register,
                     methods=["post"],
                     name="用户注册",
                     description="用户注册",
                     response_model=ResponseDto)


router.add_api_route("/login",
                     user_api.user_login,
                     methods=["post"],
                     name="用户登录",
                     description="用户登录",
                     response_model=ResponseDto[UserTokenDto])


router.add_api_route("/list",
                     user_api.user_list,
                     methods=["get"],
                     name="用户列表",
                     response_model=ListResponseDto[List[UserDto]])


router.add_api_route("/logout",
            user_api.user_logout,
            methods=["get"],
            name="退出登录",
            description="退出登录",
            response_model=ResponseDto)


router.add_api_route("/update",
                     user_api.user_update,
                     methods=["post"],
                     name="更新用户",
                     response_model=ResponseDto)



router.add_api_route("/search",
                     user_api.user_search,
                     methods=["post"],
                     name="搜索用户",
                     response_model=ResponseDto[List[SearchUserDto]])
