# __author:"zonglr"
# date:2020/11/6
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

import pytest, jsonpath
import time, datetime
from common import request, logger, Purchase_Management, Order_Management, login

from test_config.yamlconfig import timeid

log = logger.Log()

#
# # 获取权限列表,并返回所有权限id(数组)
# # 整个项目测试用例执行之前执行一次，无论调用多少次，也只执行一次
# @pytest.fixture(scope="session")
# def getPermissoinIds():
#     """正常查询"""
#     response = request.get('/permission/list')
#     assert response['msg'] == '请求成功'
#     assert len(response['data']) > 0
#     # 获取权限id
#     ids = jsonpath.jsonpath(response, '$..id')
#     return ids
#
#
# # 创建一个初始角色分类,并返回角色分类id
# # 整个项目测试用例执行之前执行一次，无聊调用多少次，也只执行一次
# @pytest.fixture(scope="session")
# def createInitRoleType():
#     # 创建角色分类
#     name = param_config.initRoleTypeName
#     response = createRoleType(name=name)
#     assert response['msg'] in ('请求成功', '该角色分类名称已存在')
#     # 根据角色分类名查询分类id
#     list = request.get('/role/findRoleTypeList')
#     assert len(list['data']) > 1
#     for i in list['data']['roleTypeList']:
#         if i['name'] == name:
#             typeId = i['roleTypeId']
#             return typeId
#
#
# # 创建一个初始角色,并返回角色id
# # 整个项目测试用例执行之前执行一次，无论调用多少次，也只执行一次
# @pytest.fixture(scope="session")
# def createInitRole(createInitRoleType):
#     # 创建角色
#     name = param_config.initRoleName
#     response = createRole(name=name, roleType=createInitRoleType)
#     assert response['msg'] in ('请求成功', '该角色名称已存在')
#     # 根据角色名查询角色id
#     list = request.get('/role/findRoleTypeList')
#     assert len(list['data']) > 1
#     # 查询返回结果中所有的角色名
#     names = jsonpath.jsonpath(list, '$..role[*].name')
#     # 所有角色id
#     ids = jsonpath.jsonpath(list, '$..role[*].id')
#     # 根据角色名查询id
#     i = 0
#     while i < len(names):
#         if names[i] == name:
#             roleId = ids[i]
#             return roleId
#         i += 1
#
#
# # 创建一个用户名为defaultLoginName的用户,并返回用户id
# # 整个项目测试用例执行之前执行一次，无论调用多少次，也只执行一次(需要调一次执行加上autouse=True)
# @pytest.fixture(scope="session")
# def createInitUser(createInitDepartment):
#     # 账号名称
#     loginName = param_config.initLoginName
#     # 密码
#     initialPassword = param_config.initialPassword
#     response = createUser(loginName=loginName, initialPassword=initialPassword, departmentId=createInitDepartment)
#     assert response['msg'] in ('请求成功', '登录名已存在')
#     # 根据departmentId查询初始用户的id
#     list = request.get('/user/list?pageNum=0&pageSize=50&departmentId=%s' % createInitDepartment)
#     assert list['data']['totalCount'] > 0
#     # 查询返回的所有账号名
#     names = jsonpath.jsonpath(list, '$..loginName')
#     # 获取账号id
#     ids = jsonpath.jsonpath(list, '$..id')
#     # 根据账号名获取到账号id
#     i = 0
#     while i < len(names):
#         if names[i] == loginName:
#             id = ids[i]
#             return id
#         i += 1
#
#
# # 创建一个初始部门，并返回部门id，整个项目测试用例执行之前执行一次
# @pytest.fixture(scope="session")
# def createInitDepartment():
#     # 初始化一个部门名称
#     deptName = param_config.initDeptName
#     # 获取部门id
#     detail = request.get('/department/findDepartment')
#     departmentId = detail['data'][0]['id']
#     # 获取字典部门分类id
#     detail2 = request.get('/dictionary/getByType/department_type')
#     sortId = detail2['data'][0]['id']
#     response = createDept(departmentName=deptName, departmentTypeId=sortId, parentId=departmentId, isEnabled=False)
#     assert response['msg'] in ('请求成功', '部门已存在')
#     # 查询列表
#     list = request.get('/department/findDepartment')
#     assert len(list['data']) > 0
#     # 提取所有部门名称
#     departmentNames = jsonpath.jsonpath(list, '$..childrenDepartment[*].departmentName')
#     # 提取所有的部门id
#     ids = jsonpath.jsonpath(list, '$..childrenDepartment[*].id')
#     # 根据部门名称循环查询部门id
#     i = 0
#     while i < len(departmentNames):
#         if departmentNames[i] == deptName:
#             id = ids[i]
#             return id
#         i += 1
supplierId = login.supplierId
timeStamp = int(time.time() * 1000)
today = datetime.date.today()
fiveDaysAfter = today + datetime.timedelta(days=5)
fiveDaysAfter_stamp = int(time.mktime(fiveDaysAfter.timetuple())) * 1000


