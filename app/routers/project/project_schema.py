# -*- coding: utf-8 -*- 
# @Time : 2022/6/12 20:47 
# @Author : junjie
# @File : project_schema.py

from pydantic import BaseModel, validator, Field
from typing import Literal, Optional, List, Union
from app.models.base import ToolsSchemas
from datetime import datetime
from app.models.base import ResponseDto, ListDto



class AddProject(BaseModel):
    project_name: str = Field(..., title="项目名称", description="必传")
    description: str = Field(None, title="项目描述", description="非必传")
    owner: str = Field(..., title="项目负责人", description="必传")
    directory: str = Field(..., title="脚本目录", description="必传")
    private: bool = Field(..., title="是否私有", description="必传")
    pull_type: Literal[0, 1] = Field(..., title="拉取项目形式", description="必传")
    git_project: str = Field(..., title="git项目名", description="必传")
    git_url: str = Field(..., title="git地址", description="必传")
    git_branch: str = Field(..., title="git分支名", description="必传")
    git_account: Optional[str] = Field(..., title="git账号", description="非必传")
    git_password: Optional[str] = Field(..., title="git密码", description="非必传")

    @validator('project_name', 'owner', 'directory', 'private', 'git_project', 'pull_type', 'git_url','git_branch')
    def name_not_empty(cls, v):
        return ToolsSchemas.not_empty(v)

    @validator('git_account')
    def check_account(cls, v, values, **kwargs):
        if 'pull_type' in values and values['pull_type'] == 0:
            v = ToolsSchemas.not_empty(v)
            return v
        return v

    @validator('git_password')
    def check_pwd(cls, v, values, **kwargs):
        if 'pull_type' in values and values['pull_type'] == 0:
            v = ToolsSchemas.not_empty(v)
            from app.commons.utils.aes_utils import AesUtils
            return AesUtils.encrypt(v)
        return v

class EditProject(AddProject):
    id : int=Field(..., title="项目id", description="主键id")

    @validator('id')
    def id_not_empty(cls, v):
        return ToolsSchemas.not_empty(v)


class ProjectDto(BaseModel):
    id: int
    project_name: str
    description: str = None
    directory: str
    owner: str
    private: bool
    pull_type: int
    git_project: str
    git_url: str
    git_branch: str
    git_account: str = None
    git_password: str = None
    create_time: datetime
    update_time: datetime
    del_flag: int
    create_code: int
    create_name: str
    update_code: int = None
    update_name: str = None

    class Config:
        orm_mode = True
        # json_encoders = {
        #     datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        # }

class ProjectList(ListDto):
    lists: List[ProjectDto]

class ProjectListResDto(ResponseDto):
    data: ProjectList
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

class ProjectDetailDto(ProjectDto):
    rsa_pub_key: Union[str, None]