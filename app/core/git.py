# -*- coding: utf-8 -*- 
# @Time : 2022/6/25 23:15 
# @Author : junjie
# @File : git.py


from config import FilePath
from app.commons.utils.logger import Log
from app.commons.utils.cmd_utils import CmdUtils
from urllib.parse import quote

class Git(object):

    log = Log("git")

    @staticmethod
    def git_url(url: str, user: str, pwd: str) -> str:
        git_url_list = url.split('/')
        git_url_list[2] = f"{quote(user)}:{pwd}@" + git_url_list[2]
        return '/'.join(git_url_list)

    @staticmethod
    def git_clone_http(git_branch: str, git_url: str, user: str, password: str) -> None:
        """
        http克隆
        :param git_branch: 分支名
        :param git_url: 代码地址
        :param user: git账号
        :param password: git密码
        :return:
        """
        Git.log.info("http克隆开始")
        command_str = f"cd {FilePath.BASE_DIR}\n" \
                      f"git clone -b {git_branch} {Git.git_url(git_url, user, password)}\n"
        CmdUtils.cmd(command_str)
        Git.log.info("http克隆结束")

    @staticmethod
    def git_clone_ssh(git_branch: str, git_url: str) -> None:
        """
        ssh克隆
        :param git_branch: 分支名
        :param git_url: 代码地址
        :return:
        """
        Git.log.info("ssh克隆开始")
        command_str = f"cd {FilePath.BASE_DIR}\n" \
                      f'git clone -b {git_branch} {git_url} --config core.sshCommand="ssh -i {FilePath.RSA_PRI_KEY}"\n'
        CmdUtils.cmd(command_str)
        Git.log.info("ssh克隆结束")

if __name__ == '__main__':
    url = 'git@gitee.com:JokerChat/img.git'
    branch = 'master'
    Git.git_clone_ssh(branch, url)