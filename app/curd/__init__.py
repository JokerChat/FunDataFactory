# -*- coding: utf-8 -*- 
# @Time : 2022/5/3 08:57 
# @Author : junjie
# @File : __init__.py

import os, importlib, sys
from app.models import Base, engine
from config import FilePath


def get_curd_path():
    """获取curd目录下所有的xxxDao.py"""
    curd_path_list = []
    for file in os.listdir(FilePath.CURD_PATH):
        # 拼接目录
        file_path = os.path.join(FilePath.CURD_PATH, file)
        # 判断过滤, 取有效目录
        if os.path.isdir(file_path) and '__pycache__' not in file:
            from collections import defaultdict
            path_dict = defaultdict(list)
            # 获取目录下所有的xxxDao.py
            for py_file in os.listdir(file_path):
                if py_file.endswith('py') and 'init' not in py_file:
                    path_dict[file].append(py_file.split('.')[0])
            curd_path_list.append(path_dict)
    return curd_path_list

dao_path_list = get_curd_path()
for path in dao_path_list:
    for file_path,pys in path.items():
        # 拼接对应的curd目录
        son_dao_path = os.path.join(FilePath.CURD_PATH, file_path)
        # 导包时, 默认在这个路径下查找
        sys.path.append(son_dao_path)
        for py in pys:
            # 动态导包进去
            importlib.import_module(py)

Base.metadata.create_all(engine)