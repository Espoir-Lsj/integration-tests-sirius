# __author:"zonglr"
# date:2020/11/28
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, time, jsonpath
from common import logger, request
from test_config import param_config
from faker import Faker

faker = Faker(locale='zh_CN')
log = logger.Log()
# 新部门名称
departmentName = '一个新部门%d' % param_config.count


# 创建部门
def createDept(departmentName, departmentTypeId, parentId, sort='1', isEnabled=True, director=None,
               phone=faker.phone_number(), remark=None):
    body = {
        'departmentName': departmentName,  # 部门名称
        'departmentTypeId': departmentTypeId,  # 分类
        'director': director,  # 负责人
        'isEnabled': isEnabled,  # 部门状态
        'parentId': parentId,  # 上级部门
        'phone': phone,  # 手机号
        'remark': remark,  # 备注
        'sort': sort  # 排序
    }
    response = request.post_body('/department/create', body=body)
    return response


# 编辑部门
def updateDept(departmentName, departmentTypeId, id, parentId, sort='1', isEnabled=True, director=None,
               phone=faker.phone_number(), remark=None):
    body = {
        'departmentName': departmentName,  # 部门名称
        'departmentTypeId': departmentTypeId,  # 分类
        'director': director,  # 负责人
        'id': id,  # 部门id
        'isEnabled': isEnabled,  # 部门状态
        'parentId': parentId,  # 上级部门
        'phone': phone,  # 手机号
        'remark': remark,  # 备注
        'sort': sort  # 排序
    }
    response = request.put_body('/department/update', body=body)
    return response


# 启用禁用部门
def enableDept(id, isEnabled):
    body = {
        "id": id,
        "isEnabled": isEnabled
    }
    response = request.put_body('/department/setEnable', body=body)
    return response


# 获取部门id,当前py文件仅执行一次
@pytest.fixture(scope="module")
def parentId():
    detail = request.get('/department/findDepartment')
    departmentId = detail['data'][0]['id']
    return departmentId


# 获取字典部门分类id,当前py文件仅执行一次
@pytest.fixture(scope="module")
def getByTypeId():
    detail = request.get('/dictionary/getByType/department_type')
    id = detail['data'][0]['id']
    return id


# 循环获取顶级部门id
@pytest.fixture(scope="module")
def topLevelId():
    list = request.get('/department/findDepartment')
    assert len(list['data']) > 0
    # 查询返回结果中部门id的值
    for i in list['data']:
        if i['parentId'] == None:
            deptId = i['id']
            return deptId


# 新增一个新的部门(便于编辑和删除使用)
@pytest.fixture(scope="module")
def createNewDepartment(getByTypeId, parentId):
    deptName = '一个新仓库%d' % param_config.count
    response = createDept(departmentName=deptName, departmentTypeId=getByTypeId, parentId=parentId)
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


class TestCreateDept:
    """新增部门"""

    def test_01(self, getByTypeId, parentId):
        """部门名称为空"""
        response = createDept(departmentName=None, departmentTypeId=getByTypeId, parentId=parentId)
        assert response['msg'] == '请输入部门名称'

    def test_02(self, parentId):
        """分类为空"""
        response = createDept(departmentName=departmentName, departmentTypeId=None, parentId=parentId)
        assert response['msg'] == '请选择分类'

    def test_03(self, getByTypeId):
        """上级部门为空"""
        response = createDept(departmentName=departmentName, departmentTypeId=getByTypeId, parentId=None)
        assert response['msg'] == '请输入上级部门'

    def test_04(self, getByTypeId, parentId):
        """排序为空"""
        response = createDept(departmentName=departmentName, departmentTypeId=getByTypeId, parentId=parentId, sort=None)
        assert response['msg'] == '请选择显示排序'

    def test_05(self, getByTypeId, parentId):
        """状态为空"""
        response = createDept(departmentName=departmentName, departmentTypeId=getByTypeId, parentId=parentId,
                              isEnabled=None)
        assert response['msg'] == '请选择部门状态'

    def test_06(self, getByTypeId, parentId):
        """部门名称重复"""
        response = createDept(departmentName=param_config.initDeptName, departmentTypeId=getByTypeId,
                              parentId=parentId)
        assert response['msg'] == '部门已存在'

    def test_07(self, parentId):
        """分类不存在"""
        response = createDept(departmentName=departmentName, departmentTypeId=9999, parentId=parentId)
        assert response['msg'] in('部门类型不存在','部门已存在')

    def test_08(self, parentId):
        """手机号错误"""
        response = createDept(departmentName=departmentName, departmentTypeId=9999, parentId=parentId, phone=123)
        assert response['msg'] == '请输入正确的手机号码'


