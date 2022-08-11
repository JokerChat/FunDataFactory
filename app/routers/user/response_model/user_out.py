# -*- coding: utf-8 -*- 
# @Time : 2022/8/7 22:04 
# @Author : junjie
# @File : user_out.py

from app.commons.responses.response_model import BaseDto
from datetime import datetime

class SearchUserDto(BaseDto):
    id: int
    username: str
    name: str
    email: str

class UserDto(SearchUserDto):
    role: int
    is_valid: bool
    create_time: datetime
    last_login_time: datetime


class UserTokenDto(UserDto):
    token: str