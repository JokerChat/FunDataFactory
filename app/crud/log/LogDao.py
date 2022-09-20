# -*- coding: utf-8 -*- 
# @Time : 2022/9/13 21:27 
# @Author : junjie
# @File : LogDao.py

from sqlalchemy import or_, desc, case, func, asc
from app.models.run_log import DataFactoryRunLog
from app.models.cases import DataFactoryCases
from app.models.project import DataFactoryProject
from app.crud.case.CaseDao import CaseDao
from app.constants.enums import RunStatusEnum
from app.models import Session
from app.crud import BaseCrud
from loguru import logger
from typing import Union
from datetime import datetime


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

    @classmethod
    def log_summary(cls):
        """统计调用数量"""
        log_sum = cls.get_with_count()
        return log_sum

    @classmethod
    def success_summary(cls):
        """统计成功调用数量"""
        success_sum = cls.get_with_count( run_status = RunStatusEnum.success.value)
        return success_sum

    @classmethod
    def run_status_summary(cls):
        """统计各运行状态数量"""
        with Session() as session:
            run_type = case(whens=[(DataFactoryRunLog.run_status == 0, '成功'), (DataFactoryRunLog.run_status == 1, '异常')], else_='失败').label("name")
            run_status_sum = session.query(run_type, func.count(DataFactoryRunLog.run_status).label("value")).group_by(DataFactoryRunLog.run_status)
            return run_status_sum.all()

    @classmethod
    def call_type_summary(cls):
        """统计各调用方式数量"""
        with Session() as session:
            type = case(whens=[(DataFactoryRunLog.call_type == '0', '平台调用'),(DataFactoryRunLog.call_type == '1', '外链调用')], else_='RPC调用').label("name")
            call_type_sum = session.query(type,
                                           func.count(DataFactoryRunLog.call_type).label("value")).group_by(
                DataFactoryRunLog.call_type)
            return call_type_sum.all()

    @classmethod
    def collect_weekly_data(cls, start_time: datetime, end_time: datetime):
        """统计最近7天的数据"""
        with Session() as session:
            # 成功数
            success_count =case(whens=[(DataFactoryRunLog.run_status == RunStatusEnum.success.value, 1)], else_=0)
            # 异常数
            exception_count =case(whens=[(DataFactoryRunLog.run_status == RunStatusEnum.exception.value, 1)], else_=0)
            # 失败数
            error_count =case(whens=[(DataFactoryRunLog.run_status == RunStatusEnum.fail.value, 1)], else_=0)

            filter_list = [DataFactoryRunLog.create_time.between(start_time.strftime("%Y-%m-%d 00:00:00"), end_time.strftime("%Y-%m-%d 23:59:59"))]
            date = func.date_format(DataFactoryRunLog.create_time, "%Y-%m-%d")
            import decimal
            weekly_data = session.query(date.label("date"), func.count(DataFactoryRunLog.id).label("count"),
                                        func.sum(success_count), func.sum(exception_count), func.sum(error_count))\
                .filter(*filter_list).\
                group_by(date).order_by(asc(date))
            call_data = {i[0]:dict(count= i[1], success_count = int(decimal.Decimal(i[2])),
                                   exception_count = int(decimal.Decimal(i[3])),
                                   error_count= int(decimal.Decimal(i[4]))) for i in weekly_data.all()}
            case_data = CaseDao.collect_weekly_data(start_time, end_time)
            return LogDao.fill_data(start_time, end_time, call_data, case_data)

    @classmethod
    def fill_data(cls, start_time: datetime, end_time: datetime, call_data: dict, case_data: dict):
        """补充数据"""
        from datetime import timedelta
        start = start_time
        weekly_data = []
        while start <= end_time:
            date = start.strftime("%Y-%m-%d")
            weekly_data.append(dict(date=date, call_count=call_data.get(date).get('count') if date in call_data else 0,
                                    success_count=call_data.get(date).get('success_count') if date in call_data else 0,
                                    exception_count=call_data.get(date).get('exception_count') if date in call_data else 0,
                                    error_count=call_data.get(date).get('error_count') if date in call_data else 0,
                                    case_count=case_data.get(date, 0)))
            start += timedelta(days=1)
        return weekly_data