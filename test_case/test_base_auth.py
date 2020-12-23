# __author:"zonglr"
# date:2020/11/28
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, requests, urllib3
from common import logger, request, login
from test_config import param_config

urllib3.disable_warnings()
log = logger.Log()


class TestGetCaptcha:
    """获取图形验证码"""
    url = '/auth/getCaptcha'

    def test_01(self):
        """获取图形验证码"""
        response = request.get(self.url)
        assert response['msg'] == '请求成功'
        assert response['data'] != None


class TestLogin:
    """登录"""
    url = '/auth/login'

    def test_01(self):
        """用户名错误"""
        response = login.login('000', '123')
        assert response['msg'] == '用户名或者密码错误'
