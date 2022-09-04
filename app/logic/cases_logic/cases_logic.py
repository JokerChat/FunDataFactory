# -*- coding: utf-8 -*- 
# @Time : 2022/8/24 21:40 
# @Author : junjie
# @File : cases_logic.py

from app.commons.utils.context_utils import REQUEST_CONTEXT
from app.crud.case.CaseDao import CaseDao, CaseParamsDao
from app.crud.operation.OperationDao import LikeOperationDao, CollectionOperationDao
from app.routers.cases.request_model.cases_in import AddCasesParams, EditCasesParmas

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