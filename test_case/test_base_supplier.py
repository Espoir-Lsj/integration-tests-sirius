# __author:"zonglr"
# date:2020/11/28
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

import pytest
from common import request, logger

log = logger.Log()


class TestFindContactList:
    """查询对应供应商联系人"""

    url = '/supplier/findContactList'

    def test_01(self):
        """查询不存在的供应商联系人"""
        response = request.get(self.url + '?supplierId=0')
        assert response['msg'] == '请求成功'
        assert response['data'] == []

    def test_02(self):
        """查询存在的供应商联系人"""
        # 查询供应商列表
        list = request.get('/supplier/dropDownSupplierList')
        # 获取供应商id
        supplierId = list['data'][0]['id']
        # 查询联系人
        response = request.get(self.url + '?supplierId=%d' % supplierId)
        assert response['msg'] == '请求成功'
