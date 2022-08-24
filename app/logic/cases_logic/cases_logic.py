# -*- coding: utf-8 -*- 
# @Time : 2022/8/24 21:40 
# @Author : junjie
# @File : cases_logic.py

from app.commons.utils.context_utils import REQUEST_CONTEXT
from app.crud.operation.OperationDao import LikeOperationDao, CollectionOperationDao

def like_logic(id : int):
    user = REQUEST_CONTEXT.get().user
    result = LikeOperationDao.like(id, user)
    return result

def collection_logic(id : int):
    user = REQUEST_CONTEXT.get().user
    result = CollectionOperationDao.collection(id, user)
    return result