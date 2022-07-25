# -*- coding: utf-8 -*- 
# @Time : 2022/7/21 23:04 
# @Author : junjie
# @File : context_utils.py

import contextvars

from starlette.requests import Request

# 当前请求对象上下
REQUEST_CONTEXT: contextvars.ContextVar[Request] = contextvars.ContextVar('request', default=None)
