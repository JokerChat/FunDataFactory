# -*- coding: utf-8 -*- 
# @Time : 2022/5/5 22:44 
# @Author : junjie
# @File : logger.py

import inspect
from loguru import logger
from app.constants import constants



class Log(object):

    business = None

    def __init__(self, name='fun'):
        """
        :param name: 模块名
        """
        self.business = name


    def info(self, message: str):
        _, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=constants.FUN_INFO, func=func, line=line,
                    business=self.business).info(message)

    def error(self,  message: str):
        _, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=constants.FUN_ERROR, func=func, line=line,
                    business=self.business).error(message)

    def warning(self, message: str):
        _, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=constants.FUN_ERROR, func=func, line=line,
                    business=self.business).error(message)

    def debug(self, message: str):
        _, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=constants.FUN_INFO, func=func, line=line,
                    business=self.business).error(message)

    def exception(self, message: str):
        _, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=constants.FUN_INFO, func=func, line=line,
                    business=self.business).exception(message)

