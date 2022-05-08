# -*- coding: utf-8 -*- 
# @Time : 2022/5/3 08:57 
# @Author : junjie
# @File : __init__.py

from app.models import Base, engine

Base.metadata.create_all(engine)