@pytest.fixture(scope='class')
def res_data():
    timeid(file_yaml='request_data.yaml')._set_yaml_time({'url': 'body'}, 'w')


@pytest.fixture(scope="class")
# 调拨单：获取参数
def AllocateOrder_get_data():
    # 获取所有需要的参数
    test = Purchase_Management.AllocateOrder()
    global reasonCode, sourceWarehouseId, targetWarehouseId, goodsId, goodsLotInfoId, kitStockId, \
        goodsQuantity, kitStockQuantity
    reasonCode = test.get_allocate_reason()
    sourceWarehouseId = test.get_out_warehouse()
    targetWarehouseId = test.get_in_warehouse()
    goodsInfo = test.get_goodsInfo(sourceWarehouseId)
    goodsId = goodsInfo[0]
    goodsLotInfoId = goodsInfo[1]
    kitStockId = test.get_kitStockId(sourceWarehouseId)
    goodsQuantity = 1
    kitStockQuantity = 1


# 调拨单：获取调拨单id
@pytest.fixture(scope="class")
def AllocateOrder_get_Id(AllocateOrder_get_data):
    response = Purchase_Management.AllocateOrder().create(reasonCode=reasonCode, sourceWarehouseId=sourceWarehouseId,
                                                          targetWarehouseId=targetWarehouseId, goodsId=goodsId,
                                                          goodsLotInfoId=goodsLotInfoId, kitStockId=kitStockId,
                                                          goodsQuantity=goodsQuantity,
                                                          kitStockQuantity=kitStockQuantity)
    Id = response[0]
    yield Id


# 调拨单：审核调拨单
@pytest.fixture(scope="class")
def AllocateOrder_approve(AllocateOrder_get_Id):
    Purchase_Management.AllocateOrder().approve(Id=AllocateOrder_get_Id)
    yield AllocateOrder_get_Id


# 调拨单：关闭调拨单
@pytest.fixture(scope="class")
def AllocateOrder_close(AllocateOrder_approve):
    Purchase_Management.AllocateOrder().close(AllocateOrder_approve)
    yield AllocateOrder_approve


# 调拨单：删除调拨单
@pytest.fixture(scope="class")
def AllocateOrder_remove(AllocateOrder_close):
    Purchase_Management.AllocateOrder().remove(AllocateOrder_close)
    yield AllocateOrder_close


@pytest.fixture(scope='class')
# 临调单：获取必要参数
def AdhocOrder_get_data():
    global manufacturerId, addressId, ageGroup, procedureSite, AdhocOrdergoodsId, \
        goodsSupplierId, kitTemplateId, toolsSupplierId, AdhocOrdergoodsQuantity, \
        toolsQuantity, hospitalName, contactName, contactPhone, receivingName, surgeon, deliveryMode
    test = Order_Management.AdhocOrder()
    # 品牌
    manufacturerId = test.get_manufacturerId()
    # 默认地址
    addressId = test.get_addressId()
    # 年龄段
    ageGroup = test.get_ageGroup()
    # 手术部位
    procedureSite = test.get_procedureSite()
    # 商品信息
    goodsInfo = test.get_goodsInfo()
    AdhocOrdergoodsId = goodsInfo[0]
    goodsSupplierId = goodsInfo[1]
    # 工具包信息
    toolsInfo = test.get_toolsInfo()
    kitTemplateId = toolsInfo[0]
    toolsSupplierId = toolsInfo[1]
    AdhocOrdergoodsQuantity = 1
    toolsQuantity = 1
    hospitalName = '测试医院'
    contactName = "订单联系人"
    contactPhone = "13333333333"
    receivingName = "收件人"
    surgeon = '主刀医生'
    deliveryMode = 'SELF_PIKE_UP'


# 临调单：创建临调单
@pytest.fixture(scope='class')
def AdhocOrder_get_id(AdhocOrder_get_data):
    response = Order_Management.AdhocOrder().adhocOrder_create(procedureSite=procedureSite,
                                                               manufacturerId=manufacturerId,
                                                               ageGroup=ageGroup, addressId=addressId,
                                                               supplierId=supplierId,
                                                               goodsId=AdhocOrdergoodsId,
                                                               goodsQuantity=AdhocOrdergoodsQuantity,
                                                               goodsSupplierId=goodsSupplierId,
                                                               kitTemplateId=kitTemplateId,
                                                               toolsQuantity=toolsQuantity,
                                                               toolsSupplierId=toolsSupplierId,
                                                               hospitalName=hospitalName,
                                                               contactName=contactName,
                                                               contactPhone=contactPhone,
                                                               receivingName=receivingName,
                                                               deliveryMode=deliveryMode
                                                               )
    return response


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
