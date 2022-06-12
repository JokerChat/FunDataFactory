# -*- coding: utf-8 -*- 
# @Time : 2022/6/12 22:06 
# @Author : junjie
# @File : ProjectDao.py

from sqlalchemy import or_
from app.models import Session
from app.models.project import DataFactoryProject
from app.models.user import DataFactoryUser
from app.routers.project.project_schema import AddProject
from app.utils.logger import Log
from app.utils.exception_utils import record_log
from app.utils.exception_utils import NormalException


class ProjectDao(object):

    log = Log("ProjectDao")

    @classmethod
    @record_log
    def insert_project(cls, form: AddProject, user: dict) -> DataFactoryProject:
        with Session() as session:
            session.expire_on_commit = False
            user_query = session.query(DataFactoryUser.username).filter( DataFactoryUser.username == form.owner).first()
            if user_query is None:
                raise NormalException("用户不存在！！！")
            project = session.query(DataFactoryProject).filter( or_(DataFactoryProject.project_name == form.project_name, DataFactoryProject.git_project == form.git_project),
                                                   DataFactoryProject.del_flag==0).first()
            if project:
                raise NormalException("项目名或者git项目名重复, 请重新录入！！！")
            projects = DataFactoryProject(form, user)
            session.add(projects)
            session.commit()
            session.expunge(projects)
            return projects