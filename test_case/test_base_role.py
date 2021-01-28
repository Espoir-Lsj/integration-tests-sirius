# __author:"zonglr"
# date:2020/11/28
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, time, jsonpath
from common import logger, request
from test_config import param_config
import test_base_permission

log = logger.Log()

NewRoleName = '一个新角色%d' % param_config.count


# 自定义方法-创建角色分类
def createRoleType(name):
    body = {
        'name': name
    }
    response = request.post_body('/role/createRoleType', body)
    return response


# 自定义方法-编辑角色分类
def updateRoleType(id, name):
    body = {
        'id': id,
        'name': name
    }
    response = request.put_body('/role/updateRoleType', body)
    return response


# 自定义方法-删除角色分类
def deleteRoleType(id):
    body = {
        'id': id
    }
    response = request.delete_body('/role/deleteRoleType', body)
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


# 自定义方法-角色数据权限
def bindDataScope(roleId, dataScope='department_data'):
    body = {
        'dataScope': dataScope,
        'roleId': roleId
    }
    response = request.put_body('/role/bindDataScope', body)
    return response


# 自定义方法-角色功能权限
def bindPermission(roleId, permissionIds):
    body = {
        'permissionIds': permissionIds,
        'roleId': roleId
    }
    response = request.put_body('/role/bindPermission', body)
    return response


# 自定义方法-绑定角色
def bindRole(userId, roleIds):
    body = {
        'roleIds': roleIds,
        'userId': userId
    }
    response = request.put_body('/role/bindRole', body)
    return response


# 创建一个新的角色分类，每个文件执行一次
@pytest.fixture(scope="module")
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


# 创建一个新的角色,使用新增的分类,每个文件执行一次
@pytest.fixture(scope="module")
def createNewRole(createNewRoleType):
    response = createRole(name=NewRoleName, roleType=createNewRoleType)
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
        if names[i] == NewRoleName:
            roleId = ids[i]
            return roleId
        i += 1


class TestBindDataScope:
    """角色数据权限"""

    def test_01(self):
        """角色id不存在"""
        response = bindDataScope(roleId=0)
        assert response['msg'] == '该角色不存在'

    def test_02(self):
        """角色id为空"""
        response = bindDataScope(roleId=None)
        assert response['msg'] == '角色id不能为空'

    def test_03(self, createNewRole):
        """权限范围为空"""
        response = bindDataScope(roleId=createNewRole, dataScope=None)
        assert response['msg'] == '请选择角色数据权限'

    def test_04(self, createNewRole):
        """权限范围不存在"""
        response = bindDataScope(roleId=createNewRole, dataScope='test')
        assert response['msg'] == '请求参数异常'

    def test_05(self, createNewRole):
        """设置成功"""
        response = bindDataScope(roleId=createNewRole)
        assert response['msg'] == '请求成功'


class TestBindPermission:
    """角色功能权限"""

    def test_01(self, createNewRole):
        """权限为空"""
        response = bindPermission(roleId=createNewRole, permissionIds=None)
        assert response['msg'] == '请选择角色功能权限'

    def test_02(self, createNewRole):
        """未选择权限"""
        response = bindPermission(roleId=createNewRole, permissionIds=[])
        assert response['msg'] == '请选择角色功能权限'

    def test_03(self, createNewRole):
        """权限id不存在"""
        response = bindPermission(roleId=createNewRole, permissionIds=[0])
        assert response['msg'] == '权限不存在'

    def test_04(self, getPermissoinIds):
        """角色id为空"""
        response = bindPermission(roleId=None, permissionIds=getPermissoinIds)
        assert response['msg'] == '请选择角色'

    def test_05(self, getPermissoinIds):
        """角色id不存在"""
        response = bindPermission(roleId=0, permissionIds=getPermissoinIds)
        assert response['msg'] == '该角色不存在'

    def test_06(self, createNewRole, getPermissoinIds):
        """设置成功"""
        response = bindPermission(roleId=createNewRole, permissionIds=getPermissoinIds)
        assert response['msg'] == '请求成功'


