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


class TestCurrentUser:
    """获取当前登录用户信息"""
    url = '/user/currentUser'

    def test_01(self):
        response = request.get(self.url)
        assert response['msg'] == '请求成功'


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
        """按姓名查询"""
        response = request.get(self.url + '?pageNum=0&pageSize=50&name=test')
        # 根据返回结果判断，列表中是否存在姓名为test（初始用户名）的用户
        for i in response['data']['rows']:
            assert 'test' in i['name']


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
        response2 = request.put_body(self.url, body={'userId': createInitUser})
        assert response2['msg'] == '请求成功'


class TestEnable:
    """启用/禁用用户"""
    url = '/role/list'

    @pytest.mark.parametrize('isEnable', [True, False])
    @pytest.mark.parametrize('name', ['test', '%%'])
    def test_01(self, isEnable, name):
        """查询已启用的角色"""
        response = request.get('/role/list?pageNum=0&pageSize=50&isEnable=%s&name=%s' % (isEnable, name))
        assert response['msg'] == '请求成功'


class TestSetEnable:
    """启用禁用角色"""
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
        assert response['msg'] == '用户不存在'

    def test_02(self):
        """用户id为空"""
        response = request.get(self.url.format(userId=None))
        assert response['msg'] == '请求参数异常'
