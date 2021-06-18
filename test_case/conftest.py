# __author:"zonglr"
# date:2020/11/6
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

import pytest
import time, datetime
from test_case.common import Purchase_Management, Order_Management, login, Warehouse_Management, PostgresSql

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

@pytest.fixture(scope='class', autouse=True)
def res_data():
    yield
    body_data.clear()


@pytest.fixture(scope="class")
# 调拨单：获取参数
def AllocateOrder_get_data():
    # 获取所有需要的参数
    test = Purchase_Management.AllocateOrder()
    global ReasonCode, SourceWarehouseId, TargetWarehouseId, GoodsId, GoodsLotInfoId, KitStockId, \
        GoodsQuantity, KitStockQuantity
    ReasonCode = test.get_allocate_reason()
    SourceWarehouseId = test.get_out_warehouse()
    TargetWarehouseId = test.get_in_warehouse()
    GoodsInfo = test.get_goodsInfo(SourceWarehouseId)
    GoodsId = GoodsInfo[0]
    GoodsLotInfoId = GoodsInfo[1]
    # KitStockId = None
    KitStockId = test.get_kitStockId(SourceWarehouseId)
    GoodsQuantity = 1
    KitStockQuantity = 1


# 调拨单：获取调拨单id
@pytest.fixture(scope="class")
def AllocateOrder_get_Id(AllocateOrder_get_data):
    response = Purchase_Management.AllocateOrder().create(reasonCode=ReasonCode, sourceWarehouseId=SourceWarehouseId,
                                                          targetWarehouseId=TargetWarehouseId, goodsId=GoodsId,
                                                          goodsLotInfoId=GoodsLotInfoId, kitStockId=KitStockId,
                                                          goodsQuantity=GoodsQuantity,
                                                          kitStockQuantity=KitStockQuantity)
    Id = response[0]
    yield Id


# 调拨单：审核调拨单
@pytest.fixture(scope="class")
def AllocateOrder_approve(AllocateOrder_get_Id):
    Purchase_Management.AllocateOrder().approve(allocateId=AllocateOrder_get_Id)

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


# 编辑用
@pytest.fixture(scope='class')
def AdhocOrder_get_id03(AdhocOrder_get_data):
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


# 关闭用
@pytest.fixture(scope='class')
def AdhocOrder_get_id04(AdhocOrder_get_data):
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


# 临调单：拒绝临调单
@pytest.fixture(scope='class')
def AdhocOrder_reject(AdhocOrder_get_id):
    response = Order_Management.AdhocOrder().adhocOrder_reject(id=AdhocOrder_get_id)
    return AdhocOrder_get_id


# 临调单：拒绝临调单，编辑
@pytest.fixture(scope='class')
def AdhocOrder_reject01(AdhocOrder_get_id03):
    response = Order_Management.AdhocOrder().adhocOrder_reject(id=AdhocOrder_get_id03)
    return AdhocOrder_get_id03


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


# 临调单：关闭临调单
@pytest.fixture(scope='class')
def AdhocOrder_close(AdhocOrder_get_id04):
    response = Order_Management.AdhocOrder().adhocOrder_close(adhocOrderId=AdhocOrder_get_id04)


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


# 临调单 修改收货地址
@pytest.fixture(scope='class')
def AdhocOrder_updateAddress(AdhocOrder_accept):
    response = Order_Management.AdhocOrder().adhocOrder_updataAddress(payOnDelivery=True, deliveryMode='SELF_PIKE_UP',
                                                                      consignorName='提货人',
                                                                      consignorPhone=13212345567,
                                                                      receivingIdCard=421322199811044619,
                                                                      powerOfAttorney='http://192.168.10.254:9191/server/file/2021/05/17/5b'
                                                                                      '15b54d-de1f-4aab-ab5b-ffe6bc5a6998/base64Test.jpg',
                                                                      orderId=AdhocOrder_accept, addressId=addressId,
                                                                      parentId=AdhocOrder_accept)
    yield AdhocOrder_accept


# 仓库管理 获取拣货单ID/picking用
@pytest.fixture(scope='class')
def PickOrder_get_pickOrderId():
    global pickOrderId
    keyword = Purchase_Management.AllocateOrder().all()
    pickOrderId = Warehouse_Management.OutboundOrder().get_out_orderInfo(keyword)[0]
    yield pickOrderId


