# -*- coding: utf-8 -*- 
# @Time : 2022/8/8 22:01 
# @Author : junjie
# @File : project_in.py


from pydantic import validator, Field
from typing import Optional
from app.commons.requests.request_model import BaseBody, ToolsSchemas
from app.constants.enums import PullTypeEnum, ProjectRoleEnum



class AddProject(BaseBody):
    project_name: str = Field(..., title="项目名称", description="必传")
    description: str = Field(None, title="项目描述", description="非必传")
    owner: str = Field(..., title="项目负责人", description="必传")
    directory: str = Field(..., title="脚本目录", description="必传")
    private: bool = Field(..., title="是否私有", description="必传")
    pull_type: PullTypeEnum = Field(..., title="拉取项目形式", description="必传")
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
            from app.commons.utils.encrypt_utils import AesUtils
            return AesUtils.encrypt(v)
        return v

class EditProject(AddProject):
    id : int=Field(..., title="项目id", description="主键id")

    @validator('id')
    def id_not_empty(cls, v):
        return ToolsSchemas.not_empty(v)


class AddProjectRole(BaseBody):
    project_id: int = Field(..., title="项目id", description="必传")
    project_role: ProjectRoleEnum = Field(..., title="项目权限", description="必传")
    user_id: int = Field(..., title="用户id", description="必传")


    @validator('project_id', 'project_role', 'user_id')
    def name_not_empty(cls, v):
        return ToolsSchemas.not_empty(v)

class EditProjectRole(BaseBody):
    project_role: ProjectRoleEnum = Field(..., title="项目权限", description="必传")
    id : int=Field(..., title="项目权限id", description="主键id")

    @validator('id', 'project_role')
    def id_not_empty(cls, v):
        return ToolsSchemas.not_empty(v)

class ProjectName(BaseBody):
    name: str = Field(..., title="项目名称", description="必传")

class GitProject(BaseBody):
    project: ProjectName