# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 17:00 
# @Author : junjie
# @File : UserDao.py

from sqlalchemy import or_
from app.models.user import DataFactoryUser
from app.constants.enums import PermissionEnum
from app.routers.user.request_model.user_in import LoginUserBody, UpdateUserBody, SearchUserBody, RegisterUserBody
from app.routers.user.response_model.user_out import SearchUserDto, UserDto
from datetime import datetime
from app.commons.exceptions.global_exception import BusinessException
from app.crud import BaseCrud


class UserDao(BaseCrud):

    model = DataFactoryUser

    @classmethod
    def register_user(cls, body: RegisterUserBody) -> None:
        """
        :param body: 注册模型
        :return:
        """
        # 先查询用户名或邮箱号是否重复
        filter_list = [or_(cls.model.username == body.username, cls.model.email == body.email)]
        ant = cls.get_with_existed(filter_list=filter_list)
        if ant:
            raise BusinessException("用户名或邮箱号重复")
        # 统计用户表的用户数
        count = cls.get_with_count()
        user = DataFactoryUser(body)
        # 如果第一个进来，默认是管理员权限
        if count == 0 :
            user.role = PermissionEnum.admin.value
        cls.insert_by_model(model_obj=user)



    @classmethod
    def user_login(cls, body: LoginUserBody) -> DataFactoryUser:
        """
        :param body: 用户模型
        :return:
        """
        user_obj = cls.get_with_first(username = body.username, password = body.password)
        if user_obj is None:
            raise BusinessException("用户名或密码错误")
        if user_obj.is_valid:
            # is_valid == true, 说明被冻结了
            raise BusinessException("对不起, 你的账号已被冻结, 请联系管理员处理")
        update_map = {
            "id": user_obj.id,
           "last_login_time":  datetime.now()
        }
        user = cls.update_by_id(model = update_map)
        return user


    @classmethod
    def get_user_infos(cls, page: int=1, limit: int=10, search: str=None) ->(int, DataFactoryUser):
        """
        :param page: 页码
        :param limit: 多少条一页
        :param search: 搜索内容
        :return:
        """
        # like 比较特殊，必须f"%{search}%" if search else None
        total, user_infos = cls.get_with_pagination(page=page, limit=limit,
                                                    _sort=[DataFactoryUser.id.desc()],
                                                    _fields = UserDto,
                                                    username = f"%{search}%" if search else None)
        return total, user_infos


    @classmethod
    def search_user(cls, body: SearchUserBody) -> DataFactoryUser:
        """
        搜索用户
        :param body: 输入内容
        :return:
        """
        filter_list = [or_(DataFactoryUser.username.like(f"%{body.keyword}%"),
                           DataFactoryUser.name.like(f"%{body.keyword}%"),
                           DataFactoryUser.email.like(f"%{body.keyword}%"))]
        user = cls.get_with_params(filter_list=filter_list, _fields = SearchUserDto, is_valid = False)
        return user

    @classmethod
    def update_user(cls, body: UpdateUserBody, user_data: dict) -> None:
        """
        :param user_data: 用户数据
        :param body: 更新的数据
        :return:
        """
        ant = cls.get_with_existed(id=body.id)
        if not ant:
            raise BusinessException("用户不存在")
        # not_null=True 只有非空字段才更新数据
        cls.update_by_id(model = body, user=user_data, not_null=True)

    @classmethod
    def user_summary(cls):
        """统计用户数量"""
        user_sum = cls.get_with_count()
        return user_sum