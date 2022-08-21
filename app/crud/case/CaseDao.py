# -*- coding: utf-8 -*-
# @Time : 2022/8/21 20:27
# @Author : junjie
# @File : CasesDao.py

from app.models.cases import DataFactoryCases
from app.routers.project.response_model.project_out import CaseDto
from app.commons.exceptions.global_exception import BusinessException
from loguru import logger
from app.crud import BaseCrud

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