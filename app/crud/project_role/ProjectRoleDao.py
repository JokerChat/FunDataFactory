# -*- coding: utf-8 -*- 
# @Time : 2022/6/18 22:37 
# @Author : junjie
# @File : ProjectRoleDao.py

from app.models import Session
from app.models.project_role import DataFactoryProjectRole
from app.models.project import DataFactoryProject
from app.models.user import DataFactoryUser
from app.routers.project.request_model.project_in import AddProjectRole, EditProjectRole
from app.commons.exceptions.global_exception import BusinessException
from sqlalchemy import desc, or_
from app.constants.enums import PermissionEnum
from app.crud import BaseCrud

class ProjectRoleDao(BaseCrud):

    model = DataFactoryProjectRole

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
                raise BusinessException("用户不存在！！！")
            if user_query.is_valid:
                raise BusinessException("对不起, 该账号已被冻结, 无法添加项目权限")
            ant = cls.get_with_existed(session, user_id = form.user_id, project_id = form.project_id)
            if ant:
                raise BusinessException("该用户项目权限已存在！！！")
            project_role = DataFactoryProjectRole(form, user)
            cls.insert_by_model(session, model_obj = project_role)



    @classmethod
    def update_project_role(cls, form: EditProjectRole, user: dict) -> None:
        """
        更新用户项目权限
        :param form: 编辑模型
        :param user: 用户数据
        :return:
        """
        user_role_query = cls.get_with_id(id = form.id)
        if user_role_query is None:
            raise BusinessException("用户角色不存在！！！")
        cls.operation_permission(user_role_query.project_id, user)
        cls.update_by_id(model = form, user = user)

    @classmethod
    def delete_project_role(cls, id: int, user: dict) -> None:
        """
        删除项目权限
        :param id: 主键id
        :param user: 用户数据
        :return:
        """
        user_role_query = cls.get_with_id(id = id)
        if user_role_query is None:
            raise BusinessException("用户角色不存在！！！")
        cls.operation_permission(user_role_query.project_id, user)
        cls.delete_by_id(id = id)

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
        projects = cls.get_with_params(user_id = user['id'])
        return [project.project_id for project in projects]


    @classmethod
    def read_permission(cls, project_id: int, user: dict) -> None:
        """判断是否有项目查看权限"""
        if user['role'] == PermissionEnum.admin.value:
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
                project_role = cls.get_with_first(session, user_id = user['id'], project_id = project_id)
                if project_role is None:
                    raise BusinessException(f"对不起，你没有{project.project_name}项目查看权限！！！")


    @classmethod
    def operation_permission(cls, project_id, user):
        """判断是否有项目操作权限"""
        with Session() as session:
            project = session.query(DataFactoryProject).filter(DataFactoryProject.id == project_id,
                                                               DataFactoryProject.del_flag == 0).first()
            if project is None: raise BusinessException("项目不存在")
            if user['role'] == PermissionEnum.admin.value or project.owner == user['username']:
                # 超管 或者 项目负责人可以操作
                return
            else:
                # 非超管 或者 非项目负责人
                role_query = cls.get_with_first(session, user_id = user['id'], project_id = project_id)

                if role_query is None or role_query.project_role == PermissionEnum.members.value:
                    # 查询为空 或者 项目权限为组员
                    raise BusinessException(f"对不起，你没有{project.project_name}项目操作权限！！！")
                else:
                    # 组长可以操作
                    return