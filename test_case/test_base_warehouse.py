# __author:"zonglr"
# date:2020/11/28
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

import pytest
from common import request, logger

log = logger.Log()


class TestGetAll:
    """查询所有仓库"""

    url = '/warehouse/getAll'

    def test_01(self):
        """查询所有仓库"""
        response = request.get(self.url)
        assert response['msg'] == '请求成功'
