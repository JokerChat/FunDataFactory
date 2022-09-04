# -*- coding: utf-8 -*- 
# @Time : 2022/8/7 23:34 
# @Author : junjie
# @File : project_logic.py


import os
from concurrent.futures import ThreadPoolExecutor, ALL_COMPLETED, wait
from app.crud.project.ProjectDao import ProjectDao, DataFactoryProject
from app.crud.project_role.ProjectRoleDao import ProjectRoleDao
from app.routers.project.request_model.project_in import AddProject, EditProject, AddProjectRole, EditProjectRole
from app.commons.settings.config import FilePath
from app.core.git import Git
from app.commons.utils.aes_utils import AesUtils
from app.commons.utils.context_utils import REQUEST_CONTEXT
from app.constants.enums import PullTypeEnum
from app.commons.exceptions.global_exception import BusinessException
from app.core.get_project_path import ProjectPath
from app.core.api_doc_parse import ApiDocParse
from app.commons.utils.cmd_utils import CmdUtils



def insert_project_logic(body: AddProject):
    # todo: git_project不能与后端服务的所有目录名重名
    user = REQUEST_CONTEXT.get().user
    ProjectDao.insert_project(body, user)


def update_project_logic(body: EditProject):
    user = REQUEST_CONTEXT.get().user
    ProjectDao.update_project(body, user)


def delete_project_logic(id: int):
    user = REQUEST_CONTEXT.get().user
    project = ProjectDao.delete_project(id, user)
    import os
    project_path = os.path.join(FilePath.BASE_DIR, project.git_project)
    if os.path.isdir(project_path):
        CmdUtils.cmd(f"rm -rf {project_path}\n")


def get_project_lists_logic(page: int=1, limit: int=10, search=None):
    user = REQUEST_CONTEXT.get().user
    total, project_infos= ProjectDao.list_project(user, page, limit, search)
    project_lists = dict(total=total, lists=project_infos)
    return project_lists



def insert_project_role_logic(data: AddProjectRole):
    user = REQUEST_CONTEXT.get().user
    ProjectRoleDao.insert_project_role(data, user)



def update_project_role_logic(data: EditProjectRole):
    user = REQUEST_CONTEXT.get().user
    ProjectRoleDao.update_project_role(data, user)



def delete_project_role_logic(id: int):
    user = REQUEST_CONTEXT.get().user
    ProjectRoleDao.delete_project_role(id, user)


def project_role_list_logic(project_id: int, page: int=1, limit: int=10, search=None):
    user = REQUEST_CONTEXT.get().user
    roles, count = ProjectRoleDao.project_role_list(user, project_id, page, limit, search)
    project_role_list = dict(count=count, lists=roles)
    return project_role_list


def read_project_logic(id: int):
    user = REQUEST_CONTEXT.get().user
    ProjectRoleDao.read_permission(id, user)


def operation_project_logic(id: int):
    user = REQUEST_CONTEXT.get().user
    ProjectRoleDao.operation_permission(id, user)



def init_project_logic(id: int):
    user = REQUEST_CONTEXT.get().user
    project = ProjectDao.project_detail(id, user)
    project_path = os.path.join(FilePath.BASE_DIR, project.git_project)
    if os.path.isdir(project_path):
        raise BusinessException("项目已存在, 请执行刷新项目！")
    init_project(project)


def init_project(project: DataFactoryProject):
    # 拉取项目
    if project.pull_type == PullTypeEnum.http.value:
        Git.git_clone_http(project.git_branch, project.git_url, project.git_account,
                           AesUtils.decrypt(project.git_password))
    else:
        Git.git_clone_ssh(project.git_branch, project.git_url)


def project_detail_logic(id: int):
    user = REQUEST_CONTEXT.get().user
    rsa_pub_key = None
    project = ProjectDao.project_detail(id, user)
    if project.pull_type == PullTypeEnum.ssh.value:
        from app.commons.settings.config import FilePath
        with open(FilePath.RSA_PUB_KEY, 'r', encoding='utf-8') as f:
            rsa_pub_key = f.read()
    setattr(project, 'rsa_pub_key', rsa_pub_key)
    return project

def start_init_project_logic():
    projects = ProjectDao.get_with_params()
    workers = len(projects)
    if workers > 0:
        with ThreadPoolExecutor(max_workers=workers) as ts:
            all_task = []
            for project in projects:
                all_task.append(ts.submit(init_project, project))
            wait(all_task, return_when=ALL_COMPLETED)


# todo git webhook同步项目
def sync_project_logic(id: int):
    from app.crud.case.CaseDao import CaseDao
    # 记录是谁同步脚本，顺便判断一下权限
    user = REQUEST_CONTEXT.get().user
    project = ProjectDao.project_detail(id, user)

    # step1 git pull 更新项目
    project_path, script_path = ProjectPath.get(project.git_project, project.directory)
    Git.git_pull(project_path, project.git_branch)
    api_doc = ApiDocParse(project_path, script_path)

    # step2 执行api_doc命令, 生成api_data.json
    api_doc.exec()

    # step3 解析apidoc数据入库，暂时先返回api_data.json数据
    api_data = api_doc.parse_apidoc()

    # step4 获取该项目的所有造数场景
    from fastapi.encoders import jsonable_encoder
    project_cases = CaseDao.get_projet_case(project.id)
    project_cases = jsonable_encoder(project_cases)

    # step5 处理同步数据
    msg_dict = api_doc.sync_data(project.id, api_data, project_cases, user)

    # step6 处理同步消息
    msg = api_doc.sync_msg(**msg_dict)
    return msg

def sync_project_list_logic():
    user = REQUEST_CONTEXT.get().user
    project = ProjectDao.get_user_all_projects(user)
    return project