# -*- coding: utf-8 -*- 
# @Time : 2022/8/24 21:40 
# @Author : junjie
# @File : cases_logic.py

import time, json
from app.commons.utils.context_utils import REQUEST_CONTEXT
from app.crud.case.CaseDao import CaseDao, CaseParamsDao
from app.crud.project_role.ProjectRoleDao import ProjectRoleDao
from app.crud.log.LogDao import LogDao
from app.crud.operation.OperationDao import LikeOperationDao, CollectionOperationDao
from app.routers.cases.request_model.cases_in import AddCasesParams, EditCasesParmas, RunBody
from app.core.run_script import RunScript
from app.constants.enums import RunStatusEnum, CallTypeEnum
from app.constants import constants
from datetime import datetime
from app.commons.exceptions.global_exception import BusinessException

def like_logic(id : int):
    user = REQUEST_CONTEXT.get().user
    result = LikeOperationDao.like(id, user)
    return result

def collection_logic(id : int):
    user = REQUEST_CONTEXT.get().user
    result = CollectionOperationDao.collection(id, user)
    return result

def get_user_groups_logic():
    user = REQUEST_CONTEXT.get().user
    groups = CaseDao.get_user_group_name(user)
    group_list = [i[0] for i in groups]
    return group_list

def search_case_logic(keyword: str):
    user = REQUEST_CONTEXT.get().user
    cases = CaseDao.get_search_case(user, keyword)
    return cases

def case_list_logic(page: int=1, limit: int=10, show: str = None,
                    project_id: int=None, case_id: int=None):
    user = REQUEST_CONTEXT.get().user
    cases, total = CaseDao.get_all_cases(user, page, limit, show, project_id, case_id)
    cases_lists = dict(total=total, lists=cases)
    return cases_lists

def case_detail_logic(id: int):
    user = REQUEST_CONTEXT.get().user
    case = CaseDao.case_detail_by_id(id, user)
    return case

def add_params_logic(body: AddCasesParams):
    import uuid
    user = REQUEST_CONTEXT.get().user
    CaseParamsDao.insert_cases_params(body, out_id = uuid.uuid4().hex, user = user)

def edit_params_logic(body: EditCasesParmas):
    user = REQUEST_CONTEXT.get().user
    CaseParamsDao.update_cases_params(body, user = user)

def delete_params_logic(id: int):
    user = REQUEST_CONTEXT.get().user
    CaseParamsDao.deleta_cases_params(id, user)

def get_cases_params_logic(cases_id: int, page: int, limit: int):
    total, params_infos = CaseParamsDao.get_cases_params(cases_id, page, limit)
    params_list = dict(total=total, lists=params_infos)
    return params_list

def run_logic(body: RunBody, call_type: CallTypeEnum, user: dict):
    start_time = time.perf_counter()
    run_log = None
    try:
        run_data = RunScript.run(body.path, body.method, body.params, body.project, body.directory)
        if isinstance(run_data, tuple) and len(run_data) == 2:
            # 默认第一个是脚本返参,第二个为脚本日志
            run_data, run_log = run_data
        elif isinstance(run_data, dict):
            pass
        else:
            raise BusinessException("脚本返参数有误！！！")
        run_status = RunStatusEnum.success.value  if run_data.get('responseCode') == 0 \
                                                     or run_data.get('code') == 200 \
                                                     or run_data.get('code') == 0 \
            else RunStatusEnum.exception.value
        end_time = time.perf_counter()
        cost = "%.2fs" % (end_time - start_time)
        LogDao.add(body.cases_id, body.requests_id, body.project_id, json.dumps(body.params, ensure_ascii=False), json.dumps(run_data, ensure_ascii=False),
                   run_status=run_status, call_type=call_type, run_log=run_log, user=user)
        return dict(actual_request=body.params, actual_response=run_data, result = run_status, requests_id = body.requests_id, cost = cost, log = run_log)
    except:
        import traceback
        run_status = RunStatusEnum.fail.value
        run_log = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: 脚本执行失败 -> 脚本目录：{body.project}/{body.directory}/{body.path}.py，执行{body.method}函数失败，kwargs：{body.params}，报错信息：\n{str(traceback.format_exc())}"
        LogDao.add(body.cases_id, body.requests_id, body.project_id, json.dumps(body.params, ensure_ascii=False), run_param_out=None,
                   run_status=run_status, call_type=call_type, run_log=run_log, user=user)
        end_time = time.perf_counter()
        cost = "%.2fs" % (end_time - start_time)
        return dict(actual_request=body.params, actual_response=None, result=run_status, requests_id=body.requests_id,
                    cost=cost, log=run_log)


def plat_run_logic(body: RunBody):
    user = REQUEST_CONTEXT.get().user
    # 判断用户项目权限
    ProjectRoleDao.read_permission(body.project_id, user)
    return run_logic(body, CallTypeEnum.plat.value, user)

def log_list_logic(page: int=1, limit: int=20, group: str = None, project:str = None,
                   requests_id: str = None, search: str = None, call_type: str = None, run_status: str = None):
    user = REQUEST_CONTEXT.get().user
    logs, total = LogDao.get_all_logs(user, page, limit, group, project, requests_id, call_type, run_status, search)
    logs_lists = dict(total=total, lists=logs)
    return logs_lists

def out_run_logic(id: str):
    import uuid
    case_params = CaseParamsDao.get_params_detail(id)
    case_detail = CaseDao.case_detail_by_id(case_params.cases_id)
    body = RunBody(cases_id = case_params.cases_id, project_id = case_detail.project_id, path = case_detail.path,
                   method = case_detail.name, project = case_detail.git_project, directory = case_detail.directory,
                   params = json.loads(case_params.params), requests_id=uuid.uuid4().hex)
    return run_logic(body, CallTypeEnum.out.value, user=constants.ADMIN)

def rpc_run_logic(method: str, data: dict):
    import uuid
    case_detail = CaseDao.case_detail_by_method(method)
    body = RunBody(**case_detail, params = data, requests_id=uuid.uuid4().hex)
    return run_logic(body, CallTypeEnum.rpc.value, user=constants.ADMIN)