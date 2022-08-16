# -*- coding: utf-8 -*- 
# @Time : 2022/8/16 19:48 
# @Author : junjie
# @File : api_doc_parse.py
import os
import functools
import json
from loguru import logger
from app.commons.utils.cmd_utils import CmdUtils
from app.commons.exceptions.global_exception import BusinessException



# 捕获异常装饰器
def exception_log(func):
    functools.wraps(func)
    def wrapper(*args, **kwargs):
        cls = args[0]
        try:
            return func(*args, **kwargs)
        except Exception as e:
            func_name = func.__doc__
            # func_params = dict(args=args, kwargs=kwargs)
            import traceback
            err = traceback.format_exc()
            cls.log.error(f"{func_name}失败: {err}")
            raise BusinessException(str(e))
    return wrapper


class ApiDocParse(object):

    def __init__(self, project_path: str, script_path: str):
        """
        初始化
        :param project_path: 项目路径
        :param script_path: 脚本路径
        """
        self.log = logger
        self.project_path = project_path
        self.script_path = script_path
        self.doc_path = os.path.join(self.project_path, 'doc')

    def exec(self):
        """执行apidoc命令"""
        cmd = f"apidoc -i {self.script_path} -o {self.doc_path}"
        CmdUtils.cmd(cmd)

    @exception_log
    def get_api_data(self):
        """获取api_data数据"""
        api_data_path = os.path.join(self.doc_path, 'api_data.json')
        if not os.path.exists(api_data_path):
            raise BusinessException(f"找不到对应的api_data.json, 请执行apidoc命令")
        with open(api_data_path, 'r', encoding='utf-8') as f:
            api_data = json.load(f)
        return api_data

    @exception_log
    def parse_apidoc(self):
        """解析api_data数据"""
        api_data = self.get_api_data()
        return api_data