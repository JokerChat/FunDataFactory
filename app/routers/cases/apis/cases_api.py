# -*- coding: utf-8 -*- 
# @Time : 2022/8/24 21:45 
# @Author : junjie
# @File : cases_api.py

from app.logic.cases_logic import cases_logic
from app.commons.responses.response_model import ResponseDto

def like(id : int):
    result = cases_logic.like_logic(id)
    return ResponseDto(msg = "点赞成功" if result else "取消点赞成功")


def collection(id : int):
    result = cases_logic.collection_logic(id)
    return ResponseDto(msg = "收藏成功" if result else "取消收藏成功")