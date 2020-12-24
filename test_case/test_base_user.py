# __author:"zonglr"
# date:2020/11/28
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, time
from common import logger, request
from test_config import param_config

log = logger.Log()


# 新增用户
def createUser(name, loginName, roleIds, email=None, img=None, remark=None, type=None):
    body = {
        'email': email,
        'loginName': loginName,
        'name': name,
        'profileImg': img,
        'remark': remark,
        'roleIds': roleIds,
        'userType': type
    }
    response = request.post_body('/user/createUser', body=body)
    return response


# 修改用户
def editUser(name, id, loginName, roleIds, email=None, img=None, remark=None, type=None):
    body = {
        'email': email,
        'id': id,
        'loginName': loginName,
        'name': name,
        'profileImg': img,
        'remark': remark,
        'roleIds': roleIds,
        'userType': type
    }
    response = request.put_body('/user/editUser', body=body)
    return response


# 根据角色查询用户信息
def userListByRoleId(roleId, isEnabled='true', loginName=None, name=None, ownerRole='true', pageNum=0, pageSize=20):
    params = {
        'isEnabled': isEnabled,  # 用户是否启用
        'loginName': loginName,  # 登录账号
        'name': name,  # 用户名称
        'ownerRole': ownerRole,  # 查询的用户是否属于该角色
        'roleId': roleId,
        'pageNum': pageNum,
        'pageSize': pageSize,
        # 'sortList[0].desc': 'true'
    }
    response = request.get_params('/user/userListByRoleId', params=params)
    return response


# 获取当前登录用户的id,当前py文件仅执行一次
@pytest.fixture(scope="module")
def getCurrentUserId():
    # 查询当前登录用户的id
    response = request.get('/user/currentUser')
    assert response['msg'] == '请求成功'
    userId = response['data']['id']
    return userId


class TestCreateUser:
    """创建用户"""
    url = '/user/createUser'

    num = int(time.time() * 1000)
    userName = '测试用户%d' % num
    loginName = 'test%d' % num

    def test_01(self, createInitRole):
        """姓名为空"""
        response = createUser(name=None, loginName=self.loginName, roleIds=[createInitRole])
        assert response['msg'] == '请填写用户名称'

    def test_02(self, createInitRole):
        """登录名为空"""
        response = createUser(name=self.userName, loginName=None, roleIds=[createInitRole])
        assert response['msg'] == '请填写登录名'

    def test_03(self):
        """角色为空"""
        response = createUser(name=self.userName, loginName=self.loginName, roleIds=None)
        assert response['msg'] == '请选择用户关联的角色'

    def test_04(self):
        """角色id不存在"""
        response = createUser(name=self.userName, loginName=self.loginName, roleIds=[0])
        assert response['msg'] == '角色不存在'

    def test_05(self, createInitRole):
        """登录名重复"""
        response = createUser(name=self.userName, loginName='test', roleIds=[createInitRole])
        assert response['msg'] == '登录名已存在'


class TestEditPwd:
    """修改登录密码"""
    url = '/user/editPassword'

    def test_01(self):
        """新密码为空"""
        body = {
            'newPassword': None,
            'oldPassword': '123456'
        }
        response = request.put_body(self.url, body=body)
        assert response['msg'] == '请输入新密码'

    def test_02(self):
        """旧密码为空"""
        body = {
            'newPassword': '123456',
            'oldPassword': None
        }
        response = request.put_body(self.url, body=body)
        assert response['msg'] == '请输入旧密码'

    def test_03(self):
        """新密码长度少于8位"""
        body = {
            'newPassword': 'Aa8888^',
            'oldPassword': param_config.loginPassword
        }
        response = request.put_body(self.url, body=body)
        log.info(response)
        assert response['msg'] == '密码长度8~16位，包含数字、大写、小写字母、特殊符号中的至少3种'

    def test_04(self):
        """新密码为8位纯数字"""
        body = {
            'newPassword': '88888888',
            'oldPassword': param_config.loginPassword
        }
        response = request.put_body(self.url, body=body)
        log.info(response)
        assert response['msg'] == '密码需包含数字、大写、小写字母、特殊符号中的至少3种'

    def test_05(self):
        """旧密码不正确"""
        body = {
            'newPassword': '88888888',
            'oldPassword': '0000'
        }
        response = request.put_body(self.url, body=body)
        log.info(response)
        assert response['msg'] == '旧密码不正确'

    def test_06(self):
        """新旧密码一致"""
        body = {
            'newPassword': param_config.loginPassword,
            'oldPassword': param_config.loginPassword
        }
        response = request.put_body(self.url, body=body)
        log.info(response)
        assert response['msg'] == '新密码和旧密码一致; 请重新输入新密码'


