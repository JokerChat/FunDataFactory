# -*- coding: utf-8 -*- 
# @Time : 2022/8/8 22:01 
# @Author : junjie
# @File : project_out.py
from app.commons.responses.response_model import BaseDto
from datetime import datetime
from typing import Union

class ProjectListDto(BaseDto):
    id: int
    project_name: str
    description: str = None
    owner: str
    update_time: datetime


class ProjectDetailDto(ProjectListDto):
    directory: str
    private: bool
    pull_type: int
    git_project: str
    git_url: str
    git_branch: str
    git_account: str = None
    git_password: str = None
    rsa_pub_key: Union[str, None]


class RoleDto(BaseDto):
    id: int
    username: str
    name: str
    email: str
    project_role: int
    project_id: int
    user_id: int
    create_name: str
    create_time: datetime

class CaseDto(BaseDto):
    id: int
    title: str = None
    name: str = None
    description: str = None
    group_name: str = None
    header: str = None
    owner: str = None
    path: str = None
    param_in: str = None
    param_out: str = None
    example_param_in: str = None
    example_param_out: str = None

class CaseListDto(BaseDto):
    data: CaseDto