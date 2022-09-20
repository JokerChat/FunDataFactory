# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 22:48 
# @Author : junjie
# @File : exception_utils.py


from app.commons.responses.response_code import CodeEnum
from typing import Any

class BusinessException(Exception):
    """业务异常处理类"""
    def __init__(self, msg: str = CodeEnum.BUSINESS_ERROR.msg) -> None:
        """
        初始化类
        :param msg: 错误信息
        """
        self.code = CodeEnum.BUSINESS_ERROR.code
        self.msg = msg



class AuthException(BusinessException):
    """登录态异常类"""
    def __init__(self, msg: str = CodeEnum.AUTH_ERROR.msg) -> None:
        self.code = CodeEnum.AUTH_ERROR.code
        self.msg = msg




class PermissionException(BusinessException):
    """用户权限不足异常类"""
    def __init__(self) -> None:
        self.code = CodeEnum.ROLE_ERROR.code
        self.msg = CodeEnum.ROLE_ERROR.msg