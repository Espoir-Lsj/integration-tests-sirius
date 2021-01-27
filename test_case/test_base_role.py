# __author:"zonglr"
# date:2020/11/28
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, time, jsonpath
from common import logger, request
from test_config import param_config
import test_base_permission

log = logger.Log()

roleName = '一个新角色%d' % param_config.count


# 自定义方法-创建角色分类
def createRoleType(name):
    body = {
        'name': name
    }
    response = request.post_body('/role/createRoleType', body)
    return response


# 自定义方法-创建角色
def createRole(name, roleType, rolePermissionId=None, remark=None):
    body = {
        'name': name,
        'remark': remark,
        'rolePermissionId': rolePermissionId,  # roleId
        'roleType': roleType
    }
    response = request.post_body('/role/createRole', body=body)
    return response


# 自定义方法-修改角色
def editRole(id, name, roleType, remark=None):
    body = {
        'id': id,
        'name': name,
        'roleType': roleType,
        'remark': remark
    }
    response = request.put_body('/role/editRole', body=body)
    return response


# 自定义方法-删除角色
def deleteRole(roleId):
    body = {
        'roleId': roleId
    }
    response = request.delete_body('/role/deleteRole', body)
    return response


# 创建一个新的角色分类，每个类执行一次(涉及到删除角色，所以范围是class)
@pytest.fixture(scope="class")
def createNewRoleType():
    name = '一个新分类%d' % param_config.count
    response = createRoleType(name=name)
    assert response['msg'] in ('请求成功', '该角色分类名称已存在')
    # 根据角色分类名查询分类id
    list = request.get('/role/findRoleTypeList')
    assert len(list['data']) > 1
    for i in list['data']:
        if i['name'] == name:
            typeId = i['roleTypeId']
            return typeId


# 创建一个新的角色,使用新增的分类,每个类执行一次(涉及到删除角色，所以范围是class)
@pytest.fixture(scope="class")
def createNewRole(createNewRoleType):
    response = createRole(name=roleName, roleType=createNewRoleType)
    assert response['msg'] in ('请求成功', '该角色名称已存在')
    # 根据角色分类名查询分类id
    list = request.get('/role/findRoleTypeList')
    assert len(list['data']) > 1
    # 查询返回结果中所有的角色名
    names = jsonpath.jsonpath(list, '$..role[*].name')
    # 所有角色id
    ids = jsonpath.jsonpath(list, '$..role[*].id')
    # 根据角色名查询id
    i = 0
    while i < len(names):
        if names[i] == roleName:
            roleId = ids[i]
            return roleId
        i += 1


class TestCreate:
    """创建角色"""

    name = '测试角色%d' % int(time.time() * 1000)

    def test_01(self, createInitRoleType):
        """角色名为空"""
        response = createRole(name=None, roleType=createInitRoleType)
        assert response['msg'] == '角色只支持中文、英文、数字'

    def test_02(self):
        """角色分类id不存在"""
        response = createRole(name=self.name, roleType=0)
        assert response['msg'] == '该角色分类不存在'

    def test_03(self):
        """角色分类id为空"""
        response = createRole(name=self.name, roleType=None)
        assert response['msg'] == '请填写角色分类名称'

    @pytest.mark.skip('system busy')  # TODO
    def test_04(self, createInitRoleType):
        """复制的角色id不存在"""
        response = createRole(name=self.name, roleType=createInitRoleType, rolePermissionId=0)

    def test_05(self, createInitRoleType):
        """创建的角色名与初始角色名重复"""
        response = createRole(name=param_config.initRoleName, roleType=createInitRoleType)
        assert response['msg'] == '该角色名称已存在'


class TestCreateRoleType:
    """创建角色分类"""

    def test_01(self):
        """分类名为空"""
        response = createRoleType(name=None)
        assert response['msg'] == '角色分类只支持中文、英文、数字'

    def test_02(self):
        """分类名重复(系统内置分类名：未分类角色)"""
        response = createRoleType(name='未分类角色')
        assert response['msg'] == '该角色分类名称已存在'


class TestDeleteRole:
    """删除角色"""

    def test_01(self):
        """角色id为空"""
        response = deleteRole(roleId=None)
        assert response['msg'] == '请选择角色'

    def test_02(self):
        """角色id不存在"""
        response = deleteRole(roleId=0)
        assert response['msg'] == '角色不存在，请刷新重试'

    def test_03(self, createNewRole):
        """删除角色"""
        response = deleteRole(roleId=createNewRole)
        assert response['msg'] == '操作成功'


class TestEditRole:
    """修改角色"""

    def test_01(self, createNewRoleType):
        """修改不存在的角色"""
        response = editRole(id=0, name='test%d' % int(time.time() * 1000), roleType=createNewRoleType)
        assert response['msg'] == '角色不存在，请刷新重试'

    def test_02(self, createNewRoleType):
        """角色id为空"""
        response = editRole(id=None, name=roleName, roleType=createNewRoleType)
        assert response['msg'] == '请选择需要修改的角色'

    def test_03(self, createNewRole):
        """角色分类不存在"""
        response = editRole(id=createNewRole, name=roleName, roleType=0)

    def test_04(self, createNewRole):
        """角色分类为空"""
        response = editRole(id=createNewRole, name=roleName, roleType=None)
        assert response['msg'] == '请填写角色分类名称'

    def test_05(self, createNewRole, createNewRoleType):
        """角色名为空"""
        response = editRole(id=createNewRole, name=None, roleType=createNewRoleType)
        assert response['msg'] == '角色只支持中文和英文'

    def test_06(self, createNewRole, createNewRoleType):
        """修改角色名称与初始角色名称相同"""
        response = editRole(id=createNewRole, name=param_config.initRoleName, roleType=createNewRoleType)
        assert response['msg'] == '该角色名称已存在'

    def test_07(self, createNewRole, createNewRoleType):
        """修改角色成功"""
        response = editRole(id=createNewRole, name=roleName, roleType=createNewRoleType)
