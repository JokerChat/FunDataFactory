# -*- coding: utf-8 -*- 
# @Time : 2022/5/3 08:57 
# @Author : junjie
# @File : __init__.py


from app.routers.user import user


data = [
    (user.router, '/api/user', ["用户模块"])
]