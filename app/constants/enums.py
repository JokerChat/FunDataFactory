# -*- coding: utf-8 -*- 
# @Time : 2022/7/18 23:22 
# @Author : junjie
# @File : enums.py

from enum import Enum

class BaseEnum(Enum):
    """枚举基类"""
    @classmethod
    def get_member_values(cls):
        return [item.value for item in cls._member_map_.values()]

    @classmethod
    def get_member_names(cls):
        return [name for name in cls._member_names_]


class IntEnum(int, BaseEnum):
    """整型枚举"""
    pass

class StrEnum(str, BaseEnum):
    """字符串枚举"""
    pass

class PermissionEnum(IntEnum):
    members = 0 # 普通用户
    leader = 1 # 组长
    admin = 2 # 超管

class DeleteEnum(IntEnum):
    no = 0 # 未删除
    yes = 1 # 已删除

class ProjectRoleEnum(IntEnum):
    members = 0 # 普通用户
    leader = 1 # 组长

class PullTypeEnum(IntEnum):
    http = 0
    ssh = 1

class ShowEnum(StrEnum):
    my = "my"
    like = "like"
    collection = "collection"
    all = "all"

class RunStatusEnum(IntEnum):
    success = 0
    exception = 1
    fail = 2

class CallTypeEnum(IntEnum):
    plat = 0
    out = 1
    rpc = 2

class SysEnum(StrEnum):
    git = "git"
    platform = "platform"