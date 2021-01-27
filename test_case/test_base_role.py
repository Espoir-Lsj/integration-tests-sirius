# __author:"zonglr"
# date:2020/11/28
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, time
from common import logger, request
import test_base_permission

log = logger.Log()


# 创建角色
def createRole(name, roleType,rolePermissionId=0,remark=None):
    body = {
        'name': name,
        'remark': remark,
        'rolePermissionId': rolePermissionId,
        'roleType': roleType
    }
    response = request.post_body('/role/createRole', body=body)
    return response


# 修改角色
def editRole(code, id, name, permissionIds, remark='test'):
    body = {
        'code': code,
        'id': id,
        'name': name,
        'permissionIds': permissionIds,
        'remark': remark
    }
    response = request.put_body('/role/editRole', body=body)
    return response


# 获取初始角色详情,当前py文件仅执行一次
@pytest.fixture(scope="module")
def getInitRoleDetail(createInitRole):
    # 查询初始角色的详情
    response = request.get('/role/get/%s' % createInitRole)
    assert response['msg'] == '请求成功'
    # 获取信息内容
    initCode = response['data']['code']
    initName = response['data']['name']
    initIsEnabled = response['data']['isEnabled']
    return initCode, initName, initIsEnabled


class TestCreate:
    """创建角色"""
    url = '/role/createRole'
    num = int(time.time() * 1000)
    code = 'code%d' % num
    name = '测试角色%d' % num

    def test_01(self, getPermissoinIds):
        """角色编码为空"""
        response = createRole(code=None, name=self.name, permissionIds=getPermissoinIds)
        assert response['msg'] == '请填写角色编码'

    def test_02(self, getPermissoinIds):
        """角色名为空"""
        response = createRole(code=self.code, name=None, permissionIds=getPermissoinIds)
        assert response['msg'] == '请填写角色名称'

    def test_03(self, getPermissoinIds):
        """权限id为空"""
        response = createRole(code=self.code, name=self.name, permissionIds=None)
        assert response['msg'] == '请选择角色需要关联的权限'

    def test_04(self, getPermissoinIds):
        """角色编码重复"""
        # 创建一个角色编码和角色名称为test的角色
        response = createRole(code='test', name='test', permissionIds=getPermissoinIds)
        assert response['msg'] == '角色编码已被使用'

    def test_05(self):
        """权限id不存在"""
        response = createRole(code=self.code, name=self.name, permissionIds=[0])
        assert response['msg'] == '请选择正确的权限'


class TestEditRole:
    """修改角色"""
    url = '/role/editRole'
    num = int(time.time() * 1000)
    code = 'code%d' % num
    name = '测试角色%d' % num

    def test_01(self, getPermissoinIds):
        """修改不存在的角色"""
        response = editRole(code=self.code, id=0, name=self.name, permissionIds=getPermissoinIds)
        assert response['msg'] == '角色不存在，请刷新重试'

    def test_02(self, createInitRole, getInitRoleDetail, getPermissoinIds):
        """修改存在的角色"""
        # 修改角色权限，取权限列表中第一个值
        edit_response = editRole(code=getInitRoleDetail[0], id=createInitRole, name=getInitRoleDetail[1],
                                 permissionIds=getPermissoinIds[0:1])
        assert edit_response['msg'] == '请求成功'
        # 修改角色权限为全部权限
        edit_response2 = editRole(code=getInitRoleDetail[0], id=createInitRole, name=getInitRoleDetail[1],
                                  permissionIds=getPermissoinIds)
        assert edit_response2['msg'] == '请求成功'

    def test_03(self, getPermissoinIds):
        """修改角色编码重复"""
        # 查询管理员角色id
        list = request.get('/role/list?pageNum=0&pageSize=50&name=管理')
        assert list['data']['totalCount'] > 0
        roleId = list['data']['rows'][0]['id']
        # 修改角色编码为测试用编码
        edit_response = editRole(code='test', id=roleId, name='test', permissionIds=getPermissoinIds)
        assert edit_response['msg'] == '角色编码已被使用'


class TestGetDetail:
    """获取角色详情"""
    url = '/role/get/{id}'

    def test_01(self):
        """角色id不存在"""
        response = request.get(self.url.format(id=0))
        assert response['msg'] == '角色不存在'

    def test_02(self, createInitRole):
        """角色id存在"""
        # 查询角色详情
        response = request.get(self.url.format(id=createInitRole))
        assert response['msg'] == '请求成功'


class TestList:
    """角色列表"""
    url = '/role/list'

    @pytest.mark.parametrize('isEnable', [True, False])
    @pytest.mark.parametrize('name', ['test', '%%'])
    def test_01(self, isEnable, name):
        """查询已启用的角色"""
        response = request.get('/role/list?pageNum=0&pageSize=50&isEnable=%s&name=%s' % (isEnable, name))
        assert response['msg'] == '请求成功'


class TestSetEnable:
    """启用禁用角色"""
    url = '/role/setEnable'

    def test_01(self):
        """启用角色id不存在"""
        body = {
            'id': 0,
            'isEnabled': True
        }
        response = request.put_body(self.url, body=body)
        assert response['msg'] == '角色不存在'

    def test_02(self):
        """禁用角色id不存在"""
        body = {
            'id': 0,
            'isEnabled': False
        }
        response = request.put_body(self.url, body=body)
        assert response['msg'] == '角色不存在'

    def test_03(self):
        """角色id为空"""
        body = {
            'id': None,
            'isEnabled': True
        }
        response = request.put_body(self.url, body=body)
        assert response['msg'] == '请选择角色'

    def test_04(self, createInitRole, getInitRoleDetail):
        """启用禁用角色"""
        # 查询初始角色详情
        isEabled = getInitRoleDetail[2]
        # 如果状态为已禁用则启用角色
        if isEabled == False:
            response = request.put_body(self.url, body={'id': createInitRole, 'isEnabled': True})
            assert response['msg'] == '请求成功'
            # 重复启用
            response2 = request.put_body(self.url, body={'id': createInitRole, 'isEnabled': True})
            assert response2['msg'] == '请求成功'
            # 禁用角色
            response3 = request.put_body(self.url, body={'id': createInitRole, 'isEnabled': False})
            assert response3['msg'] == '请求成功'
            # 重复禁用
            response4 = request.put_body(self.url, body={'id': createInitRole, 'isEnabled': False})
            assert response4['msg'] == '请求成功'
        else:
            response = request.put_body(self.url, body={'id': createInitRole, 'isEnabled': False})
            assert response['msg'] == '请求成功'
            # 重复启用
            response2 = request.put_body(self.url, body={'id': createInitRole, 'isEnabled': False})
            assert response2['msg'] == '请求成功'
            # 禁用角色
            response3 = request.put_body(self.url, body={'id': createInitRole, 'isEnabled': True})
            assert response3['msg'] == '请求成功'
            # 重复禁用
            response4 = request.put_body(self.url, body={'id': createInitRole, 'isEnabled': True})
            assert response4['msg'] == '请求成功'
