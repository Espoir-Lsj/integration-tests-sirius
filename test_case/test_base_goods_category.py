# __author:"zonglr"
# date:2020/12/11
#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, time
from common import logger, request
from test_config import param_config

log = logger.Log()

class TestAddCategory:
    """新增商品分类"""
    url = '/goodsCategory/addGoodsCategory'

    def test_01(self):
        body = {
            'categoryIds': [0],
            'goodsId': 0
        }
        response = request.post_body(self.url, body=body)
        assert response['msg'] == '该商品不存在'

    def test_02(self):
        body = {
            'categoryIds': [0],
            'goodsId': param_config.goodsId
        }
        response = request.post_body(self.url, body=body)