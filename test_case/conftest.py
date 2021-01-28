# __author:"zonglr"
# date:2020/11/6
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

import pytest, jsonpath
from common import request, logger
from test_base_role import createRole, createRoleType
from test_base_user import createUser
from test_config import param_config
from test_base_department import createDept

log = logger.Log()


# 获取权限列表,并返回所有权限id(数组)
# 整个项目测试用例执行之前执行一次，无论调用多少次，也只执行一次
@pytest.fixture(scope="session")
def getPermissoinIds():
    """正常查询"""
    response = request.get('/permission/list')
    assert response['msg'] == '请求成功'
    assert len(response['data']) > 0
    # 获取权限id
    ids = jsonpath.jsonpath(response, '$..id')
    return ids


# 创建一个初始角色分类,并返回角色分类id
# 整个项目测试用例执行之前执行一次，无聊调用多少次，也只执行一次
@pytest.fixture(scope="session", autouse=True)
def createInitRoleType():
    # 创建角色分类
    name = param_config.initRoleTypeName
    response = createRoleType(name=name)
    assert response['msg'] in ('请求成功', '该角色分类名称已存在')
    # 根据角色分类名查询分类id
    list = request.get('/role/findRoleTypeList')
    assert len(list['data']) > 1
    for i in list['data']:
        if i['name'] == name:
            typeId = i['roleTypeId']
            return typeId


# 创建一个初始角色,并返回角色id
# 整个项目测试用例执行之前执行一次，无论调用多少次，也只执行一次
@pytest.fixture(scope="session", autouse=True)
def createInitRole(createInitRoleType):
    # 创建角色
    name = param_config.initRoleName
    response = createRole(name=name, roleType=createInitRoleType)
    assert response['msg'] in ('请求成功', '该角色名称已存在')
    # 根据角色名查询角色id
    list = request.get('/role/findRoleTypeList')
    assert len(list['data']) > 1
    # 查询返回结果中所有的角色名
    names = jsonpath.jsonpath(list, '$..role[*].name')
    # 所有角色id
    ids = jsonpath.jsonpath(list, '$..role[*].id')
    # 根据角色名查询id
    i = 0
    while i < len(names):
        if names[i] == name:
            roleId = ids[i]
            return roleId
        i += 1


# # 创建一个用户名和帐号为test的用户,并返回用户id
# # 整个项目测试用例执行之前执行一次，无论调用多少次，也只执行一次
# @pytest.fixture(scope="session", autouse=True)
# def createInitUser(createInitRole):
#     name = 'test'
#     response = createUser(name='test', loginName=name, roleIds=[createInitRole])
#     assert response['msg'] in ('请求成功', '登录名已存在')
#     # 根据loginName查询初始用户的id（模糊查询，可能查询出其他包含指定值的数据）
#     list = request.get('/user/list?pageNum=0&pageSize=50&loginName=%s' % name)
#     assert list['data']['totalCount'] > 0
#     # 查询返回结果中loginName=name的值
#     for i in list['data']['rows']:
#         if i['loginName'] == name:
#             userId = i['id']
#             return userId
# 新建初始分类，整个项目仅执行一次
# 新建初始一个角色，整个项目仅执行一次

# 创建一个初始部门，并返回部门id，整个项目测试用例执行之前执行一次
@pytest.fixture(scope="session")
def createInitDepartment():
    # 初始化一个部门名称
    deptName = param_config.initDeptName
    # 获取部门id
    detail = request.get('/department/findDepartment')
    departmentId = detail['data'][0]['id']
    # 获取字典部门分类id
    detail2 = request.get('/dictionary/getByType/department_type')
    sortId = detail2['data'][0]['id']
    response = createDept(departmentName=deptName, departmentTypeId=sortId, parentId=departmentId)
    assert response['msg'] in ('请求成功', '部门已存在')
    # 查询列表
    list = request.get('/department/findDepartment')
    assert len(list['data']) > 0
    # 提取所有部门名称
    departmentName = jsonpath.jsonpath(list, '$..childrenDepartment[*].departmentName')
    # 提取所有的部门id
    ids = jsonpath.jsonpath(list, '$..childrenDepartment[*].id')
    # 根据部门名称循环查询部门id
    i = 0
    while i < len(departmentName):
        if departmentName[i] == deptName:
            id = ids[i]
            return id
        i += 1


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
