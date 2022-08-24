# -*- coding: utf-8 -*- 
# @Time : 2022/5/3 00:00 
# @Author : junjie
# @File : main.py

from app import fun, init_logging, register_routers, register_middlewares, create_global_exception_handler
from app.logic.project_logic.project_logic import start_init_project_logic
from loguru import logger


@fun.on_event('startup')
async def startup_event():
    """项目启动时，要做的事情"""

    # step1 初始化项目日志器
    init_logging()
    logger.info('logging is init success！！！')

    # step2 注册路由
    await register_routers(fun)
    logger.info('routers is register success！！！')
    # step3 注册中间件
    await register_middlewares(fun)
    logger.info('middlewares is register success！！！')

    # step4 注册全局异常处理器
    await create_global_exception_handler(fun)
    logger.info('exceptionHandler is register success！！！')

    from app.models import Base, engine
    # step5 向数据库发出建表完成类与表的映射
    Base.metadata.create_all(engine)
    logger.info('db is init success！！！')

    # step6 初始化项目
    start_init_project_logic()
    logger.info('project is init success！！！')

    logger.info('FunDataFactory is start success！！！')