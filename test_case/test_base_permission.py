# __author:"zonglr"
# date:2020/11/28
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, jsonpath
from common import logger, request

log = logger.Log()


class TestDetail:
    """根据id获取权限详情"""
    url = '/permission/{id}'

    def test_01(self):
        """查询不存在的权限id"""
        response = request.get(self.url.format(id=0))
        assert response['msg'] == '权限不存在'

    def test_02(self):
        """权限id为空"""
        response = request.get(self.url.format(id=None))
        assert response['msg'] == '请求参数异常'

    def test_03(self):
        """查询存在的权限id"""
        response = request.get(self.url.format(id=1))
        assert response['msg'] == '请求成功'


class TestGetUserMenus:
    """获取用户可访问的菜单"""
    url = '/permission/getUserMenus'

    def test_01(self):
        """正常查询"""
        response = request.get(self.url)
        assert response['msg'] == '请求成功'
        assert len(response['data']) > 0


class TestGetUserPermission:
    """获取用户的权限信息"""
    url = '/permission/getUserPermission'

    def test_01(self):
        """正常查询"""
        response = request.get(self.url)
        assert response['msg'] == '请求成功'
        assert len(response['data']) > 0

