# -*- coding: utf-8 -*- 
# @Time : 2022/8/21 18:59 
# @Author : junjie
# @File : cases.py


from sqlalchemy import Column, String, Text, INT
from app.models.base import FunBaseModel

class DataFactoryCases(FunBaseModel):
    """脚本表"""
    __tablename__ = 'data_factory_cases'
    project_id = Column(INT, nullable=False, comment="项目id")
    title = Column(String(255), nullable=False, comment="标题")
    name = Column(String(255), nullable=False, comment="方法名")
    description = Column(String(512), nullable=False, comment="描述信息")
    group_name = Column(String(255), nullable=False, comment="分组名")
    header = Column(Text, nullable=True, comment="请求头")
    owner = Column(String(255), nullable=False, comment="负责人")
    path = Column(String(255), nullable=False, comment="脚本路径")
    param_in = Column(Text, nullable=True, comment="请求参数")
    param_out = Column(Text, nullable=True, comment="返回参数")
    example_param_in = Column(Text, nullable=True, comment="请求示例")
    example_param_out = Column(Text, nullable=True, comment="返回示例")


    def __init__(self, project_id, title, name, description, group_name, header, owner, path, param_in, param_out, example_param_in, example_param_out, user, del_flag=0, id=None):
        super().__init__(create_id=user['id'], create_name=user['username'], del_flag=del_flag, id=id)
        self.project_id = project_id
        self.title = title
        self.name = name
        self.description = description
        self.group_name = group_name
        self.header = header
        self.owner = owner
        self.path = path
        self.param_in = param_in
        self.param_out = param_out
        self.example_param_in = example_param_in
        self.example_param_out = example_param_out