class TestEditUser:
    """修改用户"""
    url = '/user/editUser'

    num = int(time.time() * 1000)
    userName = '测试用户%d' % num
    loginName = 'test%d' % num

    def test_01(self, createInitRole):
        """用户id不存在"""
        response = editUser(name=self.userName, id=0, loginName=self.loginName, roleIds=[createInitRole])
        assert response['msg'] == '用户不存在，请检查重试'

    def test_02(self, createInitUser):
        """修改初始用户"""
        # 查询初始用户的信息
        response = request.get('/user/userDetail/{userId}'.format(userId=createInitUser))
        # 判断查询出的id,与初始用户id一致
        assert response['data']['id'] == createInitUser
        # 获取信息内容
        initId = response['data']['id']
        initRoleIds = response['data']['roleIds']
        initLoginName = response['data']['loginName']
        initName = response['data']['name']
        # 修改用户
        response = editUser(name=initName, id=initId, loginName=initLoginName, roleIds=initRoleIds)
        assert response['msg'] == '请求成功'


class TestList:
    """查询用户列表"""
    url = '/user/list'

    def test_01(self):
        """查询已启用/禁用用户"""
        response = request.get(self.url + '?pageNum=0&pageSize=50&isEnabled=true')
        # 判断查出出的数据，状态是否都是已启用
        for i in response['data']['rows']:
            assert i['isEnabled'] == True
        response2 = request.get(self.url + '?pageNum=0&pageSize=50&isEnabled=false')
        # 判断查出出的数据，状态是否都是已禁用
        for j in response2['data']['rows']:
            assert j['isEnabled'] == False

    def test_02(self):
        """查询结果为空的情况"""
        response = request.get(self.url + '?pageNum=0&pageSize=50&isEnabled=true&loginName=--')
        # totalCount=0
        assert response['data']['totalCount'] == 0


class TestResetPassword:
    """重置用户密码"""
    url = '/user/restPassword'

    def test_01(self):
        """用户id不存在"""
        response = request.put_body(self.url, body={'userId': 0})
        assert response['msg'] == '用户不存在'

    def test_02(self):
        """用户id为空"""
        response = request.put_body(self.url, body={'userId': None})
        assert response['msg'] == '请选择用户'

    def test_03(self, createInitUser):
        """正确的用户id"""
        # 重置初始用户的密码
        response = request.put_body(self.url, body={'userId': createInitUser})
        assert response['msg'] == '请求成功'

    def test_04(self, getCurrentUserId):
        """重置当前登录用户的密码"""
        response = request.put_body(self.url, body={'userId': getCurrentUserId})
        log.info(response)
        assert response['msg'] == '不允许重置自己的密码'


