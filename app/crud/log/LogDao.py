# -*- coding: utf-8 -*- 
# @Time : 2022/9/13 21:27 
# @Author : junjie
# @File : LogDao.py

from sqlalchemy import or_, desc
from app.models.run_log import DataFactoryRunLog
from app.models.cases import DataFactoryCases
from app.models.project import DataFactoryProject
from app.crud.case.CaseDao import CaseDao
from app.constants.enums import RunStatusEnum, CallTypeEnum
from app.models import Session
from app.crud import BaseCrud
from loguru import logger
from typing import Union


class LogDao(BaseCrud):

    log = logger
    model = DataFactoryRunLog

    @classmethod
    def add(cls, cases_id: int, requests_id: str, project_id: int, run_param_in: str,
            run_param_out: Union[str, None], run_status: int, call_type: int, run_log: str, user: dict):
        """新增日志"""
        log = DataFactoryRunLog(cases_id, requests_id, project_id, run_param_in,
                                    run_param_out, run_status, call_type, run_log, user)
        cls.insert_by_model(model_obj = log)


    @classmethod
    def get_all_logs(cls, user: dict, page: int = 1, limit: int = 20, group: str=None, project: str=None,
                     requests_id: str=None, call_type: str=None, run_status: str=None, search: str=None):
        """获取所有的日志"""
        with Session() as session:
            filter_list = [DataFactoryRunLog.del_flag == 0]
            # 查询用户有效的项目id
            project_ids = CaseDao.project_ids(user)
            filter_list.extend(project_ids)
            if search:
                search_str = f"%{search}%"
                filter_list.append(or_(DataFactoryCases.name.like(search_str),
                                       DataFactoryCases.title.like(search_str),
                                       DataFactoryRunLog.run_log.like(search_str),
                                       ))
            if call_type: filter_list.append(DataFactoryRunLog.call_type == call_type)
            if run_status: filter_list.append(DataFactoryRunLog.run_status == run_status)
            if requests_id: filter_list.append(DataFactoryRunLog.requests_id == requests_id)
            if group: filter_list.append(DataFactoryCases.group_name == group)
            if project: filter_list.append(DataFactoryProject.project_name == project)
            log = session.query(DataFactoryRunLog.requests_id, DataFactoryRunLog.run_param_in, DataFactoryRunLog.run_param_out,
                                DataFactoryRunLog.call_type, DataFactoryRunLog.run_status, DataFactoryRunLog.run_log,
                                DataFactoryCases.title, DataFactoryCases.name, DataFactoryCases.group_name,
                                DataFactoryCases.path, DataFactoryProject.project_name, DataFactoryProject.directory,
                                DataFactoryRunLog.create_name, DataFactoryRunLog.create_time, DataFactoryRunLog.create_id). \
                outerjoin(DataFactoryCases,
                          DataFactoryRunLog.cases_id == DataFactoryCases.id).\
                outerjoin(DataFactoryProject,
                          DataFactoryRunLog.project_id == DataFactoryProject.id)
            log = log.filter(*filter_list)
            log_infos = log.order_by(desc(DataFactoryRunLog.id)).limit(limit).offset((page - 1) * limit).all()
            count = log.count()
        return log_infos, count