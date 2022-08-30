# -*- coding: utf-8 -*-
# @Time : 2022/8/21 20:27
# @Author : junjie
# @File : CasesDao.py

from app.models.cases import DataFactoryCases
from app.models.cases_like import DataFactoryCasesLike
from app.models.cases_collection import DataFactoryCasesCollection
from app.routers.cases.response_model.cases_out import CaseDto, CaseGroupDto, CaseSearchDto
from app.commons.exceptions.global_exception import BusinessException
from app.crud.project.ProjectDao import ProjectDao
from loguru import logger
from app.crud import BaseCrud
from sqlalchemy import or_, asc, and_, func, case as case_, distinct
from sqlalchemy.orm import aliased
from app.models import Session
from app.constants.enums import DeleteEnum, ShowEnum

class CaseDao(BaseCrud):

    log = logger
    model = DataFactoryCases

    @classmethod
    def insert_case(cls, project_id: int , title: str, name: str, description: str, group_name: str, header: str, owner: str, path: str,
                    param_in: str, param_out: str, example_param_in: str, example_param_out: str, user: dict) -> None:
        """
        新增造数场景
        :param project_id: 项目id
        :param title: 标题
        :param name: 方法名
        :param description: 描述信息
        :param group_name: 分组名
        :param header: 请求头
        :param owner: 负责人
        :param path: 路径
        :param param_in: 请求参数
        :param param_out: 返回参数
        :param example_param_in: 请求示例
        :param example_param_out: 返回示例
        :param user: 用户数据
        :return:
        """
        ant = cls.get_with_existed(project_id = project_id, name = name)
        if ant:
            raise BusinessException("造数场景已存在！！！")
        case = DataFactoryCases(project_id, title, name, description, group_name, header, owner, path, param_in,
                                 param_out, example_param_in, example_param_out, user)
        cls.insert_by_model(model_obj = case)

    @classmethod
    def update_case(cls, cases_id: int, title: str, name: str, description: str, group_name: str, header: str, owner: str, path: str,
                    param_in: str, param_out: str, example_param_in: str, example_param_out: str, user: dict) -> None:
        """
        更新造数场景
        :param cases_id: 主键id
        :param title: 标题
        :param name: 方法名
        :param description: 描述信息
        :param group_name: 分组名
        :param header: 请求头
        :param owner: 负责人
        :param path: 路径
        :param param_in: 请求参数
        :param param_out: 返回参数
        :param example_param_in: 请求示例
        :param example_param_out: 返回示例
        :param user: 用户数据
        :return:
        """
        ant = cls.get_with_existed(id=cases_id)
        if not ant:
            raise BusinessException("造数场景不存在！！！")
        update_map = {
            "id": cases_id,
            "title": title,
            "name": name,
            "description": description,
            "group_name": group_name,
            "header": header,
            "owner": owner,
            "path": path,
            "param_in": param_in,
            "param_out": param_out,
            "example_param_in": example_param_in,
            "example_param_out": example_param_out
        }
        cls.update_by_id(model = update_map, user = user)


    @classmethod
    def delete_case(cls, cases_id: int, user: dict) -> None:
        """
        删除造数场景
        :param cases_id: 主键id
        :param user: 用户数据
        :return:
        """
        ant = cls.get_with_existed(id=cases_id)
        if not ant:
            raise BusinessException("造数场景不存在！！！")
        cls.delete_by_id(id = cases_id, user = user)

    @classmethod
    def get_projet_case(cls, project_id: int) -> DataFactoryCases:
        """
        获取项目下的所有造数场景
        :param project_id: 项目id
        :return:
        """
        case_infos = cls.get_with_params(project_id = project_id, _fields = CaseDto)
        return case_infos

    @classmethod
    def project_ids(cls, user: dict):
        """
        获取用户所拥有的项目id
        :param user: 用户数据
        :return:
        """
        filter_list = []
        project_ids = [i[0] for i in ProjectDao.get_user_all_projects(user)]
        filter_list.append(DataFactoryCases.project_id.in_(project_ids))
        return filter_list

    @classmethod
    def get_user_group_name(cls, user: dict):
        """
        获取用户权限范围内的业务线
        :param user:
        :return:
        """
        groups = cls.get_with_params(filter_list = [ *cls.project_ids(user) ],
                                     _fields = CaseGroupDto, _group = [DataFactoryCases.group_name])
        return groups

    @classmethod
    def get_search_case(cls, user: dict, search: str):
        """
        模糊搜索用例，用于前端查询
        :param user: 用户数据
        :param search: 搜索内容
        :return:
        """
        filter_list = []
        search_str = f"%{search}%"
        filter_list.append(or_(DataFactoryCases.name.like(search_str),
                               DataFactoryCases.title.like(search_str),
                               DataFactoryCases.owner.like(search_str),
                               DataFactoryCases.description.like(search_str),
                               ))
        filter_list.extend(cls.project_ids(user))
        cases = cls.get_with_params(filter_list = filter_list, _fields = CaseSearchDto)
        return cases

    @classmethod
    def get_all_cases(cls, user: dict, page: int = 1, limit: int = 10, show: str = None, project_id: int = None, case_id: int = None):
        """
        用例列表展示
        :param user: 用户数据
        :param page: 页码
        :param limit: 页码大小
        :param show: 筛选类型
        :param project_id: 项目id
        :param case_id: 用例id
        :return:
        """
        with Session() as session:
            # 别名
            like_ = aliased(DataFactoryCasesLike)
            collection_ = aliased(DataFactoryCasesCollection)

            # 只取未删除的数据
            filter_list = [DataFactoryCases.del_flag == DeleteEnum.no.value]
            # 如果like_表中 del_flag字段标识为0则为已点赞=True，其余情况为未点赞=False
            is_like = case_([(like_.del_flag == DeleteEnum.no.value, True)], else_=False).label("like")
            # 如果collection_表中 del_flag字段标识为0则为已收藏=True，其余情况为未收藏=False
            is_collection = case_([(collection_.del_flag == DeleteEnum.no.value, True)], else_=False).label("collection")

            # 子表-统计各造数场景点赞数和收藏数, 子查询(subquery)
            summary = session.query(DataFactoryCases.id.label("cases_id"),
                                    func.count(distinct(like_.id)).label("like_num"),
                                    func.count(distinct(collection_.id)).label("collection_num")). \
                outerjoin(like_, and_(DataFactoryCases.id == like_.cases_id,
                                     like_.del_flag == 0)). \
                outerjoin(collection_, and_(DataFactoryCases.id == collection_.cases_id,
                                           collection_.del_flag == 0)).group_by(DataFactoryCases.id).subquery()

            # 为null的数据默认为0
            like_num = func.ifnull(summary.c.like_num, 0).label("like_num")
            collection_num = func.ifnull(summary.c.collection_num, 0).label("collection_num")

            # 用户有效的项目id
            filter_list.extend(cls.project_ids(user))
            # 根据项目id查询
            if project_id:
                filter_list.append(DataFactoryCases.project_id == project_id)
            # 根据case id查询
            if case_id:
                filter_list.append(DataFactoryCases.id == case_id)

            if show:
                if show in ShowEnum.get_member_values():
                    # 获取我创建的
                    if show == ShowEnum.my.value:
                        filter_list.append(DataFactoryCases.owner == user['username'])
                    # 获取我的喜欢
                    elif show == ShowEnum.like.value:
                        my_like = [like_.create_id == user['id'], like_.del_flag == 0]
                        filter_list.extend(my_like)
                    # 获取我的收藏
                    elif show == ShowEnum.collection.value:
                        my_collection = [collection_.create_id == user['id'], collection_.del_flag == 0]
                        filter_list.extend(my_collection)
                    elif show == ShowEnum.all.value:
                        pass
                    else:
                        raise BusinessException("类型有误！！！")
                else:
                    # 业务线分组
                    filter_list.append(DataFactoryCases.group_name == show)

            # cases主表关联like表、collection表、summary表
            case = session.query(like_num, collection_num, DataFactoryCases.project_id, DataFactoryCases.id,
                                 DataFactoryCases.title, DataFactoryCases.group_name, DataFactoryCases.description,
                                 DataFactoryCases.owner, is_like, is_collection, DataFactoryCases.update_time). \
                outerjoin(like_, and_(DataFactoryCases.id == like_.cases_id,
                                     like_.del_flag == 0,
                                     like_.create_id == user['id'])). \
                outerjoin(collection_, and_(DataFactoryCases.id == collection_.cases_id,
                                           collection_.del_flag == 0,
                                           collection_.create_id == user['id'])). \
                outerjoin(summary, DataFactoryCases.id == summary.c.cases_id)

            # 过滤条件
            case = case.filter(*filter_list)
            # 分页
            case_infos = case.order_by(asc(DataFactoryCases.id)).limit(limit).offset((page - 1) * limit).all()
            count = case.count()
            return case_infos, count