class TestSetEnable:
    """启用禁用用户"""
    url = '/user/setEnable'

    def test_01(self):
        """启用用户id不存在"""
        body = {
            'id': 0,
            'isEnabled': True
        }
        response = request.put_body(self.url, body=body)
        assert response['msg'] == '用户不存在'

    def test_02(self):
        """禁用用户id不存在"""
        body = {
            'id': 0,
            'isEnabled': False
        }
        response = request.put_body(self.url, body=body)
        assert response['msg'] == '用户不存在'

    def test_03(self):
        """用户id为空"""
        body = {
            'id': None,
            'isEnabled': True
        }
        response = request.put_body(self.url, body=body)
        assert response['msg'] == '请选择用户'

    def test_04(self, createInitUser):
        """启用禁用"""
        # 查询初始用户状态
        list = request.get('/user/list?pageNum=0&pageSize=50&name=test')
        assert list['data']['totalCount'] > 0
        isEabled = list['data']['rows'][0]['isEnabled']
        # 如果状态为已禁用则启用
        if isEabled == True:
            response = request.put_body(self.url, body={'id': createInitUser, 'isEnabled': True})
            assert response['msg'] == '请求成功'
            # 重复启用
            response2 = request.put_body(self.url, body={'id': createInitUser, 'isEnabled': True})
            assert response2['msg'] == '请求成功'
        else:
            # 如果状态为已启用则禁用
            response = request.put_body(self.url, body={'id': createInitUser, 'isEnabled': False})
            assert response['msg'] == '请求成功'
            # 重复禁用
            response2 = request.put_body(self.url, body={'id': createInitUser, 'isEnabled': True})
            assert response2['msg'] == '请求成功'

    def test_05(self, getCurrentUserId):
        """禁用当前登录用户"""
        body = {
            'id': getCurrentUserId,
            'isEnabled': False
        }
        response = request.put_body(self.url, body=body)
        log.info(response)
        assert response['msg'] == '不允许启用或者禁用自己的账号'


class TestUserBindRole:
    """用户绑定角色"""
    url = '/user/userBindRole'

    def test_01(self, createInitUser):
        """角色id不存在"""
        params = [
            {
                'roleId': 0,
                'userId': createInitUser
            }
        ]
        response = request.post_body(self.url, body=params)
        assert response['msg'] == '角色不存在'

    def test_02(self, createInitRole):
        """用户id不存在"""
        params = [
            {
                'roleId': createInitRole,
                'userId': 0
            }
        ]
        response = request.post_body(self.url, body=params)
        assert response['msg'] == '用户不存在'

    def test_03(self, createInitRole, createInitUser):
        """正确的用户和角色id"""
        params = [
            {
                'roleId': createInitRole,
                'userId': createInitUser
            }
        ]
        response = request.post_body(self.url, body=params)
        assert response['msg'] == '请求成功'


class TestUserDetail:
    """获取用户详情"""
    url = '/user/userDetail/{userId}'

    def test_01(self):
        """不存在的用户id"""
        response = request.get(self.url.format(userId=0))
        log.info(response)
        assert response['msg'] == '用户不存在'

    def test_02(self):
        """用户id为空"""
        response = request.get(self.url.format(userId=None))
        log.info(response)
        assert response['msg'] == '请求参数异常'


class TestUserListByRoleId:
    """根据角色查询用户信息"""
    url = '/user/userListByRoleId'

    def test_01(self):
        """角色id不存在"""
        response = userListByRoleId(roleId=0)
        log.info(response)
        assert response['msg'] == '请求成功'

    def test_02(self, createInitRole):
        """初始角色id"""
        response = userListByRoleId(roleId=createInitRole)
        log.info(response)
        assert response['msg'] == '请求成功'


class TestUserUnbindRole:
    """用户解绑角色"""
    url = '/user/userUnbindRole'

    def test_01(self, createInitUser):
        """角色id不存在"""
        params = [
            {
                'roleId': 0,
                'userId': createInitUser
            }
        ]
        response = request.post_body(self.url, body=params)
        assert response['msg'] == '角色不存在'

    def test_02(self, createInitRole):
        """用户id不存在"""
        params = [
            {
                'roleId': createInitRole,
                'userId': 0
            }
        ]
        response = request.post_body(self.url, body=params)
        assert response['msg'] == '用户不存在'

    def test_03(self, createInitRole, createInitUser):
        """正确的用户和角色id"""
        params = [
            {
                'roleId': createInitRole,
                'userId': createInitUser
            }
        ]
        response = request.post_body(self.url, body=params)
        assert response['msg'] == '请求成功'
