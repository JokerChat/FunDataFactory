# -*- coding: utf-8 -*- 
# @Time : 2022/8/24 21:45 
# @Author : junjie
# @File : cases_out.py

from app.commons.responses.response_model import BaseDto
from datetime import datetime

class CaseGroupDto(BaseDto):
    group_name: str = None

class CaseDto(CaseGroupDto):
    id: int
    title: str = None
    name: str = None
    description: str = None
    header: str = None
    owner: str = None
    path: str = None
    param_in: str = None
    param_out: str = None
    example_param_in: str = None
    example_param_out: str = None

class CaseSearchDto(BaseDto):
    id: int
    title: str
    group_name: str


class CaseListDto(BaseDto):
    id: int
    title: str
    group_name: str
    description: str
    owner: str
    project_id: int
    like: bool
    like_num: int
    collection: bool
    collection_num: int
    update_time: datetime

class CaseDetailDto(CaseDto):
    project_id: int
    project_name: str
    git_project: str
    directory: str
    create_name: str
    create_time: datetime
    update_time: datetime

class CasesParamsDto(BaseDto):
    id: int
    name: str
    params: str
    out_id: str
    create_name: str
    update_name: str = None
    create_time: datetime
    update_time: datetime = None

class CasesRunDto(BaseDto):
    actual_request: dict
    actual_response: dict = None
    result: int
    requests_id: str
    cost: str
    log: str = None


class LogListDto(BaseDto):
    requests_id: str
    run_param_in: str
    run_param_out: str = None
    call_type: int
    run_status: int
    run_log: str = None
    title: str
    name: str
    group_name: str
    path: str
    project_name: str
    directory: str
    create_name: str
    create_time: datetime