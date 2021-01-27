# __author:"zonglr"
# date:2020/11/28
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, time
from common import logger, request
from test_config import param_config

log = logger.Log()


# 创建部门
def createDept(departmentName, departmentTypeId, parentId, sort=1, isEnabled=False, director=None, phone=None,
               remark=None):
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


# 获取字典部门分类信息,整个文件执行一次
@pytest.fixture(scope="module")
def getByTypeId():
    detail = request.get('/dictionary/getByType/department_type')
    id = detail['data'][0]['id']
    return id


# 获取顶级部门信息,并提取顶级部门id，整个文件执行一次
@pytest.fixture(scope="module")
def parentId():
    detail = request.get('/department/findDepartment')
    departmentid = detail['data'][0]['id']
    return departmentid


class TestCreateDept:
    """新增部门"""

    def test_01(self, getByTypeId, parentId):
        """部门名称为空"""
        response = createDept(departmentName=None, departmentTypeId=getByTypeId, parentId=parentId)
        assert response['msg'] == '请输入部门名称'

    def test_02(self, createInitDepartment):
        log.warning(createInitDepartment)
