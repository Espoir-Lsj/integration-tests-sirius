# -*- coding: utf-8 -*-
# @Time : 2021/6/7 2:47 下午 
# @Author : lsj
# @File : test_All.py
from test_case.common import Material_Management, Order_Management, Purchase_Management, Warehouse_Management


# 物资管理主流程
def test_material():
    # 物资/工具
    Goods_test = Material_Management.Goods('material')
    Goods_test1 = Material_Management.Goods('tool')
    Goods_test.all()
    Goods_test1.all()

    # 工具包
    KitTemplate_test = Material_Management.KitTemplate()
    KitTemplate_test.all()

    # 加工组包
    PackagingOrder_test = Material_Management.PackagingOrder()
    PackagingOrder_test.all()


# 采购管理主流程
def purchase():
    AllocateOrder_test = Purchase_Management.AllocateOrder()
    AllocateOrder_test.all()


# 订单管理主流程
def Oeder():
    AdhocOrder_test = Order_Management.AdhocOrder()
    AdhocOrder_test.all()


# 仓库管理主流程
def Warehouse():
    OutboundOrder_test = Warehouse_Management.OutboundOrder()

    PickOrder_test = Warehouse_Management.PickOrder()

    InboundOrder_test = Warehouse_Management.InboundOrder()
