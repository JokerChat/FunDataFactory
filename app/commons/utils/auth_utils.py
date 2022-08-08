# -*- coding: utf-8 -*- 
# @Time : 2022/5/22 22:53 
# @Author : junjie
# @File : auth_utils.py
from app.commons.settings import config
from app.commons.utils.jwt_utils import UserToken
from app.commons.utils.context_utils import REQUEST_CONTEXT
from app.commons.exceptions.global_exception import AuthException, PermissionException
from starlette.requests import Request
from app.constants.enums import PermissionEnum
from app.crud.user.UserDao import UserDao
from app.routers.user.response_model.user_out import UserDto

async def authentication(request: Request):
    # 从请求中获取token`
    token = request.headers.get('token') or None
    if not token:
        raise AuthException()
    try:
        user_info = UserToken.parse_token(token)
    except Exception as e:
        raise AuthException(str(e))
    # 通过数据库查询最新的用户信息
    user = UserDao.get_with_id(id = user_info.get('id'))
    if user is None:
        raise AuthException("用户不存在")
    role = user.role or PermissionEnum.members.value
    if role < PermissionEnum.admin.value and str(request.url.path) in config.API_ADMIN_LIST:
        raise PermissionException()
    if role < PermissionEnum.leader.value and str(request.url.path) in config.API_LEADER_LIST:
        raise PermissionException()
    user_dict = UserDto.from_orm(user)
    request.scope['user'] = user_dict.dict()



async def request_context(request: Request):
    """ 保存当前request对象到上下文中 """
    REQUEST_CONTEXT.set(request)