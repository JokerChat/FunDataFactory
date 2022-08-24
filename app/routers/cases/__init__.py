# -*- coding: utf-8 -*- 
# @Time : 2022/8/24 21:44 
# @Author : junjie
# @File : __init__.py.py

from fastapi import APIRouter
from app.routers.cases.apis import cases_api
from app.commons.responses.response_model import ResponseDto

router = APIRouter()

router.add_api_route("/like",
                     cases_api.like,
                     methods=["get"],
                     name="点赞场景",
                     response_model=ResponseDto)

router.add_api_route("/collection",
                     cases_api.collection,
                     methods=["get"],
                     name="收藏场景",
                     response_model=ResponseDto)