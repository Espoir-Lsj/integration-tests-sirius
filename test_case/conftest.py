# __author:"zonglr"
# date:2020/11/6
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

import pytest
import time, datetime
from test_case.common import Purchase_Management, Order_Management, login

from test_config.yamlconfig import timeid, body_data

# log = logger.Log()

supplierId = login.supplierId
timeStamp = int(time.time() * 1000)
today = datetime.date.today()
fiveDaysAfter = today + datetime.timedelta(days=5)
fiveDaysAfter_stamp = int(time.mktime(fiveDaysAfter.timetuple())) * 1000


# @pytest.fixture(scope='class')
# def res_data():
#     timeid(file_yaml='request_data.yaml')._set_yaml_time({'url': 'body'}, 'w')

@pytest.fixture(scope='class')
def res_data():
    yield
    body_data.clear()


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
        toolsQuantity, hospitalName, contactName, contactPhone, receivingName, surgeon, deliveryMode, warehouseId
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
    warehouseId = test.get_warehouse()


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
    yield response['data']['id']
    # Order_Management.AdhocOrder().adhocOrder_close(response['data']['id'])


# 接收用
@pytest.fixture(scope='class')
def AdhocOrder_get_id01(AdhocOrder_get_data):
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
    yield response['data']['id']
    # Order_Management.AdhocOrder().adhocOrder_close(response['data']['id'])


# 拒绝用
@pytest.fixture(scope='class')
def AdhocOrder_get_id02(AdhocOrder_get_data):
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
    yield response['data']['id']
    # Order_Management.AdhocOrder().adhocOrder_close(response['data']['id'])


# 临调单：拒绝临调单
@pytest.fixture(scope='class')
def AdhocOrder_reject(AdhocOrder_get_id):
    response = Order_Management.AdhocOrder().adhocOrder_reject(id=AdhocOrder_get_id)
    return AdhocOrder_get_id


# 临调单：接收临调单
@pytest.fixture(scope='class')
def AdhocOrder_accept(AdhocOrder_get_id):
    response = Order_Management.AdhocOrder().adhocOrder_accept(id=AdhocOrder_get_id, goodsId=AdhocOrdergoodsId,
                                                               Gquantity=AdhocOrdergoodsQuantity,
                                                               kitTemplateId=kitTemplateId,
                                                               Kquantity=toolsQuantity, warehouseId=warehouseId)
    return AdhocOrder_get_id


# 临调单：编辑临调单
@pytest.fixture(scope='class')
def AdhocOrder_edit(AdhocOrder_reject):
    response = Order_Management.AdhocOrder().adhocOrder_edit(id=AdhocOrder_reject,
                                                             procedureSite=procedureSite,
                                                             manufacturerId=manufacturerId,
                                                             ageGroup=ageGroup, addressId=addressId,
                                                             supplierId=supplierId,
                                                             goodsId=AdhocOrdergoodsId,
                                                             goodsQuantity=AdhocOrdergoodsQuantity,
                                                             goodsSupplierId=goodsSupplierId,
                                                             kitTemplateId=kitTemplateId,
                                                             toolsQuantity=toolsQuantity,
                                                             hospitalName=hospitalName,
                                                             contactName=contactName,
                                                             contactPhone=contactPhone,
                                                             receivingName=receivingName,
                                                             deliveryMode=deliveryMode
                                                             )


# 临调单 添加默认收货地址
@pytest.fixture(scope='class')
def AdhocOrder_add_address():
    response = Order_Management.AdhocOrder().add_default_address()


# 临调单 查找默认地址id
@pytest.fixture(scope='class')
def AdhocOrder_get_addressId():
    addressId = Order_Management.AdhocOrder().get_addressId()
    yield addressId


# 临调单 修改默认收货地址
@pytest.fixture(scope='class')
def AdhocOrder_update_address(AdhocOrder_get_addressId):
    response = Order_Management.AdhocOrder().update_default_address(id=AdhocOrder_get_addressId)


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