class TestBindRole:
    """绑定角色"""

    def test_01(self, createNewRole):
        """用户id为空"""
        response = bindRole(userId=None, roleIds=[createNewRole])
        assert response['msg'] == '请选择账号'

    def test_02(self, createNewRole):
        """用户id不存在"""
        response = bindRole(userId=0, roleIds=[createNewRole])
        assert response['msg'] == '用户不存在'

    def test_03(self, createInitUser):
        """角色id为空"""
        response = bindRole(userId=createInitUser, roleIds=None)
        assert response['msg'] == '请至少分配一个角色'

    def test_04(self, createInitUser):
        """角色id不存在"""
        response = bindRole(userId=createInitUser, roleIds=[0])
        assert response['msg'] == '该角色不存在'

    def test_05(self, createInitUser, createNewRole):
        """分配角色成功"""
        response = bindRole(userId=createInitUser, roleIds=[createNewRole])
        assert response['msg'] == '请求成功'


class TestCreateRole:
    """创建角色"""

    name = '测试角色%d' % int(time.time() * 1000)

    def test_01(self, createInitRoleType):
        """角色名为空"""
        response = createRole(name=None, roleType=createInitRoleType)
        assert response['msg'] == '角色分类只支持中文和英文'

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
        assert response['msg'] == '角色分类只支持中文和英文'

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

    def test_03(self, createNewRoleType):
        """删除角色"""
        # 新增一个临时角色，然后删除
        tempName = 'temp%d' % int(time.time() * 1000)
        response = createRole(name=tempName, roleType=createNewRoleType)
        assert response['msg'] == '请求成功'
        # 获取角色id
        roleId = response['data']
        # 删除角色
        response2 = deleteRole(roleId=roleId)
        assert response2['msg'] == '请求成功'


class TestDeleteRoleType:
    """删除角色分类"""

    def test_01(self):
        """角色分类id为空"""
        response = deleteRoleType(id=None)
        assert response['msg'] == '角色分类id不能为空'

    def test_02(self):
        """角色分类id不存在"""
        response = deleteRoleType(id=0)
        assert response['msg'] == '该角色分类不存在'

    def test_03(self):
        """删除角色分类"""
        # 新增一个临时角色分类
        tempName = 'temp%d' % int(time.time() * 1000)
        response = createRoleType(name=tempName)
        assert response['msg'] == '请求成功'
        # 获取角色分类id
        typeId = response['data']
        # 删除角色分类
        delete_response = deleteRoleType(id=typeId)
        assert delete_response['msg'] == '请求成功'


class TestEditRole:
    """修改角色"""

    def test_01(self, createNewRoleType):
        """修改不存在的角色"""
        response = editRole(id=0, name='test%d' % int(time.time() * 1000), roleType=createNewRoleType)
        assert response['msg'] == '角色不存在，请刷新重试'

    def test_02(self, createNewRoleType):
        """角色id为空"""
        response = editRole(id=None, name=NewRoleName, roleType=createNewRoleType)
        assert response['msg'] == '请选择需要修改的角色'

    def test_03(self, createNewRole):
        """角色分类不存在"""
        response = editRole(id=createNewRole, name=NewRoleName, roleType=0)
        assert response['msg'] == '该角色分类不存在'

    def test_04(self, createNewRole):
        """角色分类为空"""
        response = editRole(id=createNewRole, name=NewRoleName, roleType=None)
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
        response = editRole(id=createNewRole, name=NewRoleName, roleType=createNewRoleType)
        assert response['msg'] == '请求成功'


class TestUpdateRoleType:
    """编辑角色分类"""

    def test_01(self):
        """分类id为空"""
        response = updateRoleType(id=None, name=NewRoleName)
        assert response['msg'] == '角色分类id不能为空'

    def test_02(self):
        """分类id不存在"""
        response = updateRoleType(id=0, name=NewRoleName)
        assert response['msg'] == '该角色分类不存在'

    def test_03(self, createNewRoleType):
        """编辑分类成功"""
        response = updateRoleType(id=createNewRoleType, name=NewRoleName)
        assert response['msg'] == '请求成功'
