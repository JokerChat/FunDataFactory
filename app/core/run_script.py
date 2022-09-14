# -*- coding: utf-8 -*- 
# @Time : 2022/9/4 23:23 
# @Author : junjie
# @File : run_script.py

import sys
import importlib
import os
from app.core.get_project_path import ProjectPath
from app.commons.exceptions.global_exception import BusinessException


class RunScript(object):

    @staticmethod
    def run(path: str, method: str, params: dict, project: str, directory: str):
        """
        动态导包执行方法
        :param path: 用例路径
        :param method: 方法名
        :param params: 入参
        :param project: 项目名
        :param directory: 脚本目录名
        :return:
        """
        project_path, case_path = ProjectPath.get(project, directory)
        # tag为对应业务线的目录名，py_file为脚本的py文件
        tag, py_file = path.split('/')
        # 拼接case目录路径
        tag_path = os.path.join(case_path, tag)
        if not os.path.isdir(tag_path):
            raise BusinessException(f"{tag}目录不存在！！！")
        # 导包的搜索目录，以该项目为基础
        sys.path.append(project_path)
        try:
            # 绝对导包进去
            # from funcase.case.shop.demo import *
            module_ = importlib.import_module(f"{project}.{directory}.{tag}.{py_file}")
        except ModuleNotFoundError as e:
            raise BusinessException(f"导包失败: {e}")
        # 校验module是否有对应方法
        if not hasattr(module_, method):
            raise BusinessException(f"{py_file}.py不存在{method}函数方法！！！")
        try:
            # 执行module_下的某个方法
            script_data = getattr(module_, method)(**params)
            return script_data
        except:
            import traceback
            err_msg = traceback.format_exc()
            raise BusinessException(f"执行失败: {err_msg}")
        finally:
            # 移除导包搜索目录
            sys.path.remove(project_path)


if __name__ == '__main__':
    data = {
        "path": "shop/demo",
        "method": "add",
        "params": {
            "a": 1,
            "b": 77776
        },
        "project": "funcase",
        "directory": "case"
    }
    data = RunScript.run(**data)
    print(data)

