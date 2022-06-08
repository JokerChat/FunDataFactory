# -*- coding: utf-8 -*- 
# @Time : 2022/6/4 22:32 
# @Author : junjie
# @File : db_utils.py
from datetime import datetime
class DbUtils(object):

    @staticmethod
    def update_model(dist: object, source: dict, update_user: dict=None, not_null: bool=False):
        """
        :param dist: 表对象
        :param source: 更新的数据
        :param update_user: 更新人
        :param not_null: 是否忽略更新null
        :return:
        """
        for var, value in source.items():
            if not_null:
                if value is not None:
                    setattr(dist, var, value)
            else:
                setattr(dist, var, value)
            if update_user:
                setattr(dist, 'update_code', update_user['id'])
                setattr(dist, 'update_name', update_user['username'])

    @staticmethod
    def delete_model(dist: object, delete_user: dict=None):
        """
        :param dist: 表对象
        :param delete_user: 更新人
        :return:
        """
        dist.del_flag = 1
        dist.update_time = datetime.now()
        if delete_user:
            dist.update_code =  delete_user['id']
            dist.update_name =  delete_user['username']