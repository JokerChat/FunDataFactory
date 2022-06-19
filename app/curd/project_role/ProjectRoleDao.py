# -*- coding: utf-8 -*- 
# @Time : 2022/6/18 22:37 
# @Author : junjie
# @File : ProjectRoleDao.py

from app.models import Session
from app.models.project_role import DataFactoryProjectRole
from app.models.user import DataFactoryUser
from app.routers.project.project_role_schema import AddProjectRole, EditProjectRole
from app.utils.logger import Log
from app.utils.exception_utils import record_log, NormalException
from app.utils.db_utils import DbUtils
from sqlalchemy import desc, or_


class ProjectRoleDao(object):

    log = Log("ProjectRoleDao")

    @classmethod
    @record_log
    def insert_project_role(cls, form: AddProjectRole, user: dict) ->None:
        """
        新增用户项目权限
        :param form: 新增模型
        :param user: 用户数据
        :return:
        """
        with Session() as session:
            user_query = session.query(DataFactoryUser).filter(DataFactoryUser.id == form.user_id).first()
            if user_query is None:
                raise Exception("用户不存在！！！")
            if user_query.is_valid:
                raise NormalException("对不起, 该账号已被冻结, 无法添加项目权限")
            user_role_query = session.query(DataFactoryProjectRole).filter(DataFactoryProjectRole.user_id == form.user_id, DataFactoryProjectRole.project_id == form.project_id, DataFactoryProjectRole.del_flag == 0).first()
            if user_role_query is not None:
                raise NormalException("该用户项目权限已存在！！！")
            project_role = DataFactoryProjectRole(form, user)
            session.add(project_role)
            session.commit()



    @classmethod
    @record_log
    def update_project_role(cls, form: EditProjectRole, user: dict) -> None:
        """
        更新用户项目权限
        :param form: 编辑模型
        :param user: 用户数据
        :return:
        """
        with Session() as session:
            session.expire_on_commit = False
            user_role_query = session.query(DataFactoryProjectRole).filter(DataFactoryProjectRole.id == form.id,
                                                                           DataFactoryProjectRole.del_flag == 0).first()
            if user_role_query is None:
                raise NormalException("用户角色不存在！！！")
            DbUtils.update_model(user_role_query, form.dict(), user)
            session.commit()

    @classmethod
    @record_log
    def delete_project_role(cls, id: int, user: dict) -> None:
        """
        删除项目权限
        :param id: 主键id
        :param user: 用户数据
        :return:
        """
        with Session() as session:
            user_role_query = session.query(DataFactoryProjectRole).filter(DataFactoryProjectRole.id == id,
                                                                           DataFactoryProjectRole.del_flag == 0).first()
            if user_role_query is None:
                raise NormalException("用户角色不存在！！！")
            DbUtils.delete_model(user_role_query, user)
            session.commit()

    @classmethod
    @record_log
    def project_role_list(cls, project_id: int, page = 1, limit = 10, search=None):
        """
        获取项目权限成员列表
        :param project_id: 项目id
        :param page: 页码
        :param limit: 大小
        :param search: 搜索内容
        :return:
        """
        with Session() as session:
            filter_list = [DataFactoryProjectRole.del_flag == 0, DataFactoryProjectRole.project_id == project_id]
            if search:
                filter_list.append(or_(DataFactoryUser.username.like(f"%{search}%"), DataFactoryUser.email.like(f"%{search}%")))
            roles = session.query(DataFactoryUser.name, DataFactoryUser.username, DataFactoryUser.email, DataFactoryProjectRole.user_id,
                                  DataFactoryProjectRole.project_role, DataFactoryProjectRole.project_id, DataFactoryProjectRole.id, DataFactoryProjectRole.create_name,
                                  DataFactoryProjectRole.create_time).\
                outerjoin(DataFactoryProjectRole, DataFactoryProjectRole.user_id == DataFactoryUser.id)
            roles = roles.filter(*filter_list)
            role_infos = roles.order_by(desc(DataFactoryProjectRole.create_time)).limit(limit).offset((page - 1) * limit).all()
            count = roles.count()
            return role_infos, count