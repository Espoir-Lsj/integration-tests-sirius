# -*- coding: utf-8 -*-
# @Time : 2021/5/13 10:13 上午 
# @Author : lsj
# @File : test_purchase_management.py
# 采购管理case
import time, datetime

import allure
import pytest

from test_case.common import Purchase_Management, logger, request

from test_config.yamlconfig import timeid, body_data

timeStamp = int(time.time() * 1000)
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday_stamp = int(time.mktime(yesterday.timetuple())) * 1000
fiveDaysAfter = today + datetime.timedelta(days=5)
fiveDaysAfter_stamp = int(time.mktime(fiveDaysAfter.timetuple())) * 1000
context = str('1').zfill(500)
log = logger.Log()


# 采购管理：调拨单
@allure.feature('采购管理')
@allure.story('调拨单')
@pytest.mark.usefixtures('res_data')
class TestAllocateOrder:
    data = [('调拨理由为空', {'reasonCode': None}, '请选择调拨理由'),
            ('来源仓库空', {'sourceWarehouseId': None}, '请选择来源仓库'),
            ('来源仓库错误', {'targetWarehouseId': 'aa'}, '请求参数异常'),
            ('收货仓库为空', {'targetWarehouseId': None}, '请选择目标仓库'),
            # ('收货仓库错误', {'targetWarehouseId': 9999999}, '请求参数异常'),
            # ('商品ID为空', {'goodsId': None}, ''),
            ('商品数量为空', {'goodsQuantity': None}, '请输入商品数量'),
            ('商品数量过大', {'goodsQuantity': 999999999999}, '商品数量超出限制'),
            ('商品信息为空', {'goodsLotInfoId': None}, '参数异常'),
            ('工具包数量过大', {'kitStockQuantity': 99999999999999}, '工具包数量超出限制')
            ]

    @pytest.mark.parametrize('title,case,expected', data)
    @allure.title('{title}')
    def test_create(self, title, case, expected, AllocateOrder_get_Id):
        url = '/allocateOrder/create'
        body = request.body_replace(url, case)
        response = request.post_body(url, body)
        assert response['msg'] == expected

    @allure.title('编辑未驳回订单')
    def test_edit(self, AllocateOrder_get_Id):
        url = '/allocateOrder/create'
        case = {'id': AllocateOrder_get_Id}
        body = request.body_replace(url, case)
        print(body)
        response = request.post_body(url, body)
        assert response['msg'] == '只能修改驳回的订单'

    data = [
        ('经销商：调拨单ID为空', {'id': None}, '请选择调拨单'),
        ('经销商：审核建议为空', {'approve': None}, '请选择审核或者驳回调拨单'),
        ('经销商：驳回理由为空', {'approve': False, 'rejectReason': None}, '当前用户不可接单'),
        ('经销商：驳回理由超长', {'approve': False, 'rejectReason': context}, '拒绝原因超出长度限制'),
    ]

    @pytest.mark.parametrize('title,case,expected', data)
    @allure.title('{title}')
    def test_approve(self, title, case, expected, AllocateOrder_get_Id):
        url = '/allocateOrder/approve'
        body = {
            "approve": None,
            "id": AllocateOrder_get_Id,
            "rejectReason": None
        }
        body = request.reValue_01(body, case)
        response = request.put_body(url, body)
        assert response['msg'] == expected

    data = [
        ('供应商：调拨单ID为空', {'id': None}, '请选择调拨单'),
        ('供应商：审核建议为空', {'approve': None}, '请选择审核或者驳回调拨单'),
        ('供应商：驳回理由为空', {'approve': False, 'rejectReason': None}, '请输入修改建议'),
        ('供应商：驳回理由超长', {'approve': False, 'rejectReason': context}, '拒绝原因超出长度限制'),
    ]

    @pytest.mark.parametrize('title,case,expected', data)
    @allure.title('{title}')
    def test_approve01(self, title, case, expected, AllocateOrder_get_Id):
        url = '/allocateOrder/approve'
        body = {
            "approve": None,
            "id": AllocateOrder_get_Id,
            "rejectReason": None
        }
        body = request.reValue_01(body, case)
        response = request.put_body01(url, body)
        assert response['msg'] == expected

    @allure.title('删除未关闭订单')
    def test_remove_01(self, AllocateOrder_get_Id):
        url = '/allocateOrder/remove?orderId=%s' % AllocateOrder_get_Id
        response = request.delete(url)
        assert response['msg'] == '订单状态为已关闭时才能删除'

    data = [
        ('重复关闭订单', '订单状态为待接收或待修改时才能关闭')
    ]

    @pytest.mark.parametrize('title,expected', data)
    @allure.title('{title}')
    def test_close(self, title, expected, AllocateOrder_close):
        url = '/allocateOrder/close?orderId=%s' % AllocateOrder_close
        response = request.put(url)
        assert response['msg'] == expected

    @allure.title('重复删除订单')
    def test_remove_02(self, AllocateOrder_remove):
        url = '/allocateOrder/remove?orderId=%s' % AllocateOrder_remove
        response = request.delete(url)
        assert response['msg'] == '未查询到该调拨订单，请刷新重试'
