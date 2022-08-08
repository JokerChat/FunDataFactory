# -*- coding: utf-8 -*- 
# @Time : 2022/6/18 22:27 
# @Author : junjie
# @File : project_role_schema.py


from pydantic import BaseModel, validator, Field
from app.models.base import ToolsSchemas
from typing import Literal, List
from datetime import datetime
from app.models.base import ResponseDto,ListDto
from app.constants.enums import ProjectRoleEnum




class AddProjectRole(BaseModel):
    project_id: int = Field(..., title="项目id", description="必传")
    project_role: ProjectRoleEnum = Field(..., title="项目权限", description="必传")
    user_id: int = Field(..., title="用户id", description="必传")


    @validator('project_id', 'project_role', 'user_id')
    def name_not_empty(cls, v):
        return ToolsSchemas.not_empty(v)

class EditProjectRole(BaseModel):
    project_role: Literal[0, 1] = Field(..., title="项目权限", description="必传")
    id : int=Field(..., title="项目权限id", description="主键id")

    @validator('id', 'project_role')
    def id_not_empty(cls, v):
        return ToolsSchemas.not_empty(v)

class RoleDto(BaseModel):
    id: int
    username: str
    name: str
    email: str
    project_role: int
    project_id: int
    user_id: int
    create_name: str
    create_time: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

class RoleList(ListDto):
    lists: List[RoleDto]

class RoleListResDto(ResponseDto):
    data: RoleList
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }




