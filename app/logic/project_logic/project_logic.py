# -*- coding: utf-8 -*- 
# @Time : 2022/8/7 23:34 
# @Author : junjie
# @File : project_logic.py


import os
from concurrent.futures import ThreadPoolExecutor, ALL_COMPLETED, wait
from app.crud.project.ProjectDao import ProjectDao, DataFactoryProject
from app.crud.project_role.ProjectRoleDao import ProjectRoleDao
from app.routers.project.request_model.project_in import AddProject, EditProject, AddProjectRole, EditProjectRole, GitProject
from app.commons.settings.config import FilePath
from app.core.git import Git
from app.commons.utils.encrypt_utils import AesUtils, Sha256
from app.commons.utils.context_utils import REQUEST_CONTEXT
from app.constants.enums import PullTypeEnum, SysEnum
from app.commons.exceptions.global_exception import BusinessException
from app.core.get_project_path import ProjectPath
from app.core.api_doc_parse import ApiDocParse
from app.commons.utils.cmd_utils import CmdUtils
from starlette.requests import Request
from app.constants import constants



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

def check_gitee(request: Request):
    # 这个验签可以用中间件做，但是溜达哥说中间件太耗性能了，最好用依赖注入的形式，溜达哥yyds
    # 中间件很耗性能的-->fastapi 原作者，starlette的锅...
    headers = request.headers
    user_agent = headers.get('user-agent')
    if user_agent and user_agent == constants.USER_AGENT:
        gitee_timestamp = headers.get('x-gitee-timestamp')
        gitee_token = headers.get('x-gitee-token')
        if gitee_timestamp and gitee_token and Sha256.encrypt(str(gitee_timestamp)) == gitee_token:
            return True
        else:
            raise BusinessException("验签有误！！！")
    else:
        raise BusinessException("验签有误！！！")


def sync_project_logic(type: str, user: dict, id: int = None, project_name: str = None):
    from app.crud.case.CaseDao import CaseDao
    if type == SysEnum.platform.value:
        # 记录是谁同步脚本，顺便判断一下权限
        project = ProjectDao.project_detail(id, user)
    elif type == SysEnum.git.value:
        project = ProjectDao.project_detail_by_git(project_name)
    else:
        raise BusinessException('同步失败, 不支持该类型')
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

def sync_project_logic_by_platform(id: int):
    user = REQUEST_CONTEXT.get().user
    msg = sync_project_logic(type = SysEnum.platform.value, user = user, id = id)
    return msg

def sync_project_logic_by_git(data: GitProject):
    # 如果是公司的gitlab平台，可以去除这段代码...
    request_ = REQUEST_CONTEXT.get()
    ant = check_gitee(request_)
    if not ant:
        raise BusinessException("验签有误！！！")
    msg = sync_project_logic(type = SysEnum.git.value, project_name=data.project.name, user=constants.ADMIN)
    return msg

def sync_project_list_logic():
    user = REQUEST_CONTEXT.get().user
    project = ProjectDao.get_user_all_projects(user)
    return project