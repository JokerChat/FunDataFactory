# -*- coding: utf-8 -*- 
# @Time : 2022/5/22 22:53 
# @Author : junjie
# @File : auth_utils.py

import jwt
from jwt.exceptions import ExpiredSignatureError
from datetime import timedelta, datetime
from config import Config, Permission
from fastapi import Header
from app.utils.exception_utils import AuthException, PermissionException
# from functools import wraps




class UserToken(object):

    @staticmethod
    def get_token(data: dict) -> str:
        """
        :param data: 用户数据
        :return:
        """
        # 默认加密方式为 HS256, 过期时间 = 现在时间 + 配置过期时长
        token_data = dict({"exp": datetime.utcnow() + timedelta(hours=Config.EXPIRED_HOUR)}, **data)
        return jwt.encode(token_data, key=Config.KEY)

    @staticmethod
    def parse_token(token: str) -> dict:
        """解析token"""
        try:
            return jwt.decode(token, key=Config.KEY, algorithms=["HS256"])
        # token 过期
        except ExpiredSignatureError:
            raise Exception("token已过期, 请重新登录")
        # 解析失败
        except Exception:
            raise Exception("token解析失败, 请重新登录")


class Auth(object):

    def __init__(self, role: int = Permission.MEMBERS):
        self.role = role

    def __call__(self, token: str = Header(..., description="登录的token")):
        if not token:
            raise AuthException("token不能为空")
        try:
            user_info = UserToken.parse_token(token)
        except Exception as e:
            raise AuthException(str(e))
        if user_info.get('role', 0) < self.role:
            raise PermissionException('权限不足, 请联系管理员')
        return user_info

# # 用户登录态校验
# def auth(role):
#     @wraps(role)
#     def wrapper(func):
#         def inner(*args, **kwargs):
#             try:
#                 token = args[0]
#                 user_data = UserToken.parse_token(token)
#                 print("token校验好了，可以访问")
#                 if user_data['role'] < role:
#                     raise Exception('权限不足，不能访问')
#                 print("权限验证通过，可以访问")
#                 return func(*args, **kwargs)
#             except Exception as e:
#                 raise Exception(str(e))
#         return inner
#     return wrapper
#
#
# # 我是列表接口，需要登录后才能访问~
# # Permission.ADMIN  == 2
# @auth(3)
# def user_list(token):
#     return "这是列表接口数据"
#
# user_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTM2MTU3MjQsInVzZXJuYW1lIjoiZmFuZ2ppZSIsIm5hbWUiOiJmYW5nIiwiZW1haWwiOiI2NjQ2MTYxMTU4MUB4eC5jb20iLCJyb2xlIjoyLCJpc192YWxpZCI6ZmFsc2UsImxhc3RfbG9naW5fdGltZSI6IjIwMjItMDUtMjYgMjE6NDI6MDUifQ.LKb7_i7e8O9uOj4Lm8hrzucfF3SFw5Mect-_9aWsaE0'
# # user_token = 'fake_token'
# print(user_list(user_token))