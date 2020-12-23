# __author:"zonglr"
# date:2020/12/11
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest
from common import request, logger

log = logger.Log()


class TestGetChildren:
    """查询某个区域下的所有子区域"""
    url = ''

    def test_01(self):
        """areaCode为0时，返回所有省份"""
        response = request.get('/district/getChildren/0')
        # 判断响应data非空
        assert response['data'] != None

    def test_02(self):
        """areaCode输入北京的区域代码"""
        response = request.get('/district/getChildren/110000000000')
        log.info(response)
        # 判断响应data非空
        assert response['data'] != None


class TestReversePosition:
    """逆地址解析"""
    url = '/district/reversePosition'

    def test_01(self):
        """查询正确的经纬度"""
        params = {
            'lng': 116.58114899609373,
            'lat': 39.74990554421901
        }
        response = request.get_params(self.url, params=params)
        log.info(response)
        # 判断响应data非空
        assert response['data'] != None

    def test_02(self):
        """参数值为空"""
        params = {
            'lng': None,
            'lat': None
        }
        response = request.get_params(self.url, params=params)
        log.info(response)
        assert response['msg'] == '请求参数异常'


class TestTree:
    """返回树形结构的省市区"""

    def test_01(self):
        """查询"""
        response = request.get('/district/tree')
        # 判断响应data非空
        assert response['data'] != None
