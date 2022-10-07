# -*- coding: utf-8 -*- 
# @Time : 2022/7/21 07:14 
# @Author : junjie
# @File : expention_handler.py

from fastapi import Request
from app.commons.settings.config import HTTP_MSG_MAP
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from app.commons.responses.response_model import ResponseDto
from fastapi.responses import JSONResponse
from app.commons.exceptions.global_exception import BusinessException, AuthException, PermissionException
from pydantic import ValidationError
from app.commons.responses.response_code import CodeEnum
from loguru import logger
import json


# 自定义http异常处理器
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    res = ResponseDto(code=CodeEnum.HTTP_ERROR.code, msg=HTTP_MSG_MAP.get(exc.status_code, exc.detail))
    return JSONResponse(content=res.dict())


# 请求参数校验异常处理器
async def body_validation_exception_handler(request: Request, err: RequestValidationError):
    message = ""
    data = {}
    for raw_error in err.raw_errors:
        if isinstance(raw_error.exc, ValidationError):
            exc = raw_error.exc
            if hasattr(exc, 'model'):
                fields = exc.model.__dict__.get('__fields__')
                for field_key in fields.keys():
                    field_title =  fields.get(field_key).field_info.title
                    data[field_key] = field_title if field_title else field_key
            for error in exc.errors():
                field = str(error.get('loc')[-1])
                _msg = error.get("msg")
                message += f"{data.get(field, field)}{_msg},"
        elif isinstance(raw_error.exc, json.JSONDecodeError):
            message += 'json解析失败! '
    res = ResponseDto(code=CodeEnum.PARAMS_ERROR.code, msg=f"请求参数非法!{message[:-1]}")
    return JSONResponse(content=res.dict())

# 业务异常处理器
async def business_exception_handler(request: Request, exc: BusinessException):
    res = ResponseDto(code=exc.code, msg=exc.msg)
    return JSONResponse(content=res.dict())

# 权限异常处理器
async def role_exception_handler(request: Request, exc: PermissionException):
    res = ResponseDto(code=exc.code, msg=exc.msg)
    return JSONResponse(content=res.dict())

# 用户登录态异常处理处理器
async def auth_exception_handler(request: Request, exc: AuthException):
    res = ResponseDto(code=exc.code, msg=exc.msg)
    return JSONResponse(content=res.dict())

# todo 返回参数异常处理处理器
# async def res_validation_exception_handler(request: Request, exc: ValidationError):
#     res = ResponseDto(code=111, msg='demo')
#     return JSONResponse(content=res.dict())

# 全局系统异常处理器(中间件的异常都归类到这里来，统一处理)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, PermissionException):
        return await role_exception_handler(request, exc)
    elif isinstance(exc, AuthException):
        return await auth_exception_handler(request, exc)
    # elif isinstance(exc, ValidationError):
    #     return await res_validation_exception_handler(request, exc)
    else:
        import traceback
        logger.exception(traceback.format_exc())
        res = ResponseDto(code=CodeEnum.SYSTEM_ERROR.code, msg=CodeEnum.SYSTEM_ERROR.msg)
        return JSONResponse(content=res.dict())