# 仓库管理 获取拣货单ID/pick approval用
@pytest.fixture(scope='class')
def PickOrder_get_pickOrderId01():
    global pickOrderId01
    keyword = Purchase_Management.AllocateOrder().all()
    pickOrderId01 = Warehouse_Management.OutboundOrder().get_out_orderInfo(keyword)[0]
    yield pickOrderId01


# 仓库管理 获取拣货单信息
@pytest.fixture(scope='class')
def PickOrder_get_pickOrderInfo(PickOrder_get_pickOrderId):
    global storageLocationId
    infoList = Warehouse_Management.PickOrder().get_pick_orderInfo(PickOrder_get_pickOrderId)
    materialCode = infoList[0]
    warehouseId = infoList[1]
    storageLocationId = infoList[2]
    quantity = infoList[3]
    yield materialCode, warehouseId, storageLocationId, quantity


@pytest.fixture(scope='class')
def PickOrder_get_pickOrderInfo01(PickOrder_get_pickOrderId01):
    global storageLocationId01
    infoList = Warehouse_Management.PickOrder().get_pick_orderInfo(PickOrder_get_pickOrderId01)
    materialCode = infoList[0]
    warehouseId = infoList[1]
    storageLocationId01 = infoList[2]
    quantity = infoList[3]
    yield materialCode, warehouseId, storageLocationId01, quantity


# 仓库管理 获取拣货单 商品信息
@pytest.fixture(scope='class')
def PickOrder_get_goodsInfo(PickOrder_get_pickOrderInfo):
    goodsinfoList = Warehouse_Management.PickOrder().get_goodsInfo(PickOrder_get_pickOrderInfo[1],
                                                                   PickOrder_get_pickOrderInfo[0])
    goodsId = goodsinfoList[0]
    lotNum = goodsinfoList[1]
    yield goodsId, lotNum


# 仓库管理 获取拣货单 商品信息
@pytest.fixture(scope='class')
def PickOrder_get_goodsInfo01(PickOrder_get_pickOrderInfo01):
    goodsinfoList = Warehouse_Management.PickOrder().get_goodsInfo(PickOrder_get_pickOrderInfo01[1],
                                                                   PickOrder_get_pickOrderInfo01[0])
    goodsId = goodsinfoList[0]
    lotNum = goodsinfoList[1]
    yield goodsId, lotNum


# 仓库管理 拣货单 拣货
@pytest.fixture(scope='class')
def PickOrder_picking(PickOrder_get_goodsInfo):
    Warehouse_Management.PickOrder().picking(goodsId=PickOrder_get_goodsInfo[0], lotNum=PickOrder_get_goodsInfo[1],
                                             pickOrderId=pickOrderId, storageLocationId=storageLocationId)


# 仓库管理 拣货单 拣货
@pytest.fixture(scope='class')
def PickOrder_picking01(PickOrder_get_goodsInfo01):
    Warehouse_Management.PickOrder().picking(goodsId=PickOrder_get_goodsInfo01[0], lotNum=PickOrder_get_goodsInfo01[1],
                                             pickOrderId=pickOrderId01, storageLocationId=storageLocationId01)


# 仓库管理 拣货单 拣货完成
@pytest.fixture(scope='class')
def PickOrder_pickFinished(PickOrder_picking, PickOrder_get_pickOrderId):
    Warehouse_Management.PickOrder().pickFinished(PickOrder_get_pickOrderId)


# 仓库管理 拣货单 拣货完成
@pytest.fixture(scope='class')
def PickOrder_pickFinished01(PickOrder_picking01, PickOrder_get_pickOrderId01):
    Warehouse_Management.PickOrder().pickFinished(PickOrder_get_pickOrderId01)


# 拣货完成
@pytest.fixture(scope='class')
def PickOrder_picking02():
    keyword = Purchase_Management.AllocateOrder().all()

    pickOrderId = Warehouse_Management.OutboundOrder().get_out_orderInfo(keyword)[0]
    infoList = Warehouse_Management.PickOrder().get_pick_orderInfo01(pickOrderId)
    lotNum02 = infoList['data']['goodsDetail'][0]['lotNum']
    goodsId02 = infoList['data']['goodsDetail'][0]['goodsId']
    storageLocationId02 = infoList['data']['goodsDetail'][0]['storageLocationId']

    Warehouse_Management.PickOrder().picking(goodsId=goodsId02, lotNum=lotNum02, pickOrderId=pickOrderId,
                                             storageLocationId=storageLocationId02)
    yield pickOrderId


