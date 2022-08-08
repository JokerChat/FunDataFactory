# -*- coding: utf-8 -*- 
# @Time : 2022/6/12 20:46 
# @Author : junjie
# @File : project.py

import os
from fastapi import APIRouter
from app.crud.project.ProjectDao import ProjectDao
from app.crud.project_role.ProjectRoleDao import ProjectRoleDao
from app.routers.project.project_schema import AddProject, EditProject, ProjectListResDto, ProjectDetailDto
from app.routers.project.project_role_schema import AddProjectRole, EditProjectRole, RoleListResDto
from app.models.base import ResponseDto
from app.commons.settings.config import FilePath
from app.core.git import Git
from app.commons.utils.aes_utils import AesUtils
from app.commons.utils.context_utils import REQUEST_CONTEXT

router = APIRouter()

@router.post("/insert", name="新增项目", response_model=ResponseDto)
def insert_project(body: AddProject):
    user = REQUEST_CONTEXT.get().user
    ProjectDao.insert_project(body, user)
    return ResponseDto(msg="新增成功")


@router.post("/update", name="编辑项目", response_model=ResponseDto)
def update_project(body: EditProject):
    user = REQUEST_CONTEXT.get().user
    ProjectDao.update_project(body, user)
    return ResponseDto(msg="编辑成功")


@router.get("/delete", name="删除项目", response_model=ResponseDto)
def delete_project(id: int):
    user = REQUEST_CONTEXT.get().user
    # todo: 暂时用不到，用_占坑，后续加入后置操作
    _ = ProjectDao.delete_project(id, user)
    return ResponseDto(msg="删除成功")



@router.get("/list", name="项目列表", response_model=ProjectListResDto)
def get_project_infos(page: int=1, limit: int=10, search=None):
    user = REQUEST_CONTEXT.get().user
    total, project_infos= ProjectDao.list_project(user, page, limit, search)
    return ProjectListResDto(data=dict(total=total, lists=project_infos))

@router.post("/role/insert", name="新增用户项目权限", response_model=ResponseDto)
def insert_project_role(data: AddProjectRole):
    user = REQUEST_CONTEXT.get().user
    ProjectRoleDao.insert_project_role(data, user)
    return ResponseDto(msg="新增成功")


@router.post("/role/update", name="更新用户项目权限", response_model=ResponseDto)
def update_project_role(data: EditProjectRole):
    user = REQUEST_CONTEXT.get().user
    ProjectRoleDao.update_project_role(data, user)
    return ResponseDto(msg="更新成功")



@router.get("/role/delete", name="删除用户项目权限", response_model=ResponseDto)
def delete_project_role(id):
    user = REQUEST_CONTEXT.get().user
    ProjectRoleDao.delete_project_role(id, user)
    return ResponseDto(msg="删除成功")


@router.get("/role/list", name="获取项目权限成员列表", response_model=RoleListResDto)
def project_role_list(project_id: int, page: int=1, limit: int=10, search=None):
    user = REQUEST_CONTEXT.get().user
    roles, count = ProjectRoleDao.project_role_list(user, project_id, page, limit, search)
    return RoleListResDto(data=dict(total=count, lists=roles))


@router.get("/read", name="判断用户是否有项目查看权限", response_model=ResponseDto)
def read_project(id: int):
    user = REQUEST_CONTEXT.get().user
    ProjectRoleDao.read_permission(id, user)
    return ResponseDto()


@router.get("/operation", name="判断用户是否有项目操作权限", response_model=ResponseDto)
def operation_project(id: int):
    user = REQUEST_CONTEXT.get().user
    ProjectRoleDao.operation_permission(id, user)
    return ResponseDto()

@router.get("/init", name="初始化项目", response_model=ResponseDto)
def init_project(id: int):
    user = REQUEST_CONTEXT.get().user
    project = ProjectDao.project_detail(id, user)
    project_path = os.path.join(FilePath.BASE_DIR, project.git_project)
    if os.path.isdir(project_path):
        raise Exception("项目已存在, 请执行刷新项目！")
    # 拉取项目
    if project.pull_type == 0:
        Git.git_clone_http(project.git_branch, project.git_url, project.git_account, AesUtils.decrypt(project.git_password))
    else:
        Git.git_clone_ssh(project.git_branch, project.git_url)
    return ResponseDto(msg = "初始化成功")


@router.get("/detail", name="项目详情", response_model=ResponseDto[ProjectDetailDto])
def project_detail(id: int):
    user = REQUEST_CONTEXT.get().user
    rsa_pub_key = None
    project = ProjectDao.project_detail(id, user)
    if project.pull_type == 1:
        from app.commons.settings.config import FilePath
        with open(FilePath.RSA_PUB_KEY, 'r', encoding='utf-8') as f:
            rsa_pub_key = f.read()
    setattr(project, 'rsa_pub_key', rsa_pub_key)
    return ResponseDto(data = project)