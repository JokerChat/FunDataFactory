# -*- coding: utf-8 -*- 
# @Time : 2022/6/12 20:46 
# @Author : junjie
# @File : project.py


from fastapi import APIRouter, Depends
from app.curd.project.ProjectDao import ProjectDao
from app.curd.project_role.ProjectRoleDao import ProjectRoleDao
from app.routers.project.project_schema import AddProject, EditProject, ProjectListResDto
from app.routers.project.project_role_schema import AddProjectRole, EditProjectRole, RoleListResDto
from app.models.base import ResponseDto
from app.utils.auth_utils import Auth
from app.utils.exception_utils import NormalException
from config import Permission

router = APIRouter()

@router.post("/insert", name="新增项目", response_model=ResponseDto)
def insert_project(body: AddProject, user= Depends(Auth(Permission.LEADER))):
    try:
        ProjectDao.insert_project(body, user)
        return ResponseDto(msg="新增成功")
    except Exception as e:
        raise NormalException(str(e))

@router.post("/update", name="编辑项目", response_model=ResponseDto)
def update_project(body: EditProject, user= Depends(Auth())):
    try:
        ProjectDao.update_project(body, user)
        return ResponseDto(msg="编辑成功")
    except Exception as e:
        raise NormalException(str(e))


@router.get("/delete", name="删除项目", response_model=ResponseDto)
def delete_project(id: int, user= Depends(Auth())):
    try:
        # 暂时用不到，用_占坑，后续加入后置操作
        _ = ProjectDao.delete_project(id, user)
        return ResponseDto(msg="删除成功")
    except Exception as e:
        raise NormalException(str(e))

@router.get("/list", name="项目列表", response_model=ProjectListResDto)
def get_project_infos(page: int=1, limit: int=10, search=None, user= Depends(Auth())):
    try:
        total, project_infos= ProjectDao.list_project(user, page, limit, search)
        return ProjectListResDto(data=dict(total=total, lists=project_infos))
    except Exception as e:
        raise NormalException(str(e))

@router.post("/role/insert", name="新增用户项目权限", response_model=ResponseDto)
def insert_project_role(data: AddProjectRole, user= Depends(Auth())):
    try:
        ProjectRoleDao.insert_project_role(data, user)
        return ResponseDto(msg="新增成功")
    except Exception as e:
        raise NormalException(str(e))


@router.post("/role/update", name="更新用户项目权限", response_model=ResponseDto)
def update_project_role(data: EditProjectRole, user= Depends(Auth())):
    try:
        ProjectRoleDao.update_project_role(data, user)
        return ResponseDto(msg="更新成功")
    except Exception as e:
        raise NormalException(str(e))


@router.get("/role/delete", name="删除用户项目权限", response_model=ResponseDto)
def delete_project_role(id, user= Depends(Auth())):
    try:
        ProjectRoleDao.delete_project_role(id, user)
        return ResponseDto(msg="删除成功")
    except Exception as e:
        raise NormalException(str(e))


@router.get("/role/list", name="获取项目权限成员列表", response_model=RoleListResDto)
def project_role_list(project_id: int, page: int=1, limit: int=10, search=None, user= Depends(Auth())):
    try:
        roles, count = ProjectRoleDao.project_role_list(user, project_id, page, limit, search)
        return RoleListResDto(data=dict(total=count, lists=roles))
    except Exception as e:
        raise NormalException(str(e))


@router.get("/read", name="判断用户是否有项目查看权限", response_model=ResponseDto)
def read_project(id: int, user = Depends(Auth())):
    try:
        ProjectRoleDao.read_permission(id, user)
        return ResponseDto()
    except Exception as e:
        raise NormalException(str(e))


@router.get("/operation", name="判断用户是否有项目操作权限")
def operation_project(id: int, user = Depends(Auth())):
    try:
        ProjectRoleDao.operation_permission(id, user)
        return ResponseDto()
    except Exception as e:
        raise NormalException(str(e))