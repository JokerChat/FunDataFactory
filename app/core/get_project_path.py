# -*- coding: utf-8 -*- 
# @Time : 2022/8/15 23:27 
# @Author : junjie
# @File : get_project_path.py

from app.commons.settings.config import FilePath
from app.commons.exceptions.global_exception import BusinessException
import os

class ProjectPath(object):

    @staticmethod
    def get(project_name: str, directory_name: str) -> (str, str):
        """
        获取项目路径和脚本路径
        :param project_name:项目名
        :param directory_name: 造数场景目录名
        :return: 项目目录，脚本目录
        """
        project_path = os.path.join(FilePath.BASE_DIR, project_name)
        if not os.path.isdir(project_path):
            raise BusinessException(f"找不到{project_name}这个项目")
        script_path = os.path.join(project_path, directory_name)
        if not os.path.isdir(script_path):
            raise BusinessException(f"找不到{directory_name}这个脚本目录")
        return project_path, script_path