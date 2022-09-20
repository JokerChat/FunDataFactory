# -*- coding: utf-8 -*- 
# @Time : 2022/8/9 07:23 
# @Author : junjie
# @File : __init__.py

from fastapi import APIRouter
from app.routers.project.apis import project_api
from app.routers.project.response_model.project_out import ProjectListDto, ProjectDetailDto, RoleDto, ProjectSyncDto
from app.commons.responses.response_model import ResponseDto, ListResponseDto
from typing import List


router = APIRouter()

router.add_api_route("/insert",
                     project_api.insert_project,
                     methods=["post"],
                     name="新增项目",
                     response_model=ResponseDto)


router.add_api_route("/update",
                     project_api.update_project,
                     methods=["post"],
                     name="编辑项目",
                     response_model=ResponseDto)


router.add_api_route("/delete",
                     project_api.delete_project,
                     methods=["get"],
                     name="删除项目",
                     response_model=ResponseDto)



router.add_api_route("/list",
                     project_api.get_project_infos,
                     methods=["get"],
                     name="项目列表",
                     response_model=ListResponseDto[List[ProjectListDto]])


router.add_api_route("/role/insert",
                     project_api.insert_project_role,
                     methods=["post"],
                     name="新增用户项目权限",
                     response_model=ResponseDto)


router.add_api_route("/role/update",
                     project_api.update_project_role,
                     methods=["post"],
                     name="更新用户项目权限",
                     response_model=ResponseDto)


router.add_api_route("/role/delete",
                     project_api.delete_project_role,
                     methods=["get"],
                     name="删除用户项目权限",
                     response_model=ResponseDto)


router.add_api_route("/role/list",
                     project_api.project_role_list,
                     methods=["get"],
                     name="获取项目权限成员列表",
                     response_model=ListResponseDto[List[RoleDto]])


router.add_api_route("/read",
                     project_api.read_project,
                     methods=["get"],
                     name="判断用户是否有项目查看权限",
                     response_model=ResponseDto)



router.add_api_route("/operation",
                     project_api.operation_project,
                     methods=["get"],
                     name="判断用户是否有项目操作权限",
                     response_model=ResponseDto)

router.add_api_route("/init",
                     project_api.init_project,
                     methods=["get"],
                     name="初始化项目",
                     response_model=ResponseDto)

router.add_api_route("/sync",
                     project_api.sync_project,
                     methods=["get"],
                     name="同步项目",
                     response_model=ResponseDto)

router.add_api_route("/detail",
                     project_api.project_detail,
                     methods=["get"],
                     name="项目详情",
                     response_model=ResponseDto[ProjectDetailDto])

router.add_api_route("/all",
                     project_api.sync_project_list,
                     methods=["get"],
                     name="获取用户所有有效项目",
                     response_model=ResponseDto[List[ProjectSyncDto]])

router.add_api_route("/gitSync",
                     project_api.sync_project_by_git,
                     methods=["post"],
                     name="git同步项目",
                     response_model=ResponseDto)