# 拣货审核完成
@pytest.fixture(scope='class')
def PickOrder_pickFinish02():
    keyword = Purchase_Management.AllocateOrder().all()

    pickOrderId = Warehouse_Management.OutboundOrder().get_out_orderInfo(keyword)[0]
    infoList = Warehouse_Management.PickOrder().get_pick_orderInfo01(pickOrderId)
    lotNum03 = infoList['data']['goodsDetail'][0]['lotNum']
    goodsId03 = infoList['data']['goodsDetail'][0]['goodsId']
    storageLocationId02 = infoList['data']['goodsDetail'][0]['storageLocationId']

    Warehouse_Management.PickOrder().picking(goodsId=goodsId03, lotNum=lotNum03, pickOrderId=pickOrderId,
                                             storageLocationId=storageLocationId02)
    Warehouse_Management.PickOrder().pickFinished(pickOrderId)

    yield pickOrderId, goodsId03


# 仓库管理 拣货单 拣货审核
@pytest.fixture(scope='class')
def PickOrder_pick_approval(PickOrder_pickFinished, PickOrder_get_pickOrderInfo, PickOrder_get_goodsInfo,
                            PickOrder_pickFinished01):
    Warehouse_Management.PickOrder().pick_approval(pickOrderId=pickOrderId,
                                                   goodsId=PickOrder_get_goodsInfo[0],
                                                   quantity=PickOrder_get_pickOrderInfo[3])


# 仓库管理 审核发货到出库用
@pytest.fixture(scope='class')
def PickOrder_approval01():
    keyword = Purchase_Management.AllocateOrder().all()

    pickOrderId = Warehouse_Management.OutboundOrder().get_out_orderInfo(keyword)[0]
    infoList = Warehouse_Management.PickOrder().get_pick_orderInfo01(pickOrderId)
    lotNum03 = infoList['data']['goodsDetail'][0]['lotNum']
    goodsId03 = infoList['data']['goodsDetail'][0]['goodsId']
    quantity = infoList['data']['goodsDetail'][0]['quantity']
    storageLocationId02 = infoList['data']['goodsDetail'][0]['storageLocationId']

    Warehouse_Management.PickOrder().picking(goodsId=goodsId03, lotNum=lotNum03, pickOrderId=pickOrderId,
                                             storageLocationId=storageLocationId02)
    Warehouse_Management.PickOrder().pickFinished(pickOrderId)
    Warehouse_Management.PickOrder().pick_approval(pickOrderId=pickOrderId,
                                                   goodsId=goodsId03,
                                                   quantity=quantity)

    yield keyword


# 仓库管理 出库单 发货
@pytest.fixture(scope='class')
def OutboundOrder_delivery(PickOrder_approval01):
    info = Warehouse_Management.OutboundOrder().get_out_orderInfo(PickOrder_approval01)
    outOrderId = info[1]

    Warehouse_Management.OutboundOrder().delivery(logisticsCompany='顺丰快递', deliveryDate=timeStamp, expressNo='888888',
                                                  outOrderId=outOrderId, deliveryMode='DELIVERY')


# 仓库管理 拣货完成未出库
@pytest.fixture(scope='class')
def OutboundOrder_getId():
    keyword = Purchase_Management.AllocateOrder().all()

    pickOrderId = Warehouse_Management.OutboundOrder().get_out_orderInfo(keyword)[0]
    infoList = Warehouse_Management.PickOrder().get_pick_orderInfo01(pickOrderId)
    lotNum03 = infoList['data']['goodsDetail'][0]['lotNum']
    goodsId03 = infoList['data']['goodsDetail'][0]['goodsId']
    quantity = infoList['data']['goodsDetail'][0]['quantity']
    storageLocationId02 = infoList['data']['goodsDetail'][0]['storageLocationId']

    Warehouse_Management.PickOrder().picking(goodsId=goodsId03, lotNum=lotNum03, pickOrderId=pickOrderId,
                                             storageLocationId=storageLocationId02)
    Warehouse_Management.PickOrder().pickFinished(pickOrderId)
    Warehouse_Management.PickOrder().pick_approval(pickOrderId=pickOrderId,
                                                   goodsId=goodsId03,
                                                   quantity=quantity)
    info = Warehouse_Management.OutboundOrder().get_out_orderInfo(keyword)
    outOrderId = info[1]
    yield outOrderId


