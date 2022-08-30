# -*- coding: utf-8 -*- 
# @Time : 2022/8/24 21:45 
# @Author : junjie
# @File : cases_api.py

from app.logic.cases_logic import cases_logic
from app.commons.responses.response_model import ResponseDto, ListResponseDto

def like(id : int):
    result = cases_logic.like_logic(id)
    return ResponseDto(msg = "点赞成功" if result else "取消点赞成功")


def collection(id : int):
    result = cases_logic.collection_logic(id)
    return ResponseDto(msg = "收藏成功" if result else "取消收藏成功")

def get_user_groups():
    groups = cases_logic.get_user_groups_logic()
    return ResponseDto(data = groups)

def search_case(search: str):
    cases = cases_logic.search_case_logic(search)
    return ResponseDto(data = cases)

def case_list(page: int=1, limit: int=10, show: str = None,
                    project_id: int=None, case_id: int=None):
    cases_lists = cases_logic.case_list_logic(page, limit, show, project_id, case_id)
    return ListResponseDto(data = cases_lists)