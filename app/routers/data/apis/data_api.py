# -*- coding: utf-8 -*- 
# @Time : 2022/9/18 19:27 
# @Author : junjie
# @File : data_api.py

from app.logic.data_logic import data_logic
from app.commons.responses.response_model import ResponseDto

def data_summary():
    data = data_logic.data_summary_logic()
    return ResponseDto(data = data)