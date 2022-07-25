# -*- coding: utf-8 -*- 
# @Time : 2022/5/22 22:53 
# @Author : junjie
# @File : auth_utils.py

import config
from app.commons.utils.jwt_utils import UserToken
from app.commons.utils.context_utils import REQUEST_CONTEXT
from app.commons.exceptions.global_exception import AuthException, PermissionException
from starlette.requests import Request
from app.constants.enums import PermissionEnum

async def authentication(request: Request):
    # 从请求中获取token`
    token = request.headers.get('token') or None
    if not token:
        raise AuthException()
    try:
        user_info = UserToken.parse_token(token)
    except Exception as e:
        raise AuthException(str(e))
    # todo 通过user_id 查询用户信息
    role = user_info.get('role') or PermissionEnum.MEMBERS.value
    if role < PermissionEnum.ADMIN.value and str(request.url.path) in config.API_ADMIN_LIST:
        raise PermissionException()
    if role < PermissionEnum.LEADER.value and str(request.url.path) in config.API_LEADER_LIST:
        raise PermissionException()
    request.scope['user'] = user_info



async def request_context(request: Request):
    print(id(request))
    """ 保存当前request对象到上下文中 """
    REQUEST_CONTEXT.set(request)