# -*- coding: utf-8 -*- 
# @Time : 2022/9/4 17:28
# @Author : junjie
# @File : cases_params.py

from sqlalchemy import Column,INT,Text,String
from app.models.base import FunBaseModel

class DataFactoryCasesParams(FunBaseModel):
    """参数表"""
    __tablename__ = 'data_factory_cases_params'

    cases_id = Column(INT, nullable=False, comment="造数场景id")
    params = Column(Text, nullable=True, comment="请求参数")
    name = Column(String(32), nullable=False, comment="参数组合名称")
    out_id = Column(String(64), nullable=False, comment="外链id")

    def __init__(self, cases_id, params, name, out_id, user, del_flag=0, id=None):
        super().__init__(create_id=user['id'], create_name=user['username'], del_flag=del_flag, id=id)
        self.cases_id = cases_id
        self.params = params
        self.name = name
        self.out_id = out_id