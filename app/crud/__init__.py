# -*- coding: utf-8 -*- 
# @Time : 2022/5/3 08:57 
# @Author : junjie
# @File : __init__.py
# 本页代码"借鉴"pity
# pity github: https://github.com/wuranxu/pity



from app.models.base import FunBaseModel
from typing import Type, Union
from loguru import logger
from app.commons.exceptions.global_exception import BusinessException
from app.commons.requests.request_model import BaseBody
from app.commons.responses.response_model import BaseDto
from datetime import datetime
from functools import wraps
from enum import Enum
from app.models import Session
from app.constants.enums import DeleteEnum



def connect(func):
    """
    自动创建session装饰器
    """
    @wraps(func)
    def wrapper(cls, *args, **kwargs):
        try:
            session = kwargs.get("session")
            if session is not None:
                return func(cls, session, *args[1:], **kwargs)
            with Session() as ss:
                return func(cls, ss, *args[1:], **kwargs)
        except Exception as e:
            import traceback
            logger.exception(traceback.format_exc())
            logger.error(f"操作{cls.model.__name__}失败, error: {e}")
            raise BusinessException(f"操作数据库失败: {e}")
    return wrapper

# 只支持单表
class BaseCrud(object):

    model: Type[FunBaseModel] = None


    @classmethod
    @connect
    def get_with_params(cls, session: Session, *, filter_list: list = None,
                        _sort: list = None, _fields: Type[BaseDto] = None, _group: list = None, **kwargs):
        """
        查询数据
        :param session: 会话
        :param filter_list: 过滤条件，比较特殊的，or_(xxx == xxx)
        :param _sort: 排序字段
        :param kwargs:  不定传参，xx = xx
        :param _fields: Dto 过滤查询
        :param _group: 分组
        :return: 查询对象
        """
        query_obj = cls.query_wrapper(session, filter_list, _sort, _fields, _group, **kwargs)
        return query_obj.all()


    @classmethod
    def query_wrapper(cls, session: Session, filter_list: list = None,
                      _sort: list = None, _fields: Type[BaseDto] = None, _group: list = None, **kwargs):
        """
        查询数据
        :param session: 会话
        :param filter_list: 过滤条件，比较特殊的，or_(xxx == xxx)
        :param _sort: 排序字段，[xxx.xxx]
        :param kwargs: 不定传参，xx = xx
        :param _fields: Dto 过滤查询
        :param _group: 分组
        :return: 查询语句
        """
        _filter_list = cls.__filter_k_v(filter_list, **kwargs)
        if _fields:
            field_list = []
            for field in _fields.__fields__.keys():
                field_list.append(getattr(cls.model, field))
            query_obj = session.query(*field_list).filter(*_filter_list)
        else:
            query_obj = session.query(cls.model).filter(*_filter_list)
        if _group:
            query_obj = query_obj.group_by(*_group)
        # 有排序字段时，进行排序
        return query_obj.order_by(*_sort) if _sort else query_obj

    @classmethod
    def __filter_k_v(cls, filter_list: list = None, not_del: bool = False,  **kwargs):
        """
        查询主逻辑
        :param filter_list: 过滤条件，比较特殊的，or_(xxx == xxx)
        :param kwargs: 不定传参，xx = xx
        :param not_del: nol_del = True时，不过滤删除数据
        :return: filter_list
        """
        filter_list = filter_list if filter_list else list()
        # 判断表是否有del_flag字段
        if getattr(cls.model, 'del_flag', None) and not not_del:
            # 只取未删除的数据
            filter_list.append(getattr(cls.model, 'del_flag') == DeleteEnum.no.value)
        for k, v in kwargs.items():
            # 过滤None的字段值，注意 0 和 False
            if v is None:
                continue
            elif isinstance(v, (bool, int)):
                filter_list.append(getattr(cls.model, k) == v)
            else:
                # 判断是否模糊查询，必须字符串，字符串开头%或者结尾%
                like = isinstance(v, str) and (v.startswith("%") or v.endswith("%"))
                if like and v != '%%':
                    filter_list.append(getattr(cls.model, k).like(v))
                else:
                    filter_list.append(getattr(cls.model, k) == v)
        return filter_list



    @classmethod
    @connect
    def get_with_pagination(cls, session: Session, *, page: int = 1, limit: int = 10, **kwargs):
        """
        分页查询
        :param session: 会话
        :param page: 页码
        :param limit: 大小
        :param kwargs: 不定传参
        :return: 总数，查询对象
        """
        query_obj = cls.query_wrapper(session, **kwargs)
        total = query_obj.count()
        return total, query_obj.limit(limit).offset((page - 1) * limit).all()

    @classmethod
    @connect
    def get_with_existed(cls, session: Session, *, filter_list: list = None, **kwargs):
        """
        判断数据是否存在
        :param session: 会话
        :param filter_list: 过滤条件，比较特殊的，or_(xxx == xxx)
        :param kwargs: 不定传参
        :return:
        """
        _filter_list = cls.__filter_k_v(filter_list, **kwargs)
        query = session.query(cls.model).filter(*_filter_list)
        # 获取结果，ant为true或者false
        ant = session.query(query.exists()).scalar()
        return ant

    @classmethod
    @connect
    def get_with_first(cls, session: Session, **kwargs):
        """
        获取第一条数据
        :param session: 会话
        :param kwargs: 不定传参
        :return:
        """
        sql_obj = cls.query_wrapper(session, **kwargs)
        return sql_obj.first()


    @classmethod
    @connect
    def get_with_id(cls, session: Session, *, id: int):
        """
        根据主键id查询数据
        :param session: 会话
        :param id: 主键id
        :return:
        """
        sql_obj = cls.query_wrapper(session, id=id)
        return sql_obj.first()

    @classmethod
    @connect
    def update_by_id(cls, session: Session, *, model: Union[dict, BaseBody], user: dict=None, not_null = False, **kwargs):
        """
        通过主键id更新数据
        :param session: 会话
        :param model: 更新模型
        :param user: 更新用户数据
        :param not_null: not_null=True 只有非空字段才更新数据
        :return:
        """
        if isinstance(model, dict):
            id = model['id']
            model_dict = model
        else:
            id = model.id
            model_dict = vars(model)
        query = cls.query_wrapper(session, id=id, **kwargs)
        query_obj = query.first()
        if query_obj is None:
            raise BusinessException("数据不存在")
        for var, value in model_dict.items():
            # 如果value是枚举值，得通过xxx.value获取值
            if isinstance(value, Enum): value = value.value
            if not_null:
                # 过滤None的字段值，注意 0 和 False
                if value is None:
                    continue
                if isinstance(value, (bool, int)) or value:
                    setattr(query_obj, var, value)
            else:
                setattr(query_obj, var, value)
            if user:
                setattr(query_obj, 'update_id', user['id'])
                setattr(query_obj, 'update_name', user['username'])
        session.commit()
        session.refresh(query_obj)
        return query_obj

    @classmethod
    @connect
    def update_by_map(cls, session: Session, *, filter_list: list, user: dict=None, **kwargs):
        """
        批量更新数据
        :param session: 会话
        :param filter_list: 过滤条件
        :param user: 更新人
        :param kwargs: 要更新的数据，k = v
        :return:
        """
        # https://docs.sqlalchemy.org/en/14/errors.html#error-bhk3
        if getattr(cls.model, 'update_id') and getattr(cls.model, 'update_name') and user:
            kwargs['update_id'] = user['id']
            kwargs['update_name'] = user['username']
        query_obj = session.query(cls.model).filter(*filter_list)
        query_obj.update(kwargs)
        session.commit()
        return query_obj.all()


    @classmethod
    @connect
    def insert_by_model(cls, session: Session, *, model_obj: FunBaseModel):
        """
        :param session: 会话
        :param model_obj: 实例化的表
        :return:
        """
        session.add(model_obj)
        session.commit()
        session.refresh(model_obj)
        return model_obj

    @classmethod
    @connect
    def delete_by_id(cls, session: Session, *, id: int, user: dict = None, **kwargs):
        """
        通过主键id删除数据
        :param session: 会话
        :param id: 主键id
        :param user: 操作人
        :return:
        """
        query = cls.query_wrapper(session, id=id, **kwargs)
        query_obj = query.first()
        if query_obj is None:
            raise BusinessException("数据不存在")
        setattr(query_obj, 'del_flag', DeleteEnum.yes.value)
        setattr(query_obj, 'update_time', datetime.now())
        if user:
            setattr(query_obj, 'update_id', user['id'])
            setattr(query_obj, 'update_name', user['username'])
        session.commit()
        session.refresh(query_obj)
        return query_obj

    @classmethod
    @connect
    def get_with_count(cls, session: Session(), **kwargs):
        """
        统计数据
        :param session: 会话
        :param kwargs:
        :return:
        """
        query = cls.query_wrapper(session, **kwargs)
        return query.group_by(cls.model.id).count() if getattr(cls.model, 'id', None) else query.count()