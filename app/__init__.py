# -*- coding: utf-8 -*- 
# @Time : 2022/5/3 08:56 
# @Author : junjie
# @File : __init__.py

from fastapi import FastAPI
from config import Text

fun = FastAPI(title=Text.TITLE, version=Text.VERSION, description=Text.DESCRIPTION)
