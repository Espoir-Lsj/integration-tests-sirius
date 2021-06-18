# -*- coding: utf-8 -*-
# @Time : 2021/6/7 2:47 下午 
# @Author : lsj
# @File : test_All.py
import allure

from test_case.common import Material_Management, Order_Management, Purchase_Management, Warehouse_Management, logger, \
    request

log = logger.Log()


@allure.feature('主流程冒烟')
# 物资管理主流程
@allure.story('物资管理')
def test_material():
    # 物资/工具
    Goods_test = Material_Management.Goods('material')
    Goods_test1 = Material_Management.Goods('tool')
    Goods_test.all()
    Goods_test1.all()

    # # 工具包
    # KitTemplate_test = Material_Management.KitTemplate()
    # KitTemplate_test.all()

    # 加工组包
    PackagingOrder_test = Material_Management.PackagingOrder()
    PackagingOrder_test.all()


# 采购管理主流程
@allure.story('采购管理')
def test_Purchase():
    AllocateOrder_test = Purchase_Management.AllocateOrder()
    code = AllocateOrder_test.all()
    return code


# 订单管理主流程
@allure.story('订单管理')
def test_Order():
    AdhocOrder_test = Order_Management.AdhocOrder()
    AdhocOrder_test.all()
    AdhocOrder_test.all_process()


# 仓库管理主流程
@allure.story('仓库管理')
def test_Warehouse():
    log.info("-----------调拨流程出入库--------------")
    purchaseKey = test_Purchase()
    all_out_test = Warehouse_Management.All(purchaseKey).all_pick_out()
    all_in_test = Warehouse_Management.All(purchaseKey).all_in_putOnShelf()


# 拆单流程
@allure.story('拆单流程')
def test_spit_order(spit_order_prepare):
    """
    临调物资20539 :两个仓库（1，89）库存分别为10
    临调数量16: 1仓发货9，89仓发货7
    """
    goodsId = 20539
    warehouse1 = 1
    warehouse2 = 89
    goodsLotInfoId = 8962

    test = Order_Management.AdhocOrder()
    # 创建地址
    addressId = test.add_default_address(receivingName="拆单专用")
    # 创建临调单
    info = test.adhocOrder_create(goodsId=goodsId, goodsQuantity=16, addressId=addressId, supplierId=216,
                                  manufacturerId=1, deliveryMode="DELIVERY")
    orderId = info['data']['id']
    test.get_result(orderId)
    # 审核临调单
    url = '/adhocOrder/accept'
    body = {
        "detail": [{
            "deliveryMode": "DELIVERY",
            "goodsDetailUiBeans": [{
                "goodsId": goodsId,
                "quantity": 9
            }],
            "toolsDetailUiBeans": [],
            "warehouseId": warehouse1
        }, {
            "deliveryMode": "DELIVERY",
            "goodsDetailUiBeans": [{
                "goodsId": goodsId,
                "quantity": 7
            }],
            "toolsDetailUiBeans": [],
            "warehouseId": warehouse2
        }],
        "id": orderId
    }
    response = request.put_body01(url, body)
    # 获取拆单结果
    data = test.get_adhocOrder_detail(orderId)['data']['childUiList']
    code1 = data[1]['childAdhocOrderUiBean']['code']
    code2 = data[0]['childAdhocOrderUiBean']['code']
    orderId1 = data[1]['childAdhocOrderUiBean']['id']
    orderId2 = data[0]['childAdhocOrderUiBean']['id']
    codelist = [code1, code2]
    # 根据code 拣货出库
    for i in codelist:
        Warehouse_Management.All(i).all_pick_out()
    # 提交销用
    url = '/adhocOrder/adhocReturn'
    body = {
        "detail": [{
            "childAdhocOrderId": orderId1,
            "goodsList": [{
                "goodsId": goodsId,
                "goodsLotInfoId": goodsLotInfoId,
                "kitStockId": None,
                "quantity": 9
            }]
        }, {
            "childAdhocOrderId": orderId2,
            "goodsList": [{
                "goodsId": goodsId,
                "goodsLotInfoId": goodsLotInfoId,
                "kitStockId": None,
                "quantity": 7
            }]
        }],
        "parentAdhocOrderId": orderId
    }
    response1 = request.post_body(url, body)

    # 根据code入库验收
    for i in codelist:
        Warehouse_Management.All(i).all_in_putOnShelf()

    # 生成销售单
    body = {
        "parentId": orderId,
        "createUiBeans": [{
            "adhocOrderId": orderId1,
            "detailUiBeanList": [{
                "goodsId": goodsId,
                "goodsLotInfoId": goodsLotInfoId,
                "quantity": 9
            }]
        }, {
            "adhocOrderId": orderId2,
            "detailUiBeanList": [{
                "goodsId": goodsId,
                "goodsLotInfoId": goodsLotInfoId,
                "quantity": 7
            }]
        }]
    }
    for i in ['/salesOrder/checkSalesOrder', '/salesOrder/createSalesOrder']:
        response2 = request.post_body01(i, body)