@pytest.fixture(scope='class')
def OutboundOrder_approve():
    keyword = Purchase_Management.AllocateOrder().all()

    pickOrderId = Warehouse_Management.OutboundOrder().get_out_orderInfo(keyword)[0]
    outOrderId = Warehouse_Management.OutboundOrder().get_out_orderInfo(keyword)[1]
    infoList = Warehouse_Management.PickOrder().get_pick_orderInfo01(pickOrderId)
    lotNum03 = infoList['data']['goodsDetail'][0]['lotNum']
    goodsId03 = infoList['data']['goodsDetail'][0]['goodsId']
    quantity = infoList['data']['goodsDetail'][0]['quantity']
    storageLocationId02 = infoList['data']['goodsDetail'][0]['storageLocationId']

    Warehouse_Management.PickOrder().picking(goodsId=goodsId03, lotNum=lotNum03, pickOrderId=pickOrderId,
                                             storageLocationId=storageLocationId02)
    Warehouse_Management.PickOrder().pickFinished(pickOrderId)
    Warehouse_Management.PickOrder().pick_approval(pickOrderId=pickOrderId,
                                                   goodsId=goodsId03,
                                                   quantity=quantity)
    Warehouse_Management.OutboundOrder().delivery(logisticsCompany='顺丰快递', deliveryDate=timeStamp, expressNo='888888',
                                                  outOrderId=outOrderId, deliveryMode='DELIVERY')
    Warehouse_Management.OutboundOrder().approval(logisticsCompany='顺丰快递', deliveryDate=timeStamp, expressNo='999999',
                                                  outOrderId=outOrderId)
    yield keyword


# 仓库管理 已发货未审核
@pytest.fixture(scope='class')
def OutboundOrder_getId01():
    keyword = Purchase_Management.AllocateOrder().all()

    pickOrderId = Warehouse_Management.OutboundOrder().get_out_orderInfo(keyword)[0]
    infoList = Warehouse_Management.PickOrder().get_pick_orderInfo01(pickOrderId)
    lotNum03 = infoList['data']['goodsDetail'][0]['lotNum']
    goodsId03 = infoList['data']['goodsDetail'][0]['goodsId']
    quantity = infoList['data']['goodsDetail'][0]['quantity']
    storageLocationId02 = infoList['data']['goodsDetail'][0]['storageLocationId']

    Warehouse_Management.PickOrder().picking(goodsId=goodsId03, lotNum=lotNum03, pickOrderId=pickOrderId,
                                             storageLocationId=storageLocationId02)
    Warehouse_Management.PickOrder().pickFinished(pickOrderId)
    Warehouse_Management.PickOrder().pick_approval(pickOrderId=pickOrderId,
                                                   goodsId=goodsId03,
                                                   quantity=quantity)
    info = Warehouse_Management.OutboundOrder().get_out_orderInfo(keyword)
    outOrderId = info[1]
    Warehouse_Management.OutboundOrder().delivery(logisticsCompany='顺丰快递', deliveryDate=timeStamp, expressNo='888888',
                                                  outOrderId=outOrderId, deliveryMode='DELIVERY')
    yield outOrderId


# 仓库管理 入库单 收货
@pytest.fixture(scope='class')
def InboundOrder_receiving(OutboundOrder_approve):
    inboundId = Warehouse_Management.InboundOrder().get_inboundOrderId(OutboundOrder_approve)[0]
    inboundCode = Warehouse_Management.InboundOrder().get_inboundOrderId(OutboundOrder_approve)[1]
    info = Warehouse_Management.InboundOrder().get_InboundOrder_Info(inboundOrderId=inboundId)
    registrationNum = info[0]
    inboundingQuantity = info[1]
    goodsId = info[2]
    lotNum = info[3]

    Warehouse_Management.InboundOrder().inbound_receiving(inboundOrderId=inboundId, goodsId=goodsId,
                                                          quantity=inboundingQuantity, lotNum=lotNum,
                                                          registrationNum=registrationNum, serialNumber=None)
    yield inboundCode


