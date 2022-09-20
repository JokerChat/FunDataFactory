# -*- coding: utf-8 -*- 
# @Time : 2022/7/18 23:20 
# @Author : junjie
# @File : constants.py


TOKEN_KEY = "funDataFactory"  # md5 盐值 / token key

TOKEN_EXPIRED_HOUR = 12  # token过期时长

AES_KEY = 'SVuRc6B7xsZnUWQO'  # AES 秘钥

AES_IV = 'MUnDCU0aADgs4hd1'  # AES 偏移量

ADMIN  = {
    "username": "admin",
    "id": 0
}

ERROR_MSG_TEMPLATES = {
    "value_error.missing": "必须传值",
    "value_error.extra": "不允许额外字段",
    "type_error.none.not_allowed": "不能为空",
    "type_error.bool": "必须为bool类型",
    "value_error.byte": "必须为byte类型",
    "value_error.dict": "必须为object类型",
    "value_error.email": "不是有效的邮箱地址",
    "type_error.integer": "必须为int类型",
    "type_error.float": "必须为float类型",
    "type_error.path": "不是有效的路径",
    "type_error.list": "必须为list类型",
    "type_error.str": "必须为str类型",
    "type_error.enum": "类型有误"
}

USER_AGENT = 'git-oschina-hook'

SECRET = 'fangjunjie1996'