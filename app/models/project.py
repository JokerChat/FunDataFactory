# -*- coding: utf-8 -*- 
# @Time : 2022/6/12 20:08 
# @Author : junjie
# @File : project.py

from sqlalchemy import Column, String, UniqueConstraint, BOOLEAN, SMALLINT
from app.models.base import FunBaseModel
from app.routers.project.request_model.project_in import AddProject

class DataFactoryProject(FunBaseModel):
    """
    项目表
    """
    __tablename__ = 'data_factory_project'
    __table_args__ = (
        UniqueConstraint('id', 'git_url', 'project_name', 'del_flag'),
    )
    project_name = Column(String(64), nullable=False, comment="项目名称")
    description = Column(String(64), nullable=True, comment="项目描述")
    directory = Column(String(64), nullable=False, comment="脚本目录")
    owner = Column(String(64), nullable=False, comment="项目负责人")
    private = Column(BOOLEAN, nullable=False, default=False, comment="是否私有")
    pull_type = Column(SMALLINT, default=0, nullable=False, comment="拉取方式, 0: http 1: ssh")
    git_project = Column(String(64), nullable=False, comment="git项目名")
    git_url = Column(String(255), nullable=False, comment="git地址")
    git_branch = Column(String(32), nullable=False, comment="git分支名")
    git_account = Column(String(32), nullable=True, comment="git账号")
    git_password = Column(String(64), nullable=True, comment="git密码")

    def __init__(self, form: AddProject, user, del_flag=0, id=None):
        super().__init__(create_id=user['id'], create_name=user['username'], del_flag=del_flag, id=id)
        self.git_project = form.git_project
        self.project_name = form.project_name
        self.description = form.description
        self.directory = form.directory
        self.git_url = form.git_url
        self.git_branch = form.git_branch
        self.git_account = form.git_account
        self.git_password = form.git_password
        self.owner = form.owner
        self.private = form.private
        self.pull_type = form.pull_type.value