@pytest.fixture(scope='class')
def OutboundOrder_approve01():
    keyword = Purchase_Management.AllocateOrder().all()

    pickOrderId = Warehouse_Management.OutboundOrder().get_out_orderInfo(keyword)[0]
    outOrderId = Warehouse_Management.OutboundOrder().get_out_orderInfo(keyword)[1]
    infoList = Warehouse_Management.PickOrder().get_pick_orderInfo01(pickOrderId)
    lotNum03 = infoList['data']['goodsDetail'][0]['lotNum']
    goodsId03 = infoList['data']['goodsDetail'][0]['goodsId']
    quantity = infoList['data']['goodsDetail'][0]['quantity']
    storageLocationId02 = infoList['data']['goodsDetail'][0]['storageLocationId']

    Warehouse_Management.PickOrder().picking(goodsId=goodsId03, lotNum=lotNum03, pickOrderId=pickOrderId,
                                             storageLocationId=storageLocationId02)
    Warehouse_Management.PickOrder().pickFinished(pickOrderId)
    Warehouse_Management.PickOrder().pick_approval(pickOrderId=pickOrderId,
                                                   goodsId=goodsId03,
                                                   quantity=quantity)
    Warehouse_Management.OutboundOrder().delivery(logisticsCompany='顺丰快递', deliveryDate=timeStamp, expressNo='888888',
                                                  outOrderId=outOrderId, deliveryMode='DELIVERY')
    Warehouse_Management.OutboundOrder().approval(logisticsCompany='顺丰快递', deliveryDate=timeStamp, expressNo='999999',
                                                  outOrderId=outOrderId)
    inboundId = Warehouse_Management.InboundOrder().get_inboundOrderId(keyword)[0]
    yield inboundId


@pytest.fixture(scope='class')
def OutboundOrder_approve02():
    keyword = Purchase_Management.AllocateOrder().all()

    pickOrderId = Warehouse_Management.OutboundOrder().get_out_orderInfo(keyword)[0]
    outOrderId = Warehouse_Management.OutboundOrder().get_out_orderInfo(keyword)[1]
    infoList = Warehouse_Management.PickOrder().get_pick_orderInfo01(pickOrderId)
    lotNum03 = infoList['data']['goodsDetail'][0]['lotNum']
    goodsId03 = infoList['data']['goodsDetail'][0]['goodsId']
    quantity = infoList['data']['goodsDetail'][0]['quantity']
    storageLocationId02 = infoList['data']['goodsDetail'][0]['storageLocationId']

    Warehouse_Management.PickOrder().picking(goodsId=goodsId03, lotNum=lotNum03, pickOrderId=pickOrderId,
                                             storageLocationId=storageLocationId02)
    Warehouse_Management.PickOrder().pickFinished(pickOrderId)
    Warehouse_Management.PickOrder().pick_approval(pickOrderId=pickOrderId,
                                                   goodsId=goodsId03,
                                                   quantity=quantity)
    Warehouse_Management.OutboundOrder().delivery(logisticsCompany='顺丰快递', deliveryDate=timeStamp, expressNo='888888',
                                                  outOrderId=outOrderId, deliveryMode='DELIVERY')
    Warehouse_Management.OutboundOrder().approval(logisticsCompany='顺丰快递', deliveryDate=timeStamp, expressNo='999999',
                                                  outOrderId=outOrderId)
    yield keyword


@pytest.fixture(scope='class')
def PutOnShelf_put(InboundOrder_receiving):
    putId = Warehouse_Management.PutOnShelf().get_putOnShelfId(InboundOrder_receiving)
    info = Warehouse_Management.PutOnShelf().get_putOnshelf_detail(putId)
    goodsId = info[0]
    goodsLotInfoId = info[1]
    storageLocationCode = info[2]
    quantity = info[3]
    putOnShelfId = info[4]
    Warehouse_Management.PutOnShelf().putOnshelf(goodsId=goodsId, goodsLotInfoId=goodsLotInfoId, quantity=quantity,
                                                 storageLocationCode=storageLocationCode, putOnShelfId=putOnShelfId)
    yield InboundOrder_receiving


@pytest.fixture(scope='class')
def InboundOrder_receiving01(OutboundOrder_approve02):
    inboundId = Warehouse_Management.InboundOrder().get_inboundOrderId(OutboundOrder_approve02)[0]
    inboundCode = Warehouse_Management.InboundOrder().get_inboundOrderId(OutboundOrder_approve02)[1]
    info = Warehouse_Management.InboundOrder().get_InboundOrder_Info(inboundOrderId=inboundId)
    registrationNum = info[0]
    inboundingQuantity = info[1]
    goodsId = info[2]
    lotNum = info[3]

    Warehouse_Management.InboundOrder().inbound_receiving(inboundOrderId=inboundId, goodsId=goodsId,
                                                          quantity=inboundingQuantity, lotNum=lotNum,
                                                          registrationNum=registrationNum, serialNumber=None)
    putOnShelfId = Warehouse_Management.PutOnShelf().get_putOnShelfId(inboundCode)

    yield putOnShelfId, inboundCode


