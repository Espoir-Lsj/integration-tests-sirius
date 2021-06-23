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
@allure.story('订单管理——创建订单')
def test_Order():
    AdhocOrder_test = Order_Management.AdhocOrder()
    AdhocOrder_test.all()


@allure.story('订单管理——单物资全流程')
def test_Order_all():
    AdhocOrder_test = Order_Management.AdhocOrder()
    # 全部销用
    AdhocOrder_test.all_process(Usequantity=10)
    # 部分销用
    AdhocOrder_test.all_process(Usequantity=4)
    # 全部未销用
    AdhocOrder_test.all_process(Usequantity=0)


# 仓库管理主流程
@allure.story('仓库管理')
def test_Warehouse():
    log.info("-----------调拨流程出入库--------------")
    purchaseKey = test_Purchase()
    all_out_test = Warehouse_Management.All(purchaseKey).all_pick_out()
    all_in_test = Warehouse_Management.All(purchaseKey).all_in_putOnShelf()


# 拆单流程
@allure.story('临调——拆单流程--全部销用')
def test_spit_order(spit_order_prepare):
    test = Order_Management.AdhocOrder()
    # 全部销用
    test.all_process_spit([9, 7])


@allure.story('临调——拆单流程--部分销用')
def test_spit_order2(spit_order_prepare):
    test = Order_Management.AdhocOrder()
    # 部分销用
    test.all_process_spit([1, 2])


@allure.story('临调——拆单流程--未销用')
def test_spit_order3(spit_order_prepare):
    test = Order_Management.AdhocOrder()
    # 全部未销用
    test.all_process_spit([0, 0])


# 临调申请多物资
@allure.story('多物资临调--全部销用')
def test_more_goods():
    test = Order_Management.AdhocOrder()
    test.all_process_more([20538, 20540], [10, 10], [10, 10])


@allure.story('多物资临调--部分销用')
def test_more_goods2():
    test = Order_Management.AdhocOrder()
    test.all_process_more([20538, 20540], [10, 10], [3, 4])


@allure.story('多物资临调--未销用')
def test_more_goods3():
    test = Order_Management.AdhocOrder()
    test.all_process_more([20538, 20540], [10, 10], [0, 0])


@allure.story('临调--只申请工具包')
def test_tools():
    test = Order_Management.AdhocOrder()
    test.all_tools()


def test001(spit_order_prepare):
    test = Order_Management.AdhocOrder()
    test.all_process_spit()
