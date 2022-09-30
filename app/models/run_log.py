# -*- coding: utf-8 -*- 
# @Time : 2022/9/13 21:07 
# @Author : junjie
# @File : run_log.py

from sqlalchemy import Column, String, Text, INT, SMALLINT
from app.models.base import FunBaseModel

class DataFactoryRunLog(FunBaseModel):
    """脚本表"""
    __tablename__ = 'data_factory_run_log'

    cases_id = Column(INT, nullable=False, comment="造数场景id")
    requests_id = Column(String(64), nullable=False, comment="请求id")
    project_id =  Column(INT, nullable=False, comment="项目id")
    run_param_in = Column(Text, nullable=False, comment="实际入参")
    run_param_out = Column(Text, nullable=True, comment="实际出参")
    call_type = Column(SMALLINT, default=0, nullable=False, comment="调用方式, 0: 平台调用 1: 外链调用")
    run_status = Column(SMALLINT, default=0, nullable=False, comment="运行状态, 0: 运行成功 1: 运行异常 2: 运行失败")
    run_log = Column(Text, nullable=True, comment="运行日志")

    def __init__(self, cases_id, requests_id, project_id, run_param_in, run_param_out, run_status, call_type, run_log, user, del_flag=0, id=None):
        super().__init__(create_id=user['id'], create_name=user['username'], del_flag=del_flag, id=id)
        self.cases_id = cases_id
        self.requests_id = requests_id
        self.project_id = project_id
        self.run_param_in = run_param_in
        self.run_param_out = run_param_out
        self.run_status = run_status
        self.call_type = call_type
        self.run_log = run_log
