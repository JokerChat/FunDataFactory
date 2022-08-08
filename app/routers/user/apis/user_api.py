# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 18:14 
# @Author : junjie
# @File : user.py

from app.logic.user_logic import user_logic
from app.routers.user.request_model.user_in import RegisterUserBody, LoginUserBody, UpdateUserBody, SearchUserBody
from app.commons.responses.response_model import ResponseDto, ListResponseDto

def user_register(body: RegisterUserBody):
    user_logic.user_register_logic(body)
    return ResponseDto(msg="注册成功")


def user_login(body: LoginUserBody):
    user = user_logic.user_login_logic(body)
    return ResponseDto(data = user)


def user_list(page: int = 1, limit: int = 10, search: str = None):
    user_lists = user_logic.user_list_logic(page, limit, search)
    return ListResponseDto(data = user_lists)


def user_logout():
    user_logic.user_logout_logic()
    return ResponseDto(msg = "退出成功")


def user_update(body: UpdateUserBody):
    user_logic.user_update_logic(body)
    return ResponseDto(msg = "修改成功")



def user_search(body: SearchUserBody):
    user_lists = user_logic.user_search_logic(body)
    return ResponseDto(data = user_lists)