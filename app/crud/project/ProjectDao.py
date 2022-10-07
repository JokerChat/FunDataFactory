# -*- coding: utf-8 -*- 
# @Time : 2022/6/12 22:06 
# @Author : junjie
# @File : ProjectDao.py

from sqlalchemy import or_
from app.models import Session
from app.models.project import DataFactoryProject
from app.models.user import DataFactoryUser
from app.routers.project.request_model.project_in import AddProject, EditProject
from app.routers.project.response_model.project_out import ProjectListDto, ProjectSyncDto
from app.commons.exceptions.global_exception import BusinessException
from app.crud.project_role.ProjectRoleDao import ProjectRoleDao
from app.constants.enums import PermissionEnum
from app.crud import BaseCrud




class ProjectDao(BaseCrud):

    model = DataFactoryProject

    @classmethod
    def insert_project(cls, form: AddProject, user: dict) -> None:
        """
        新增项目
        :param form: 新增项目模型
        :param user: 用户数据
        :return:
        """
        with Session() as session:
            user_query = session.query(DataFactoryUser).filter( DataFactoryUser.username == form.owner).first()
            if user_query is None:
                raise BusinessException("用户不存在！！！")
            filter_list = [or_(DataFactoryProject.project_name == form.project_name,
                               DataFactoryProject.git_project == form.git_project)]
            project = cls.get_with_existed(session, filter_list=filter_list)
            if project:
                raise BusinessException("项目名或者git项目名重复, 请重新录入！！！")
            _project = DataFactoryProject(form, user)
            cls.insert_by_model(session, model_obj=_project)

    @classmethod
    def update_project(cls, data: EditProject, user: dict) -> None:
        """
        编辑项目
        :param data: 编辑项目模型
        :param user: 用户数据
        :return:
        """
        ProjectRoleDao.operation_permission(data.id, user)
        ant = cls.get_with_existed(id = data.id)
        if not ant:
            raise BusinessException("项目不存在")
        # 根据名称查出数据
        project_name = cls.get_with_first(project_name = data.project_name)
        # 如果有数据且主键id与请求参数id不相等
        if project_name is not None and project_name.id != data.id:
            raise BusinessException("项目名重复, 请重新录入！！！")
        git_project_name = cls.get_with_first(git_project = data.git_project)
        if git_project_name is not None and git_project_name.id != data.id:
            raise BusinessException("git项目名重复, 请重新录入！！！")
        cls.update_by_id(model = data, user = user)

    @classmethod
    def delete_project(cls, id: int, user: dict) -> DataFactoryProject:
        """
        删除项目
        :param id: 项目id
        :param user: 用户数据
        :return:
        """
        ProjectRoleDao.operation_permission(id, user)
        with Session() as session:
            from app.crud.case.CaseDao import CaseDao, CaseParamsDao
            project = cls.delete_by_id(session, id = id, user = user)
            cases_id_list = CaseDao.delete_project_case(session, project.id, user)
            CaseParamsDao.delete_all_params(session, cases_id_list, user)
            return project

    @classmethod
    def list_project(cls, user: dict, page: int=1, limit: int=10, search: str=None) ->(int, DataFactoryProject):
        """
        获取项目列表
        :param user: 用户数据
        :param page: 页码
        :param limit: 大小
        :param search: 搜索内容
        :return:
        """
        filter_list = [ *cls.user_all_projects(user)]
        total, project_infos = cls.get_with_pagination(page = page,
                                                       limit = limit,
                                                       filter_list = filter_list,
                                                       _fields = ProjectListDto,
                                                       project_name = f"%{search}%" if search else None)
        return total, project_infos

    @classmethod
    def user_all_projects(cls, user: dict):
        """
        权限范围内条件
        :param user: 用户数据
        :return:
        """
        filter_list = []
        # 如果不是管理员角色
        if user['role'] != PermissionEnum.admin.value:
            # 找出用户权限范围内的所有项目
            project_ids = ProjectRoleDao.project_by_user(user)
            # 公开的项目 或者 权限范围内的项目 或者 项目负责人的项目
            filter_list.append(or_(DataFactoryProject.id.in_(project_ids), DataFactoryProject.owner == user['username'],
                                   DataFactoryProject.private == False))
        return filter_list

    @classmethod
    def get_user_all_projects(cls, user: dict):
        """
        获取用户权限范围内的所有项目
        :param user: 用户数据
        :return:
        """
        project_data = cls.get_with_params(filter_list = [ *cls.user_all_projects(user) ],
                                           _fields = ProjectSyncDto)
        return project_data

    @classmethod
    def project_detail(cls, id: int, user: dict) -> DataFactoryProject:
        """获取项目详情"""
        ProjectRoleDao.read_permission(id, user)
        project = cls.get_with_id(id = id)
        if project is None:
            raise BusinessException("项目不存在")
        return project

    @classmethod
    def project_detail_by_git(cls, name: str):
        """获取项目详情"""
        project = cls.get_with_first(git_project = name)
        if project is None:
            raise BusinessException("项目不存在")
        return project

    @classmethod
    def project_summary(cls):
        """统计项目数量"""
        project_sum = cls.get_with_count()
        return project_sum