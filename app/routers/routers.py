# -*- coding: utf-8 -*- 
# @Time : 2022/5/3 08:57 
# @Author : junjie
# @File : __init__.py


from app.routers import user, project, cases, data
from collections import namedtuple

Router = namedtuple('router', ['module', 'prefix', 'tags'])

data_ = [
        Router(module=user.router, prefix='/api/user', tags=["用户模块"]),
        Router(module=project.router, prefix='/api/project', tags=["项目管理模块"]),
        Router(module=cases.router, prefix='/api/cases', tags=["用例模块"]),
        Router(module=data.router, prefix='/api/data', tags=["数据统计"])
]