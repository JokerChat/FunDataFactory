# -*- coding: utf-8 -*- 
# @Time : 2022/6/12 20:46 
# @Author : junjie
# @File : project.py


from fastapi import APIRouter, Depends
from app.curd.project.ProjectDao import ProjectDao
from app.routers.project.project_schema import AddProject, ProjectResDto
from app.utils.auth_utils import Auth
from app.utils.exception_utils import NormalException
from config import Permission

router = APIRouter()

@router.post("/insert", name="新增项目", response_model=ProjectResDto)
def insert_project(body: AddProject, user= Depends(Auth(Permission.LEADER))):
    try:
        project = ProjectDao.insert_project(body, user)
        return ProjectResDto(data=project, msg="新增成功")
    except Exception as e:
        raise NormalException(str(e))