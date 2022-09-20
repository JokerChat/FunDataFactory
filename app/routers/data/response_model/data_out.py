# -*- coding: utf-8 -*- 
# @Time : 2022/9/18 19:25 
# @Author : junjie
# @File : data_out.py
from app.commons.responses.response_model import BaseDto
from typing import List


class DataTypeDto(BaseDto):
    name: str
    value: int

class WeeklyDataDto(BaseDto):
    date: str
    call_count: int
    success_count: int
    exception_count: int
    error_count: int
    case_count: int


class DataSummaryDto(BaseDto):
    user: int
    project: int
    case: int
    group: int
    log: int
    success_rate: str
    run_type_data: List[DataTypeDto]
    call_type_data: List[DataTypeDto]
    group_data: List[DataTypeDto]
    weekly_data: List[WeeklyDataDto] = []