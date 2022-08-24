# -*- coding: utf-8 -*- 
# @Time : 2022/8/24 22:28 
# @Author : junjie
# @File : cases_collection.py


from sqlalchemy import Column,INT
from app.models.base import FunBaseModel

class DataFactoryCasesCollection(FunBaseModel):
    """收藏表"""
    __tablename__ = 'data_factory_cases_collection'

    cases_id = Column(INT, nullable=False, comment="造数场景id")

    def __init__(self, cases_id, user, del_flag=0, id=None):
        super().__init__(create_id=user['id'], create_name=user['username'], del_flag=del_flag, id=id)
        self.cases_id = cases_id