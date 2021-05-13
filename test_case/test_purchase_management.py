# -*- coding: utf-8 -*-
# @Time : 2021/5/13 10:13 上午 
# @Author : lsj
# @File : test_purchase_management.py
# 采购管理case
import time, datetime

import allure
import pytest

from common import Purchase_Management, logger, request, tes

timeStamp = int(time.time() * 1000)
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday_stamp = int(time.mktime(yesterday.timetuple())) * 1000
fiveDaysAfter = today + datetime.timedelta(days=5)
fiveDaysAfter_stamp = int(time.mktime(fiveDaysAfter.timetuple())) * 1000
log = logger.Log()


# 采购管理：调拨单
class TestAllocateOrder:

    @pytest.fixture(scope="module")
    def get_data(self):
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

    @pytest.fixture()
    def get_body(self, get_data):
        body = Purchase_Management.AllocateOrder().push_body(reasonCode, sourceWarehouseId, targetWarehouseId, goodsId,
                                                             goodsLotInfoId, kitStockId,
                                                             goodsQuantity, kitStockQuantity)
        yield body

    data = [('调拨理由为空', {'reasonCode': None}, '请选择调拨理由'),
            ('来源仓库空', {'sourceWarehouseId': None}, '请选择来源仓库'),
            ('来源仓库错误', {'targetWarehouseId': 'aa'}, ''),
            # ('收货仓库错误', {'targetWarehouseId': 'aa'}, '请选择目标仓库'),
            # ('收货仓库错误', {'targetWarehouseId': 'aa'}, ''),
            # ('商品ID为空', {'goodsId': None}, ''),
            # ('商品数量为空', {'goodsQuantity': None}, '请输入商品数量'),
            # ('商品数量过大', {'goodsQuantity': 999999999999}, ''),
            # ('商品信息为空', {'goodsLotInfoId': None}, ''),
            # ('工具包ID为空', {'kitStockId': None}, ''),
            # ('工具包数量为空', {'kitStockId': None}, '请输入工具包数量'),
            # ('工具包数量过大', {'kitStockQuantity': 99999999999999}, '')
            ]

    @pytest.mark.parametrize('title,case,expected', data)
    @allure.title('{title}')
    def test_create(self, title, case, expected, get_body):
        url = '/allocateOrder/create'
        body = get_body
        body = request.reValue(body, case)
        response = request.post_body(url, body)
        assert response['msg'] == expected

    # def test_02(self):
