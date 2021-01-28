# __author:"zonglr"
# date:2020/11/28
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, time, jsonpath
from common import logger, request
from test_config import param_config
from test_base_department import enableDept
from faker import Faker

faker = Faker(locale='zh_CN')

log = logger.Log()

loginName = 'NeW%d' % param_config.count


# 新增用户
def createUser(loginName, initialPassword, departmentId, code=None, email=faker.safe_email(), gender=None, manager=None,
               name=faker.name(), phone=faker.phone_number(), remark=None, title=None):
    body = {
        'code': code,  # 员工编号
        'departmentId': departmentId,  # 所属部门id
        'email': email,  # 用户邮箱
        'gender': gender,  # 性别
        'initialPassword': initialPassword,  # 初始密码
        'loginName': loginName,  # 登录名
        'manager': manager,  # 主管
        'name': name,  # 真实姓名
        'phone': phone,  # 手机号
        'remark': remark,  # 备注
        'title': title  # 职位
    }
    response = request.post_body('/user/createUser', body=body)
    return response


# 修改用户
def editUser(loginName, departmentId, id, code=None, email=faker.safe_email(), gender=None, manager=None,
             name=faker.name(), phone=faker.phone_number(), remark=None, title=None):
    body = {
        'code': code,  # 员工编号
        'departmentId': departmentId,  # 所属部门
        'email': email,  # 邮箱
        'gender': gender,  # 性别
        'id': id,  # 用户id
        'loginName': loginName,  # 用户名
        'manager': manager,  # 主管
        'name': name,  # 真实姓名
        'phone': phone,  # 手机号
        'remark': remark,  # 备注
        'title': title  # 职位
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


# 新增一个新的用户，(便于编辑和删除使用)
@pytest.fixture(scope="module")
def createNewUser(createInitDepartment):
    # 账号名称
    Name = loginName
    # 密码
    initialPassword = param_config.initialPassword
    # 启用默认部门
    response2 = enableDept(id=createInitDepartment, isEnabled=True)
    response = createUser(loginName=Name, initialPassword=initialPassword, departmentId=createInitDepartment)
    assert response['msg'] in ('请求成功', '登录名已存在')
    # 根据departmentId查询初始用户的id
    list = request.get('/user/list?pageNum=0&pageSize=50&departmentId=%s' % createInitDepartment)
    assert list['data']['totalCount'] > 0
    # 查询返回的所有账号名
    names = jsonpath.jsonpath(list, '$..loginName')
    # 获取账号id
    ids = jsonpath.jsonpath(list, '$..id')
    # 根据账号名获取到账号id
    i = 0
    while i < len(names):
        if names[i] == Name:
            id = ids[i]
            return id
        i += 1


# 获取当前登录用户的id,当前py文件仅执行一次
@pytest.fixture(scope="module")
def getCurrentUserId():
    # 查询当前登录用户的id
    response = request.get('/user/currentUser')
    assert response['msg'] == '请求成功'
    userId = response['data']['id']
    return userId


# 获取初始用户详情,当前py文件仅执行一次
@pytest.fixture(scope="module")
def getInitUserDetail(createInitUser):
    # 查询初始用户的信息
    response = request.get('/user/userDetail/{userId}'.format(userId=createInitUser))
    # 判断查询出的id,与初始用户id一致
    assert response['data']['id'] == createInitUser
    # 获取信息内容
    initName = response['data']['name']
    initLoginName = response['data']['loginName']
    initRoleIds = response['data']['roleIds']
    initIsEnabled = response['data']['isEnabled']
    return initName, initLoginName, initRoleIds, initIsEnabled


class TestCreateUser:
    """创建用户"""

    def test_01(self, createInitDepartment):
        """用户名为空"""
        response = createUser(loginName=None, initialPassword=param_config.initialPassword,
                              departmentId=createInitDepartment)
        assert response['msg'] == '账号只支持英文、数字'

    def test_02(self, createInitDepartment):
        """密码为空"""
        response = createUser(loginName=loginName, initialPassword=None, departmentId=createInitDepartment)
        assert response['msg'] == '请填写初始密码'

    def test_03(self):
        """部门为空"""
        response = createUser(loginName=loginName, initialPassword=param_config.initialPassword, departmentId=None)
        assert response['msg'] == '请选择所属部门'

    def test_04(self, createInitUser, createInitDepartment):
        """用户名重复"""
        response = createUser(loginName=createInitUser, initialPassword=param_config.initialPassword,
                              departmentId=createInitDepartment)
        assert response['msg'] == '登录名已存在'

    def test_05(self, createInitDepartment):
        """部门被禁用"""
        # 禁用默认部门
        response = enableDept(id=createInitDepartment, isEnabled=False)
        response2 = createUser(loginName=loginName, initialPassword=param_config.initialPassword,
                               departmentId=createInitDepartment)
        assert response2['msg'] == '您的部门被禁用，请联系管理员'

    def test_06(self, createInitDepartment):
        """密码输入规则（大写字母，小写字母，数字，常用特殊字符这4中缺2）"""
        response = createUser(loginName=loginName, initialPassword='aa888888', departmentId=createInitDepartment)
        assert response['msg'] == '密码需包含数字、大写、小写字母、特殊符号中的至少3种'

    def test_07(self, createInitDepartment):
        """密码小于6位或大于20位"""
        response = createUser(loginName=loginName, initialPassword='12345', departmentId=createInitDepartment)
        assert response['msg'] == '密码长度为6-20之间'

    def test_08(self, createInitDepartment):
        """手机号格式错误"""
        response = createUser(loginName=loginName, initialPassword=param_config.initialPassword,
                              departmentId=createInitDepartment, phone=123)
        assert response['msg'] == '请输入正确的手机号码'

    def test_09(self, createInitDepartment):
        """邮箱格式错误"""
        response = createUser(loginName=loginName, initialPassword=param_config.initialPassword,
                              departmentId=createInitDepartment, email=123)
        assert response['msg'] == '请输入正确的邮箱'

    def test_10(self):
        """部门不存在"""
        response = createUser(loginName=loginName, initialPassword=param_config.initialPassword, departmentId=9999)
        assert response['msg'] == '未找到该部门'

    def test_11(self, createInitDepartment):
        """账号输入汉字（只支持字母、数字）"""
        response = createUser(loginName='苏勇', initialPassword=param_config.initialPassword,
                              departmentId=createInitDepartment)
        assert response['msg'] == '账号只支持英文、数字'


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
        assert response['msg'] == '密码长度8~16位，包含数字、大写、小写字母、特殊符号中的至少3种'

    def test_04(self):
        """新密码为8位纯数字"""
        body = {
            'newPassword': '88888888',
            'oldPassword': param_config.loginPassword
        }
        response = request.put_body(self.url, body=body)
        assert response['msg'] == '密码需包含数字、大写、小写字母、特殊符号中的至少3种'

    def test_05(self):
        """旧密码不正确"""
        body = {
            'newPassword': '88888888',
            'oldPassword': '0000'
        }
        response = request.put_body(self.url, body=body)
        assert response['msg'] == '旧密码不正确'

    def test_06(self):
        """新旧密码一致"""
        body = {
            'newPassword': param_config.loginPassword,
            'oldPassword': param_config.loginPassword
        }
        response = request.put_body(self.url, body=body)
        assert response['msg'] == '新密码和旧密码一致; 请重新输入新密码'


class TestEditUser:
    """修改用户"""

    def test_01(self, createInitDepartment, createNewUser):
        """编辑成功"""
        response = editUser(loginName=loginName, departmentId=createInitDepartment, id=createNewUser)
        assert response['msg'] == '请求成功'

    def test_02(self, createInitDepartment, createNewUser):
        """用户名重复"""
        response = editUser(loginName=param_config.initLoginName, departmentId=createInitDepartment, id=createNewUser)
        assert response['msg'] == '登录名已存在'

    def test_03(self, createInitDepartment, createNewUser):
        """用户名为空"""
        response = editUser(loginName=None, departmentId=createInitDepartment, id=createNewUser)
        assert response['msg'] == '账号只支持英文、数字'

    def test_04(self, createNewUser):
        """部门不存在"""
        response = editUser(loginName=loginName, departmentId=99999, id=createNewUser)
        assert response['msg'] == '未找到该部门'

    def test_05(self, createNewUser):
        """部门为空"""
        response = editUser(loginName=loginName, departmentId=None, id=createNewUser)
        assert response['msg'] == '请选择所属部门'

    def test_06(self, createInitDepartment):
        """用户不存在"""
        response = editUser(loginName=loginName, departmentId=createInitDepartment, id=99999)
        assert response['msg'] == '用户不存在，请检查重试'

    def test_07(self, createInitDepartment):
        """用户为空"""
        response = editUser(loginName=loginName, departmentId=createInitDepartment, id=None)
        assert response['msg'] == '请输入用户id'

    def test_08(self, createInitDepartment, createNewUser):
        """手机号错误"""
        response = editUser(loginName=loginName, departmentId=createInitDepartment, id=createNewUser,phone=123)
        assert response['msg'] == '请输入正确的手机号码'

    def test_09(self, createInitDepartment, createNewUser):
        """邮箱错误"""
        response = editUser(loginName=loginName, departmentId=createInitDepartment, id=createNewUser,email=123)
        assert response['msg'] == '请输入正确的邮箱'


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

    def test_04(self, createInitUser, getInitUserDetail):
        """启用禁用"""
        # 查询初始用户状态
        isEabled = getInitUserDetail[3]
        # 如果状态为已禁用则启用
        if isEabled == True:
            response = request.put_body(self.url, body={'id': createInitUser, 'isEnabled': True})
            assert response['msg'] == '请求成功'
            # 重复启用
            response2 = request.put_body(self.url, body={'id': createInitUser, 'isEnabled': True})
            assert response2['msg'] == '请求成功'
            # 如果状态为已启用则禁用
            response3 = request.put_body(self.url, body={'id': createInitUser, 'isEnabled': False})
            assert response3['msg'] == '请求成功'
            # 重复禁用
            response4 = request.put_body(self.url, body={'id': createInitUser, 'isEnabled': False})
            assert response4['msg'] == '请求成功'
        else:
            response = request.put_body(self.url, body={'id': createInitUser, 'isEnabled': False})
            assert response['msg'] == '请求成功'
            # 重复启用
            response2 = request.put_body(self.url, body={'id': createInitUser, 'isEnabled': False})
            assert response2['msg'] == '请求成功'
            # 如果状态为已启用则禁用
            response3 = request.put_body(self.url, body={'id': createInitUser, 'isEnabled': True})
            assert response3['msg'] == '请求成功'
            # 重复禁用
            response4 = request.put_body(self.url, body={'id': createInitUser, 'isEnabled': True})
            assert response4['msg'] == '请求成功'

    def test_05(self, getCurrentUserId):
        """禁用当前登录用户"""
        body = {
            'id': getCurrentUserId,
            'isEnabled': False
        }
        response = request.put_body(self.url, body=body)
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
        assert response['msg'] == '用户不存在'

    def test_02(self):
        """用户id为空"""
        response = request.get(self.url.format(userId=None))
        assert response['msg'] == '请求参数异常'


class TestUserListByRoleId:
    """根据角色查询用户信息"""
    url = '/user/userListByRoleId'

    def test_01(self):
        """角色id不存在"""
        response = userListByRoleId(roleId=0)
        assert response['msg'] == '请求成功'

    def test_02(self, createInitRole):
        """初始角色id"""
        response = userListByRoleId(roleId=createInitRole)
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
        # 解绑
        params = [
            {
                'roleId': createInitRole,
                'userId': createInitUser
            }
        ]
        response = request.post_body(self.url, body=params)
        assert response['msg'] == '请求成功'
