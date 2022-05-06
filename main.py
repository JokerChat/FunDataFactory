# -*- coding: utf-8 -*- 
# @Time : 2022/5/3 00:00 
# @Author : junjie
# @File : main.py

from app import fun
from app.utils.logger import Log

@fun.get("/")
async def root():
    logger = Log('测试模块')
    logger.info('欢迎来到方总的数据工厂~')
    return {"message": "Hello World"}

