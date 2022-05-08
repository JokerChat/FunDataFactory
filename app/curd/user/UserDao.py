# -*- coding: utf-8 -*- 
# @Time : 2022/5/8 17:00 
# @Author : junjie
# @File : UserDao.py

from app.models import Session
from sqlalchemy import or_, func
from app.models.user import DataFactoryUser
from app.utils.logger import Log
from config import Permission

class UserDao(object):

    log = Log('UserDao')

    @classmethod
    def register_user(cls, username: str, name: str, password: str, email: str) -> None:
        """
        :param username: 用户名
        :param name: 姓名
        :param password: 密码
        :param email: 邮箱号
        :return:
        """
        try:
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
        except Exception as e:
            cls.log.error(f"用户注册失败: {str(e)}")
            raise Exception(str(e))
