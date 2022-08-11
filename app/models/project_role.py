# -*- coding: utf-8 -*- 
# @Time : 2022/6/18 22:01 
# @Author : junjie
# @File : project_role.py


from sqlalchemy import Column, INT, SMALLINT
from app.models.base import FunBaseModel
from app.routers.project.request_model.project_in import AddProjectRole


class DataFactoryProjectRole(FunBaseModel):
    """
    项目权限表
    """
    __tablename__ = 'data_factory_project_role'
    user_id = Column(INT, nullable=False, comment="用户id")
    project_id = Column(INT, nullable=False, comment="项目id")
    project_role = Column(SMALLINT, default=0, nullable=False, comment="0: 普通用户 1: 组长")

    def __init__(self, form: AddProjectRole, user, del_flag=0, id=None):
        super().__init__(create_id=user['id'], create_name=user['username'], del_flag=del_flag, id=id)
        self.user_id = form.user_id
        self.project_id = form.project_id
        self.project_role = form.project_role.value