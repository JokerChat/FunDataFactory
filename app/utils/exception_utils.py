# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 22:48 
# @Author : junjie
# @File : exception_utils.py

from fastapi import HTTPException
from typing import Any
import functools

# 通用捕获异常类
class NormalException(HTTPException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(status_code=200, detail=detail)

# 用户登录态
class AuthException(HTTPException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(status_code=200, detail=detail)

# 用户权限
class PermissionException(HTTPException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(status_code=200, detail=detail)



# 捕获异常装饰器
def record_log(func):
    functools.wraps(func)
    def wrapper(*args, **kwargs):
        cls = args[0]
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 如果不是主动抛出的异常就记录详细的日志
            if not isinstance(e, NormalException):
                # 获取函数名
                func_name = func.__name__
                import traceback
                err = traceback.format_exc()
                # 日志输出详细报错信息
                cls.log.error(f"{func_name}失败: {err}")
                raise Exception(str(e))
            return func(*args, **kwargs)
    return wrapper

