# -*- coding: utf-8 -*- 
# @Time : 2022/9/18 19:07 
# @Author : junjie
# @File : data_logic.py

from app.crud.project.ProjectDao import ProjectDao
from app.crud.case.CaseDao import CaseDao
from app.crud.log.LogDao import LogDao
from app.crud.user.UserDao import UserDao
from datetime import datetime, timedelta




def data_summary_logic():
    # 用户数
    user_num = UserDao.user_summary()
    # 项目数
    project_num = ProjectDao.project_summary()
    # 场景数
    case_num = CaseDao.case_summary()
    # 业务线数
    group_num = CaseDao.get_group_name()
    # 调用量数
    log_num = LogDao.log_summary()

    # 成功率计算
    success_num = LogDao.success_summary()
    success_rate = success_num / log_num if log_num !=0 else 0

    # 各状态分布
    run_type_data = LogDao.run_status_summary()

    # 各调用方式分布
    call_type_data = LogDao.call_type_summary()

    # 统计各业务线分布
    group_case_num = CaseDao.case_group_summary()

    # 最近7天调用量
    today = datetime.today()
    last_7_day = (today - timedelta(days=6))
    weekly_data = LogDao.collect_weekly_data(last_7_day, today)

    return dict(user=user_num, project=project_num, case=case_num,
                 group = len(group_num), log=log_num, success_rate = '{:.2f}%'.format(success_rate*100),
                run_type_data = run_type_data, call_type_data = call_type_data,
                group_data = group_case_num, weekly_data = weekly_data)