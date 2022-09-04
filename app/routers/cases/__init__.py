# -*- coding: utf-8 -*- 
# @Time : 2022/8/24 21:44 
# @Author : junjie
# @File : __init__.py.py

from fastapi import APIRouter
from app.routers.cases.apis import cases_api
from app.commons.responses.response_model import ResponseDto, ListResponseDto
from typing import List
from app.routers.cases.response_model.cases_out import CaseSearchDto, CaseListDto, CaseDetailDto, CasesParamsDto

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

router.add_api_route("/group",
                     cases_api.get_user_groups,
                     methods=["get"],
                     name="业务线分组列表",
                     response_model=ResponseDto)

router.add_api_route("/search",
                     cases_api.search_case,
                     methods=["get"],
                     name="模糊搜索用例",
                     response_model=ResponseDto[List[CaseSearchDto]])

router.add_api_route("/list",
                     cases_api.case_list,
                     methods=["get"],
                     name="用例列表",
                     response_model=ListResponseDto[List[CaseListDto]])

router.add_api_route("/detail",
                     cases_api.case_detail,
                     methods=["get"],
                     name="用例详情",
                     response_model=ResponseDto[CaseDetailDto])

router.add_api_route("/params/insert",
                     cases_api.add_params,
                     methods=["post"],
                     name="添加参数组合",
                     response_model=ResponseDto)

router.add_api_route("/params/update",
                     cases_api.edit_params,
                     methods=["post"],
                     name="编辑参数组合",
                     response_model=ResponseDto)

router.add_api_route("/params/delete",
                     cases_api.delete_params,
                     methods=["get"],
                     name="删除参数组合",
                     response_model=ResponseDto)

router.add_api_route("/params/list",
                     cases_api.get_cases_params,
                     methods=["get"],
                     name="参数组合列表",
                     response_model=ListResponseDto[List[CasesParamsDto]])