# -*- coding: utf-8 -*-
# @Time : 2021/6/3 10:52 上午 
# @Author : lsj
# @File : test_warehouse_management.py
import allure
import pytest

from test_case.common import Data_driven, request

get_datas = Data_driven.CsvData()


@allure.feature('仓库管理——拣货单')
class TestPickOrder:
    data = get_datas.get_csv('/pickOrder/picking')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('拣货单——拣货单 拣货')
    @allure.title('{title}')
    def test_picking(self, url, title, case, expected, PickOrder_get_pickOrderId, PickOrder_picking):
        body = request.body_replace(url, case)
        response = request.put_body01(url, body)
        assert response['msg'] == expected

    data = get_datas.get_csv('/pickOrder/pickFinished')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('拣货单——拣货单 完成拣货')
    @allure.title('{title}')
    def test_pickFinished(self, url, title, case, expected, PickOrder_pickFinished):
        body = request.body_replace(url, case)
        response = request.put_body01(url, body)
        assert response['msg'] == expected

    def test_pickApproval(self, PickOrder_pick_approval):
        pass
