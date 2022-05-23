# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 17:00 
# @Author : junjie
# @File : UserDao.py

from app.models import Session
from sqlalchemy import or_, func
from app.models.user import DataFactoryUser
from app.utils.logger import Log
from config import Permission
from app.utils.exception_utils import record_log
from app.routers.user.user_schema import LoginUserBody
from datetime import datetime


class UserDao(object):

    log = Log('UserDao')

    @classmethod
    @record_log
    def register_user(cls, username: str, name: str, password: str, email: str) -> None:
        """
        :param username: 用户名
        :param name: 姓名
        :param password: 密码
        :param email: 邮箱号
        :return:
        """
        with Session() as session:
            # 先查询用户名或邮箱号是否重复
            users = session.query(DataFactoryUser).filter(or_(DataFactoryUser.username == username, DataFactoryUser.email == email)).first()
            if users:
                raise Exception('用户名或邮箱号重复')
            # 统计用户表的用户数
            count = session.query(func.count(DataFactoryUser.id)).group_by(DataFactoryUser.id).count()
            user = DataFactoryUser(username, name, password, email)
            # 如果第一个进来，默认是管理员权限
            if count == 0 :
                user.role = Permission.ADMIN
            session.add(user)
            session.commit()


    @classmethod
    @record_log
    def user_login(cls, data: LoginUserBody) -> DataFactoryUser:
        """
        :param data: 用户模型
        :return:
        """
        with Session() as session:
            user = session.query(DataFactoryUser).filter(DataFactoryUser.username == data.username, DataFactoryUser.password == data.password).first()
            if user is None:
                raise Exception("用户名或密码错误")
            if user.is_valid:
                # is_valid == true, 说明被冻结了
                raise Exception("对不起, 你的账号已被冻结, 请联系管理员处理")
            user.last_login_time = datetime.now()
            session.commit()
            # 进行对象刷新，更新对象，让对象过期，从而在下次访问时重新加载
            session.refresh(user)
            return user



