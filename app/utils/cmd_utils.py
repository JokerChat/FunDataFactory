# -*- coding: utf-8 -*- 
# @Time : 2022/6/25 22:30 
# @Author : junjie
# @File : cmd_utils.py

import subprocess
from app.utils.logger import Log

class CmdUtils(object):

    log = Log("CmdUtils")

    @staticmethod
    def cmd(cmd_str: str, timeout: int = 10):
        """
        执行shell命令
        :param cmd_str: 字符串命令
        :param timeout: 超时时间
        :return:
        """
        try:
            subprocess.run(cmd_str, shell=True, check=True, timeout=timeout)
        except Exception as e:
            CmdUtils.log.error(f"{cmd_str} 命令执行失败, 错误信息: {str(e)}")
            raise Exception(f"命令执行失败!!! ")