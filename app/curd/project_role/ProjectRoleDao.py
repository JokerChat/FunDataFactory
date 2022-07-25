# -*- coding: utf-8 -*- 
# @Time : 2022/6/18 22:37 
# @Author : junjie
# @File : ProjectRoleDao.py

from app.models import Session
from app.models.project_role import DataFactoryProjectRole
from app.models.project import DataFactoryProject
from app.models.user import DataFactoryUser
from app.routers.project.project_role_schema import AddProjectRole, EditProjectRole
from app.commons.utils.logger import Log
from app.commons.exceptions.global_exception import BusinessException
from app.commons.utils.db_utils import DbUtils
from sqlalchemy import desc, or_
from config import Permission


class ProjectRoleDao(object):

    log = Log("ProjectRoleDao")

    @classmethod
    def insert_project_role(cls, form: AddProjectRole, user: dict) ->None:
        """
        新增用户项目权限
        :param form: 新增模型
        :param user: 用户数据
        :return:
        """
        with Session() as session:
            cls.operation_permission(form.project_id, user)
            user_query = session.query(DataFactoryUser).filter(DataFactoryUser.id == form.user_id).first()
            if user_query is None:
                raise Exception("用户不存在！！！")
            if user_query.is_valid:
                raise BusinessException("对不起, 该账号已被冻结, 无法添加项目权限")
            user_role_query = session.query(DataFactoryProjectRole).filter(DataFactoryProjectRole.user_id == form.user_id, DataFactoryProjectRole.project_id == form.project_id, DataFactoryProjectRole.del_flag == 0).first()
            if user_role_query is not None:
                raise BusinessException("该用户项目权限已存在！！！")
            project_role = DataFactoryProjectRole(form, user)
            session.add(project_role)
            session.commit()



    @classmethod
    def update_project_role(cls, form: EditProjectRole, user: dict) -> None:
        """
        更新用户项目权限
        :param form: 编辑模型
        :param user: 用户数据
        :return:
        """
        with Session() as session:
            user_role_query = session.query(DataFactoryProjectRole).filter(DataFactoryProjectRole.id == form.id,
                                                                           DataFactoryProjectRole.del_flag == 0).first()
            if user_role_query is None:
                raise BusinessException("用户角色不存在！！！")
            cls.operation_permission(user_role_query.project_id, user)
            DbUtils.update_model(user_role_query, form.dict(), user)
            session.commit()

    @classmethod
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
                raise BusinessException("用户角色不存在！！！")
            cls.operation_permission(user_role_query.project_id, user)
            DbUtils.delete_model(user_role_query, user)
            session.commit()

    @classmethod
    def project_role_list(cls, uesr:dict, project_id: int, page = 1, limit = 10, search=None):
        """
        获取项目权限成员列表
        :param uesr: 用户数据
        :param project_id: 项目id
        :param page: 页码
        :param limit: 大小
        :param search: 搜索内容
        :return:
        """
        with Session() as session:
            cls.operation_permission(project_id, uesr)
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

    @classmethod
    def project_by_user(cls, user):
        """
        根据用户获取权限范围内项目
        :param user: 用户数据
        :return:
        """
        with Session() as session:
            projects = session.query(DataFactoryProjectRole.project_id).filter(DataFactoryProjectRole.user_id == user['id'],
                                                               DataFactoryProjectRole.del_flag == 0).all()
            return  [i[0] for i in projects]


    @classmethod
    def read_permission(cls, project_id: int, user: dict) -> None:
        """判断是否有项目查看权限"""
        if user['role'] == Permission.ADMIN:
            # 超管不限制
            return
        with Session() as session:
            project = session.query(DataFactoryProject).filter(DataFactoryProject.id == project_id,
                                                               DataFactoryProject.del_flag == 0).first()
            if project is None: raise BusinessException("项目不存在")
            if project.owner == user['username']:
                # 项目负责人可以查看
                return
            else:
                # 查询是否在项目配有权限
                project_role = session.query(DataFactoryProjectRole).filter(DataFactoryProjectRole.user_id == user['id'],
                                                             DataFactoryProjectRole.project_id == project_id,
                                                             DataFactoryProjectRole.del_flag == 0).first()
                if project_role is None:
                    raise BusinessException(f"对不起，你没有{project.project_name}项目权限！！！")


    @classmethod
    def operation_permission(cls, project_id, user):
        """判断是否有项目操作权限"""
        with Session() as session:
            project = session.query(DataFactoryProject).filter(DataFactoryProject.id == project_id,
                                                               DataFactoryProject.del_flag == 0).first()
            if project is None: raise BusinessException("项目不存在")
            if user['role'] == Permission.ADMIN or project.owner == user['username']:
                # 超管 或者 项目负责人可以操作
                return
            else:
                # 非超管 或者 非项目负责人
                role_query = session.query(DataFactoryProjectRole).filter(DataFactoryProjectRole.user_id == user['id'],
                                                             DataFactoryProjectRole.project_id == project_id, DataFactoryProjectRole.del_flag ==0 ).first()

                if role_query is None or role_query.project_role == Permission.MEMBERS:
                    # 查询为空 或者 项目权限为组员
                    raise BusinessException(f"对不起，你没有{project.project_name}项目操作权限！！！")
                else:
                    # 组长可以操作
                    return