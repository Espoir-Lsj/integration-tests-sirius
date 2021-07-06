# -*- coding: utf-8 -*-
# @Time : 2021/6/7 2:47 下午 
# @Author : lsj
# @File : test_All.py
import allure, pytest

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
    # PackagingOrder_test = Material_Management.PackagingOrder()
    # PackagingOrder_test.all()


# 订单管理主流程
@allure.feature('主流程冒烟')
@allure.story('订单管理——创建订单')
def test_Order():
    AdhocOrder_test = Order_Management.AdhocOrder()
    AdhocOrder_test.all()


# goodsId = 20543


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('订单管理——单物资全流程')
def test_Order_all():
    AdhocOrder_test = Order_Management.AdhocOrder()
    # # 全部销用
    AdhocOrder_test.all_process(goodsId=26745, Usequantity=10)
    # # 部分销用
    AdhocOrder_test.all_process(goodsId=26745, Usequantity=4)
    # 全部未销用
    AdhocOrder_test.all_process(goodsId=26745, Usequantity=0)


# 拆单流程
@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('临调——拆单流程--全部销用')
def test_spit_order(spit_order_prepare):
    test = Order_Management.AdhocOrder()
    # 全部销用
    res = test.all_process_spit([9, 7])
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('临调——拆单流程--部分销用')
def test_spit_order2(spit_order_prepare):
    test = Order_Management.AdhocOrder()
    # 部分销用
    res = test.all_process_spit([1, 2])
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('临调——拆单流程--未销用')
def test_spit_order3(spit_order_prepare):
    test = Order_Management.AdhocOrder()
    # 全部未销用
    res = test.all_process_spit([0, 0])
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('临调——拆单流程--未销用--加部分销用')
def test_spit_order4(spit_order_prepare):
    test = Order_Management.AdhocOrder()
    # 全部未销用+部分销用
    res = test.all_process_spit([0, 1])
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('临调——拆单流程--全部销用--加全未销用')
def test_spit_order5(spit_order_prepare):
    test = Order_Management.AdhocOrder()
    # 全部销用+未销用
    res = test.all_process_spit([9, 0])
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('临调——拆单流程--全部销用--加部分销用')
def test_spit_order5(spit_order_prepare):
    test = Order_Management.AdhocOrder()
    # 全部销用+未销用
    res = test.all_process_spit([9, 1])
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
# 临调申请多物资
@allure.story('多物资临调--全部销用')
def test_more_goods():
    test = Order_Management.AdhocOrder()
    res = test.all_process_more([26745, 23626], [10, 10], [10, 10])
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('多物资临调--部分销用')
def test_more_goods2():
    test = Order_Management.AdhocOrder()
    res = test.all_process_more([26745, 23626, 22130], [10, 10, 10], [10, 2, 3])
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('多物资临调--未销用')
def test_more_goods3():
    test = Order_Management.AdhocOrder()
    res = test.all_process_more([26745, 23626], [10, 10], [0, 0])
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('多物资临调--未销用--加部分销用')
def test_more_goods4():
    test = Order_Management.AdhocOrder()
    res = test.all_process_more([26745, 23626], [10, 10], [0, 3])
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('多物资临调--全部销用--加部分未销用')
def test_more_goods5():
    test = Order_Management.AdhocOrder()
    res = test.all_process_more([26745, 23626], [10, 10], [10, 0])
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('多物资临调--全部销用--加部分销用')
def test_more_goods6():
    test = Order_Management.AdhocOrder()
    res = test.all_process_more([26745, 23626], [10, 10], [10, 1])
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('临调--只申请工具包')
def test_tools():
    test = Order_Management.AdhocOrder()
    res = test.all_tools()
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('临调--工具包+多物资全部销用')
def test_tools_goods():
    test = Order_Management.AdhocOrder()
    res = test.all_tools_goods([26745, 23626], [5, 4], [5, 4], [112], [1])
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('临调--工具包+多物资')
def test_tools_goods1():
    test = Order_Management.AdhocOrder()
    res = test.all_tools_goods([26745, 23626, 22130], [5, 6, 7], [1, 1, 1], [112], [1])
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('临调--工具包+多物资 部分全部销用')
def test_tools_goods2():
    test = Order_Management.AdhocOrder()
    res = test.all_tools_goods([26745, 23626], [5, 4], [5, 0], [112], [1])
    assert res == 'success'


@pytest.mark.Order_Smoke
@allure.feature('主流程冒烟')
@allure.story('临调--工具包+多物资 未销用')
def test_tools_goods3():
    test = Order_Management.AdhocOrder()
    res = test.all_tools_goods([26745, 23626], [5, 4], [0, 0], [112], [1])
    assert res == 'success'


@allure.story('调拨--单物资')
@allure.feature('主流程冒烟')
def test_allocateOrder():
    test = Purchase_Management.AllocateOrder()
    test.all(26745, 10)


@allure.story('调拨--多物资')
@allure.feature('主流程冒烟')
def test_allocateOrder_more():
    test = Purchase_Management.AllocateOrder()
    # test.all_moreGoods(['ID_20539'], [9])
    res = test.all_moreGoods(['ID_26745', 'ID_23626'], [1, 2])
    assert res == 'success'


@allure.story('调拨--工具包')
@allure.feature('主流程冒烟')
def test_allocateOrder_tools():
    test = Purchase_Management.AllocateOrder()
    res = test.all_tools()
    assert res == 'success'


@allure.story('调拨--多物资 加 工具包')
@allure.feature('主流程冒烟')
def test_allocateOrder_tools_goods():
    test = Purchase_Management.AllocateOrder()
    res = test.all_tools_goods(['ID_26745', 'ID_23626'], [1, 2])
    assert res == 'success'

# def test001(spit_order_prepare):
#     test = Order_Management.AdhocOrder()
#     test.all_process_spit()
