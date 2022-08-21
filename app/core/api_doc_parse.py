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

    def exec(self) -> None:
        """执行apidoc命令"""
        cmd = f"apidoc -i {self.script_path} -o {self.doc_path}"
        CmdUtils.cmd(cmd)

    @exception_log
    def get_api_data(self) -> dict:
        """获取api_data数据"""
        api_data_path = os.path.join(self.doc_path, 'api_data.json')
        if not os.path.exists(api_data_path):
            raise BusinessException(f"找不到对应的api_data.json, 请执行apidoc命令")
        with open(api_data_path, 'r', encoding='utf-8') as f:
            api_data = json.load(f)
        return api_data

    @exception_log
    def parse_apidoc(self) -> list:
        """解析api_data数据"""
        api_data = self.get_api_data()
        case_list = []
        for case in api_data:
            # body 解析
            params = []
            example_params = {}
            if "parameter" in case and "fields" in case['parameter'] and case['parameter']['fields']:
                for group_key in case['parameter']['fields']:
                    params.extend(case['parameter']['fields'][group_key])
                params = self.__fields_value_change(self.__remove_fields_ptag(params))
            # 请求示例解析
            if "parameter" in case and "examples" in case['parameter'] and case['parameter']['examples']:
                # 默认取第一个
                try:
                    content = case['parameter']['examples'][0]['content']
                    example_params = json.loads(content)
                except:
                    self.log.error(
                        f"解析请求示例json失败, 场景标题: {case['title']}, 方法名: {case['name']}, 场景标题: {case['title']}, 路径: {case['filename']}")
                    example_params = {}

            # header 解析
            header = []
            if "header" in case and "fields" in case['header'] and 'Header' in case['header']['fields']:
                header = self.__fields_value_change(case['header']['fields']['Header'])

            # response解析 默认取200
            response = []
            example_response = {}
            if "success" in case and "fields" in case['success'] and "200" in case['success']['fields']:
                response = self.__fields_value_change(self.__remove_fields_ptag(case['success']['fields']['200']))

            # 返回示例解析
            if "success" in case and "examples" in case['success'] and case['success']['examples']:
                # 默认取第一个
                try:
                    content = case['success']['examples'][0]['content']
                    example_response = json.loads(content)
                except:
                    self.log.error(
                        f"解析返回示例json失败, 场景标题: {case['title']}, 方法名: {case['name']}, 场景标题: {case['title']}, 路径: {case['filename']}")
                    example_response = {}

            # 组装case对象信息
            case_dict = dict(
                title=case['title'],
                name=case['name'],
                description=self.__remove_ptag(case['description']) if case.get('description', None) else None,
                group_name=case['group'],
                header=json.dumps(header, ensure_ascii=False),
                owner=case['permission'][0]['name'] if case.get('permission', None) else None,
                path=self.__get_path(case['filename']),
                param_in=self.__tree_params(params),
                param_out=self.__tree_params(response),
                example_param_in=json.dumps(example_params, ensure_ascii=False),
                example_param_out=json.dumps(example_response, ensure_ascii=False)
            )
            case_list.append(case_dict)
        return case_list

    @staticmethod
    def __remove_ptag(str_: str) -> str:
      """
      去除字符串中的P标签
      :param str_:
      :return:
      """
      import re
      regex = r'</?p>'
      new_str = re.sub(regex, "", str_)
      return new_str

    @staticmethod
    def __remove_fields_ptag(list_ : list) -> list:
        """
        去除fields中的P标签，顺便补充一下字段
        :param list_: 参数数组
        :return:
        """
        id = 0
        for param in list_:
            id +=1
            # 赋值id key，用于前端展示
            param['id'] = id
            if 'description' in param:
                param['description'] = ApiDocParse.__remove_ptag(param['description'])
            # # 如果是object类型，赋值child字段，适用前端展示
            if "Object" in param['type']:
                param['child'] = []
        return list_

    @staticmethod
    def __fields_value_change(param_lsit: list) -> list:
        """
        字段默认值/可选值转换
        :param param_lsit: 字段list
        :return:
        """
        for param in param_lsit:
            # 布尔值类型
            if str(param['type']).lower() == "boolean":
                # 默认值转换
                if "defaultValue" in param:
                    param['defaultValue'] = ApiDocParse.__str_to_bool(str(param['defaultValue']))
                # 可选值转换
                if "allowedValues" in param:
                    new_allowed_values = list(param['allowedValues'])
                    for index, value in enumerate(new_allowed_values):
                        new_allowed_values[index] = ApiDocParse.__str_to_bool(str(value))
                    param['allowedValues'] = new_allowed_values

            # array类型，一般不维护可选值，不解析可选值
            if str(param['type']).lower() == "array" and "defaultValue" in param:
                # 默认值转换 低版本apidc，array类型缺失"]"，补全[]
                param['defaultValue'] = str(param['defaultValue']) + ']'

            # string类型，可选值去除双引号
            if str(param['type']).lower() == "string" and "allowedValues" in param:
                new_allowed_values = list(param['allowedValues'])
                for index, value in enumerate(new_allowed_values):
                    new_allowed_values[index] = value.replace('"', '')
                param['allowedValues'] = new_allowed_values

            # number类型
            if str(param['type']).lower() == "number":
                # 默认值转换
                if "defaultValue" in param:
                    param['defaultValue'] = int(param['defaultValue'])
                # 可选值转换
                if "allowedValues" in param:
                    new_allowed_values = list(param['allowedValues'])
                    for index, value in enumerate(new_allowed_values):
                        if isinstance(value, str):
                            new_allowed_values[index] = int(value)
                    param['allowedValues'] = new_allowed_values
        return param_lsit


    @staticmethod
    def __str_to_bool(str_: str) ->bool:
        return True if str_.lower() == 'true' else False

    @staticmethod
    def __get_path(file_path: str) -> str:
        # todo 更深层的模块文件
        """目前只支持cases目录下的文件"""
        method_path = file_path.split('.')[0].split('/')[-2:]
        return '/'.join(method_path)

    @staticmethod
    def __tree_params(param_list: list) -> str:
        """
        生成树
        :param param_list: 参数
        :return:
        """
        tree_params = []
        link_list = []
        import copy
        param_list_copy = copy.deepcopy(param_list)
        for index, param in enumerate(param_list):
            if "child" in param:
                field_list = param['field'].split('.')
                if len(field_list) > 1:
                    father_key, son_key = field_list[-2:]
                    param['field'] = son_key
                else:
                    father_key = param['field']
                param_list_copy[index]['child'] = ApiDocParse.__find_son_params(father_key, param_list, link_list)
                if param['id'] not in link_list:
                    link_list.append(param['id'])
                    tree_params.append(param_list_copy[index])
            else:
                if param['id'] not in link_list:
                    link_list.append(param['id'])
                    tree_params.append(param_list_copy[index])
        return json.dumps(tree_params, ensure_ascii=False)

    @staticmethod
    def __find_son_params(pk, params_list, link_list):
        """
        找出子
        :param pk: 父参数
        :param params_list: 参数列表
        :param link_list: 链路集合
        :return:
        """
        son_params = []
        for param in params_list:
            field_list = param['field'].split('.')
            if len(field_list) > 1:
                father_key, son_key = field_list[-2:]
                if father_key == pk:
                    if "Object" in param['type']:
                        # 如果有object类型继续递归找出子
                        param['child'] = ApiDocParse.__find_son_params(son_key, params_list, link_list)
                    param['field'] = son_key
                    son_params.append(param)
                    link_list.append(param['id'])
        return son_params


if __name__ == '__main__':
    from app.core.get_project_path import ProjectPath
    project_path, cases_path = ProjectPath.get('funcase', 'case')
    apidoc = ApiDocParse(project_path, cases_path)
    data = apidoc.parse_apidoc()
    print(json.dumps(data, ensure_ascii=False))