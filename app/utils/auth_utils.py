# -*- coding: utf-8 -*- 
# @Time : 2022/5/22 22:53 
# @Author : junjie
# @File : auth_utils.py

import jwt
from jwt.exceptions import ExpiredSignatureError
from datetime import timedelta, datetime
from config import Config

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