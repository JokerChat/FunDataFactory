# -*- coding: utf-8 -*- 
# @Time : 2022/8/24 21:05 
# @Author : junjie
# @File : OperationDao.py

from app.models.cases_like import DataFactoryCasesLike
from app.models.cases_collection import DataFactoryCasesCollection
from app.crud import BaseCrud
from app.constants.enums import DeleteEnum


class LikeOperationDao(BaseCrud):

    model = DataFactoryCasesLike

    @classmethod
    def like(cls, cases_id: int, user: dict) -> bool:
        case = cls.get_with_first(not_del = True, cases_id = cases_id, create_id = user['id'])
        # 已存在点赞记录
        if case:
            # 但是已经点赞了的
            if case.del_flag == DeleteEnum.no.value:
                # 将点赞记录置为删除 == 取消点赞
                cls.delete_by_id(id = case.id, user = user, not_del = True)
                return False
            else:
                # 删除状态的，置为未删除 == 点赞
                cls.update_by_id(model = dict(id = case.id, del_flag = DeleteEnum.no.value), user = user, not_del = True)
                return True
        # 不存在点赞记录，新增点赞记录 == 点赞
        else:
            cases = DataFactoryCasesLike(cases_id, user)
            cls.insert_by_model(model_obj = cases)
            return True


class CollectionOperationDao(BaseCrud):

    model = DataFactoryCasesCollection

    @classmethod
    def collection(cls, cases_id: int, user: dict) -> bool:
        case = cls.get_with_first(not_del = True, cases_id = cases_id, create_id = user['id'])
        # 已存在收藏记录
        if case:
            # 但是已经收藏了的
            if case.del_flag == DeleteEnum.no.value:
                # 将收藏记录置为删除 == 取消点赞
                cls.delete_by_id(id = case.id, user = user, not_del = True)
                return False
            else:
                # 删除状态的，置为未删除 == 点赞
                cls.update_by_id(model = dict(id = case.id, del_flag = DeleteEnum.no.value), user = user, not_del = True)
                return True
        # 不存在点赞记录，新增收藏记录 == 点赞
        else:
            cases = DataFactoryCasesCollection(cases_id, user)
            cls.insert_by_model(model_obj = cases)
            return True