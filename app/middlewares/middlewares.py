# -*- coding: utf-8 -*- 
# @Time : 2022/7/20 14:27 
# @Author : junjie
# @File : middlewares.py

from app.commons.settings import config
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Scope, Receive, Send
from app.commons.utils.auth_utils import authentication
from starlette.middleware.base import BaseHTTPMiddleware
from app.commons.exceptions.expention_handler import global_exception_handler




class BaseMiddleware(object):
    """中间件基类"""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self,  scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        request = Request(scope, receive=receive)
        response = await self.before_request(request) or self.app
        await response(request.scope, request.receive, send)
        await self.after_request(request)

    async def get_body(self, request: Request) -> bytes:
        """获取请求body"""
        body = await request.body()
        return body

    async def before_request(self, request: Request) -> [Response, None]:
        """请求之前处理"""
        return self.app

    async def after_request(self, request: Request) -> None:
        """请求后处理"""
        return None


class AuthMiddleware(BaseMiddleware):
    """权限和登录态中间件"""
    async def before_request(self, request: Request):
        """白名单pass"""
        for api_url in config.API_WHITE_LIST:
            if str(request.url.path).startswith(api_url):
                return
        await authentication(request)

class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            return await global_exception_handler(request, exc)