class TestUpdateDept:
    """编辑部门"""

    def test_01(self, getByTypeId, createNewDepartment, parentId):
        """编辑部门成功"""
        response = updateDept(departmentName=departmentName, departmentTypeId=getByTypeId,
                              id=createNewDepartment, parentId=parentId)
        assert response['msg'] in ('请求成功','部门已存在')

    def test_02(self, getByTypeId, parentId):
        """编辑部门为空"""
        response = updateDept(departmentName=departmentName, departmentTypeId=getByTypeId,
                              id=None, parentId=parentId)
        assert response['msg'] == '部门id不能为空'

    def test_03(self, getByTypeId, createNewDepartment):
        """编辑上级部门为空"""
        response = updateDept(departmentName=departmentName, departmentTypeId=getByTypeId,
                              id=createNewDepartment, parentId=None)
        assert response['msg'] == '上级部门不存在'

    def test_04(self, getByTypeId, createNewDepartment, parentId):
        """编辑部门名称为空"""
        response = updateDept(departmentName=None, departmentTypeId=getByTypeId,
                              id=createNewDepartment, parentId=parentId)
        assert response['msg'] == '请输入部门名称'

    def test_05(self, createNewDepartment, parentId):
        """编辑分类为空"""
        response = updateDept(departmentName=departmentName, departmentTypeId=None,
                              id=createNewDepartment, parentId=parentId)
        assert response['msg'] == '请选择分类'

    def test_06(self, createNewDepartment, parentId):
        """编辑分类不存在"""
        response = updateDept(departmentName=departmentName, departmentTypeId=9999,
                              id=createNewDepartment, parentId=parentId)
        assert response['msg'] in( '部门类型不存在','部门已存在')

    # @pytest.mark.skip('排序是必填项，为空编辑成功')  # TODO
    def test_07(self, createNewDepartment, getByTypeId, parentId):
        """编辑排序为空"""
        response = updateDept(departmentName=departmentName, departmentTypeId=getByTypeId,
                              id=createNewDepartment, parentId=parentId, sort=None)
        assert response['msg'] == '请选择显示排序'

    def test_08(self, createNewDepartment, getByTypeId, parentId):
        """编辑状态为空"""
        response = updateDept(departmentName=departmentName, departmentTypeId=getByTypeId,
                              id=createNewDepartment, parentId=parentId, isEnabled=None)
        assert response['msg'] == '请选择部门状态'

    def test_09(self, createNewDepartment, getByTypeId, parentId):
        """编辑部门名称已存在"""
        response = updateDept(departmentName=param_config.initDeptName, departmentTypeId=getByTypeId,
                              id=createNewDepartment, parentId=parentId)
        assert response['msg'] == '部门已存在'

    def test_10(self, createNewDepartment, getByTypeId, parentId):
        """编辑手机号错误"""
        response = updateDept(departmentName=departmentName, departmentTypeId=getByTypeId,
                              id=createNewDepartment, parentId=parentId, phone=123)
        assert response['msg'] == '请输入正确的手机号码'


class TestSetEnable:
    """启用/禁用部门"""

    def test_01(self):
        """部门id为空"""
        response = enableDept(id=None, isEnabled=False)
        assert response['msg'] == '请选择部门'

    def test_02(self):
        """部门id不存在"""
        response = enableDept(id=9999, isEnabled=False)
        assert response['msg'] == '该部门不存在'

    def test_03(self, createNewDepartment):
        """启用禁用为空"""
        response = enableDept(id=createNewDepartment, isEnabled=None)
        assert response['msg'] == '请选择启用或者禁用的部门'

    def test_04(self, createNewDepartment):
        """启用禁用部门交互"""
        # 获取新部门详情的启用禁用状态
        response = request.get('/department/getDetail/%d' % createNewDepartment)
        isEnabled = response['data']['isEnabled']
        # 如果部门状态为启用则禁用
        if isEnabled == True:
            response = enableDept(id=createNewDepartment, isEnabled=False)
            assert response['msg'] == '请求成功'
            # 再次启用部门
            response2 = enableDept(id=createNewDepartment, isEnabled=True)
            assert response2['msg'] == '请求成功'
        else:
            # 如果状态为已禁用就启用
            response = enableDept(id=createNewDepartment, isEnabled=True)
            assert response['msg'] == '请求成功'

    # @pytest.mark.skip('顶级部门不能被禁用，目前禁用成功了')  # TODO
    def test_05(self, topLevelId):
        """禁用顶级部门"""
        response = enableDept(id=topLevelId, isEnabled=False)
        assert response['msg'] == '不能禁用最上层部门'


class TestGetDetail:
    """查询部门详情"""

    def test_01(self, createNewDepartment):
        """查询成功"""
        response = request.get('/department/getDetail/%d' % createNewDepartment)
        assert response['msg'] == '请求成功'

    def test_02(self):
        """部门id不存在"""
        response = request.get('/department/getDetail/%d' % 000000)
        assert response['msg'] == '该部门不存在'
