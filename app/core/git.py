# -*- coding: utf-8 -*- 
# @Time : 2022/6/25 23:15 
# @Author : junjie
# @File : git.py


from app.commons.settings.config import FilePath
from app.commons.utils.cmd_utils import CmdUtils
from urllib.parse import quote
from loguru import logger

class Git(object):

    @staticmethod
    def git_url(url: str, user: str, pwd: str) -> str:
        git_url_list = url.split('/')
        git_url_list[2] = f"{quote(user)}:{quote(pwd)}@" + git_url_list[2]
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
        logger.info("http克隆开始")
        command_str = f"cd {FilePath.BASE_DIR} && " \
                      f"git clone -b {git_branch} {Git.git_url(git_url, user, password)}"
        CmdUtils.cmd(command_str)
        logger.info("http克隆结束")

    @staticmethod
    def git_clone_ssh(git_branch: str, git_url: str) -> None:
        """
        ssh克隆
        :param git_branch: 分支名
        :param git_url: 代码地址
        :return:
        """
        import platform
        if platform.platform() == 'Windows':
            FilePath.RSA_PRI_KEY = FilePath.RSA_PRI_KEY.replace('\\', r'\\')
        logger.info("ssh克隆开始")
        command_str = f"cd {FilePath.BASE_DIR} && " \
                      f'git clone -b {git_branch} {git_url} --config core.sshCommand="ssh -i {FilePath.RSA_PRI_KEY}"'
        CmdUtils.cmd(command_str)
        logger.info("ssh克隆结束")

    @staticmethod
    def git_pull(project_path: str, git_branch: str) -> None:
        """
        拉取代码
        :param project_path: 项目路径
        :param git_branch: 代码分支
        :return:
        """
        logger.info("拉取项目代码开始")
        command_str = f"cd {project_path} && " \
                      f"git fetch --all && " \
                      f"git reset --hard origin/{git_branch}"
        CmdUtils.cmd(command_str)
        logger.info("拉取项目代码结束")

    @staticmethod
    def project_install(project_path: str):
        logger.info("更新依赖开始")
        command_str = f"cd {project_path} && " \
                      f"pip install -r requirements.txt --default-timeout=60 -i https://pypi.tuna.tsinghua.edu.cn/simple"
        p = CmdUtils.cmd(command_str, timeout=60)
        logger.info("更新依赖结束")
        return p.stdout

if __name__ == '__main__':
    url = 'git@gitee.com:JokerChat/img.git'
    branch = 'master'
    Git.git_clone_ssh(branch, url)