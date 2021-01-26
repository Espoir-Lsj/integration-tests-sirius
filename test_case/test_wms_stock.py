# __author:"zonglr"
# date:2020/12/10
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import time, datetime, re
from common import logger, request
from faker import Faker

log = logger.Log()
faker = Faker(locale='zh_CN')


class TestGoodsStock:

    def test_01(self):
        """上架任务清单"""
        response = request.get('/goodsStock/print')
        assert response['msg'] == '请求成功'


class TestKitStock:

    def test_01(self):
        """打印套包条码"""
        response = request.get('/kitStock/printKitBarcode/{barcode}'.format(barcode=0))
        assert response['msg'] == '套包不存在'

    def test_02(self):
        """打印工具包条码"""
        response = request.get('/kitStock/printToolKitBarcode/{barcode}'.format(barcode=0))
        assert response['msg'] == '套包不存在'

    def test_03(self):
        """货位不存在"""
        body = [
            {
                'kitStockId': 0,
                'locationCode': 'test'
            }
        ]
        response = request.post_body('/kitStock/putOnShelf', body=body)
        assert response['msg'] == '货位test不存在'

    def test_04(self):
        """套包待上架列表"""
        # 分页大小为空
        response = request.get('/kitStock/putOnShelfPendingProcedureList?pageNum=0')
        assert response['msg'] == '请填写分页大小'
        # 页码为空
        response2 = request.get('/kitStock/putOnShelfPendingProcedureList?pageSize=20')
        log.info(response2)
        assert response2['msg'] == '请填写当前页码'
        # 分页和页码正确
        # 页码为空
        response3 = request.get('/kitStock/putOnShelfPendingProcedureList?pageNum=0&pageSize=20')
        assert response3['msg'] == '请求成功'

    def test_05(self):
        """工具包待上架列表"""
        # 分页大小为空
        response = request.get('/kitStock/putOnShelfPendingToolsList?pageNum=0')
        assert response['msg'] == '请填写分页大小'
        # 页码为空
        response2 = request.get('/kitStock/putOnShelfPendingToolsList?pageSize=20')
        log.info(response2)
        assert response2['msg'] == '请填写当前页码'
        # 分页和页码正确
        # 页码为空
        response3 = request.get('/kitStock/putOnShelfPendingToolsList?pageNum=0&pageSize=20')
        assert response3['msg'] == '请求成功'
