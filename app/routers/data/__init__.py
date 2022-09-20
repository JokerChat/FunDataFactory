# -*- coding: utf-8 -*- 
# @Time : 2022/9/18 19:24 
# @Author : junjie
# @File : __init__.py.py

from typing import List
from fastapi import APIRouter
from app.routers.data.apis import data_api
from app.commons.responses.response_model import ResponseDto
from app.routers.data.response_model.data_out import DataSummaryDto


router = APIRouter()

router.add_api_route("/summary",
                     data_api.data_summary,
                     methods=["get"],
                     name="数据汇总",
                     response_model=ResponseDto[DataSummaryDto])