@pytest.fixture(scope='class')
def PutOnShelf_put01(InboundOrder_receiving01):
    info = Warehouse_Management.PutOnShelf().get_putOnshelf_detail(InboundOrder_receiving01[0])
    goodsId = info[0]
    goodsLotInfoId = info[1]
    storageLocationCode = info[2]
    quantity = info[3]
    putOnShelfId = info[4]
    Warehouse_Management.PutOnShelf().putOnshelf(goodsId=goodsId, goodsLotInfoId=goodsLotInfoId, quantity=quantity,
                                                 storageLocationCode=storageLocationCode, putOnShelfId=putOnShelfId)

    checkId = Warehouse_Management.CheckOrder().get_checkOrder_list(InboundOrder_receiving01[1])[0]
    yield checkId


@pytest.fixture(scope='class')
def CheckOrder_check(PutOnShelf_put):
    checkId = Warehouse_Management.CheckOrder().get_checkOrder_list(PutOnShelf_put)[0]
    info = Warehouse_Management.CheckOrder().get_checkOrder_Info(checkId)
    goodsLotInfoId = info[1]
    goodsId = info[2]
    lotNum = info[3]
    inboundingQuantity = info[4]
    registrationNum = info[5]
    Warehouse_Management.CheckOrder().check(checkId=checkId, goodsLotInfoId=goodsLotInfoId, goodsId=goodsId,
                                            lotNum=lotNum, registrationNum=registrationNum,
                                            receivedQuantity=inboundingQuantity)


# 预备临调单用
@pytest.fixture(scope='class')
def Prepare_adhocOrder():
    test = Order_Management.AdhocOrder()
    # 品牌
    manufacturerId = test.get_manufacturerId()
    # 默认地址
    addressId = test.add_default_address()
    # 仓库地址
    warehouseId = test.get_warehouse()
    # 年龄段
    ageGroup = test.get_ageGroup()
    # 手术部位
    procedureSite = test.get_procedureSite()
    # 商品信息
    goodsInfo = test.get_goodsInfo()
    goodsId = 20538
    goodsSupplierId = goodsInfo[1]
    orderList = []
    codeList = []

    # 创建临调单
    for i in range(1, 5):
        data = test.adhocOrder_create(procedureSite=procedureSite, manufacturerId=manufacturerId,
                                      ageGroup=ageGroup, addressId=addressId, supplierId=supplierId,
                                      goodsId=goodsId, goodsSupplierId=goodsSupplierId, goodsQuantity=3,
                                      kitTemplateId=None
                                      )
        adhocOrderId = data['data']['id']
        adhocOrderCode = data['data']['code']
        i += 1
        orderList.append(adhocOrderId)
        codeList.append(adhocOrderCode)

    # 接收临调单
    for id in orderList:
        test.adhocOrder_accept(goodsId=goodsId, Gquantity=3,
                               warehouseId=warehouseId, id=id)
    # 拣货发货
    for i in codeList:
        Warehouse_Management.All(i).all_pick_out()

    goodsLotInfoId = test.get_goodsLotInfoId(orderList[0])

    # 提交销用
    for id in orderList[1:]:
        test.adhocOrder_return(childAdhocOrderId=id, goodsId=goodsId, goodsLotInfoId=goodsLotInfoId,
                               Usequantity=1, parentAdhocOrderId=id)
    # 入库、上架、验收
    for i in codeList[1:]:
        Warehouse_Management.All(i).all_in_putOnShelf()

    # 生成销售单
    for id in orderList[2:]:
        test.create_salesOrder(parentId=id, adhocOrderId=id, goodsId=goodsId,
                               goodsLotInfoId=goodsLotInfoId, Usequantity=1)
    # 检查销售单
    for id in orderList[3:]:
        test.check_salesOrder(parentId=id, adhocOrderId=id, goodsId=goodsId,
                              goodsLotInfoId=goodsLotInfoId, Usequantity=1)

    return orderList


# 拆单需要数据库准备商品数量
@pytest.fixture()
def spit_order_prepare():
    test = PostgresSql.PostgresSql()
    sql = """update wms_goods_stock set quantity = 10 where goods_id=20539 and status = 'put_on_shelf' and warehouse_id in (1,89)"""
    test.execute(sql)


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
