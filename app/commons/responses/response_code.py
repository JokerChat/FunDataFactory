# -*- coding: utf-8 -*- 
# @Time : 2022/7/20 16:38 
# @Author : junjie
# @File : response_code.py

from app.constants.enums import BaseEnum

class CodeEnum(BaseEnum):
    """编码枚举类"""
    OK = (200, '请求成功')
    HTTP_ERROR = (201, 'HTTP错误')
    PARAMS_ERROR = (101, '请求参数错误')
    JSON_ERROR = (102, 'json解析失败')
    BUSINESS_ERROR = (110, '系统处理异常, 请重试')
    AUTH_ERROR = (401, '权限认证失败')
    ROLE_ERROR  = (403, '权限不足, 请联系管理员')
    SYSTEM_ERROR = (500, '系统内部错误, 请重试')

    @property
    def code(self) -> int:
        return self.value[0]

    @property
    def msg(self) -> str:
        return self.value[1]

if __name__ == '__main__':
    print(CodeEnum.get_member_values())

