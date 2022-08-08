# -*- coding: utf-8 -*- 
# @Time : 2022/8/7 22:49 
# @Author : junjie
# @File : user_logic.py

import json
from app.crud.user.UserDao import UserDao
from app.routers.user.request_model.user_in import RegisterUserBody, LoginUserBody, UpdateUserBody, SearchUserBody
from app.routers.user.response_model.user_out import UserDto
from app.commons.utils.jwt_utils import UserToken
from app.commons.utils.context_utils import REQUEST_CONTEXT



def user_register_logic(body: RegisterUserBody):
    UserDao.register_user(body)

def user_login_logic(body: LoginUserBody):
    user = UserDao.user_login(body)
    # 将类加载数据到模型中
    user_model = UserDto.from_orm(user)
    # xx.dict() 返回模型的字段和值的字典
    # 返回表示 dict() 的 JSON 字符串，只有当转换为json，模型里面的编码规则(json_encoders)才生效
    user_data = user_model.json()
    token = UserToken.get_token(json.loads(user_data))
    setattr(user, "token", token)
    return user

def user_list_logic(page: int = 1, limit: int = 10, search: str = None):
    total, user_infos = UserDao.get_user_infos(page, limit, search)
    user_list = dict(total=total, lists=user_infos)
    return user_list

def user_logout_logic():
    # todo 退出登录删除清空redis token数据
    pass


def user_update_logic(body: UpdateUserBody):
    user = REQUEST_CONTEXT.get().user
    UserDao.update_user(body, user)

def user_search_logic(body: SearchUserBody):
    user_list = UserDao.search_user(body)
    return user_list
