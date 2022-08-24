# -*- coding: utf-8 -*- 
# @Time : 2022/8/23 22:49 
# @Author : junjie
# @File : cases_like.py

from sqlalchemy import Column,INT
from app.models.base import FunBaseModel

class DataFactoryCasesLike(FunBaseModel):
    """点赞表"""
    __tablename__ = 'data_factory_cases_like'

    cases_id = Column(INT, nullable=False, comment="造数场景id")

    def __init__(self, cases_id, user, del_flag=0, id=None):
        super().__init__(create_id=user['id'], create_name=user['username'], del_flag=del_flag, id=id)
        self.cases_id = cases_id
