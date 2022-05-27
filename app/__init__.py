# -*- coding: utf-8 -*- 
# @Time : 2022/5/3 08:56 
# @Author : junjie
# @File : __init__.py

import json
from fastapi import FastAPI, Request
from config import Text, HTTP_MSG_MAP
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.types import Message
from fastapi.exceptions import RequestValidationError
from app.models.base import ResponseDto
from fastapi.responses import JSONResponse
from app.utils.exception_utils import NormalException, AuthException, PermissionException
from app.utils.logger import Log
from app.routers import routers


fun = FastAPI(title=Text.TITLE, version=Text.VERSION, description=Text.DESCRIPTION)

#注册路由
for item in routers.data:
    fun.include_router(item[0], prefix=item[1], tags=item[2])

async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {"type": "http.request", "body": body}
    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.body()
    await set_body(request, body)
    return body

# 自定义http异常处理器
@fun.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    res = ResponseDto(code=201, msg=HTTP_MSG_MAP.get(exc.status_code, exc.detail))
    return JSONResponse(content=res.dict())

# 自定义参数校验异常处理器
@fun.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    message = ""
    for error in exc.errors():
        message += str(error.get('loc')[-1]) + ":" + str(error.get("msg"))+","
    res = ResponseDto(code=101, msg=f"请求参数非法! {message[:-1]}")
    return JSONResponse(content=res.dict())

# 手动捕获异常处理器
@fun.exception_handler(NormalException)
async def unexpected_exception_error(request: Request, exc: NormalException):
    log_msg = f"数据工厂捕获到异常, 请求路径: {request.url.path}\n"
    params = request.query_params
    headers = request.headers
    if params: log_msg += f"路径参数: {params}\n"
    if headers.get('content-type') == 'application/json':
        body = json.dumps(await request.json(), ensure_ascii=False)
        log_msg += f"请求参数: {body}"
    Log().info(log_msg)
    res = ResponseDto(code=110, msg=exc.detail)
    return JSONResponse(content=res.dict())

# 自定义权限异常
@fun.exception_handler(PermissionException)
async def unexpected_exception_error(request: Request, exc: PermissionException):
    res = ResponseDto(code=403, msg=HTTP_MSG_MAP.get(exc.status_code, exc.detail))
    return JSONResponse(content=res.dict())

# 自定义用户登录态异常
@fun.exception_handler(AuthException)
async def unexpected_exception_error(request: Request, exc: AuthException):
    res = ResponseDto(code=401, msg=HTTP_MSG_MAP.get(exc.status_code, exc.detail))
    return JSONResponse(content=res.dict())

# 全局捕获异常
@fun.middleware("http")
async def errors_handling(request: Request, call_next):
    log_msg = f"数据工厂捕获到系统错误, 请求路径:{request.url.path}\n"
    params = request.query_params
    body = await request.body()
    headers = request.headers
    if params:
        log_msg += f"路径参数: {params}\n"
    if body and headers.get('content-type') == 'application/json':
        try:
            body = json.dumps(json.loads(body), ensure_ascii=False)
            log_msg += f"请求参数: {body}\n"
        except:
            res = ResponseDto(code=102, msg='解析json失败')
            return JSONResponse(content=res.dict())
    try:
        await set_body(request, await request.body())
        return await call_next(request)
    except Exception as exc:
        import traceback
        log_msg += f"错误信息: {traceback.format_exc()}"
        # todo 发送报错消息到企微机器人/钉钉/飞书
        Log().error(log_msg)
        res = ResponseDto(code=500, msg=str(exc.args[0]))
        return JSONResponse(content=res.dict())