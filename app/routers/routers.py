# -*- coding: utf-8 -*- 
# @Time : 2022/5/3 08:57 
# @Author : junjie
# @File : __init__.py


from app.routers.user import user
from app.routers.project import project


data = [
    (user.router, '/api/user', ["用户模块"]),
    (project.router, '/api/project', ["项目管理模块"])
]