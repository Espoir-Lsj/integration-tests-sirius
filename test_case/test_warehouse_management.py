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

    @allure.story('拣货单——拣货单 完成拣货')
    @allure.title('上传图片过多')
    def test_pickFinished01(self, PickOrder_picking02):
        url = '/pickOrder/pickFinished'
        body = {
            "pickOrderId": PickOrder_picking02,
            "imagePath": ["/file/2021/06/15/0a9dcc89-f831-4b48-a5c4-2f05b8701868/base64Test.jpg",
                          "/file/2021/06/15/e9c93cc7-66d1-4e50-b9a3-75cd71581632/base64Test.jpg",
                          "/file/2021/06/15/d6dfc69f-dbe7-4c64-b349-f3d8c574cbbf/base64Test.jpg",
                          "/file/2021/06/15/233799c3-3b28-4639-ab63-aa6fe7125376/base64Test.jpg",
                          "/file/2021/06/15/82aad064-47cd-4c17-a000-84f32264a5f0/base64Test.jpg",
                          "/file/2021/06/15/a94e64a4-02ec-4439-93c7-dceb6d92be74/base64Test.jpg",
                          "/file/2021/06/15/6cab9b68-b6fa-4fa4-a464-783f0664c489/base64Test.jpg",
                          "/file/2021/06/15/ae46f0fc-ff45-4dcd-badc-0f6944a5a14c/base64Test.jpg",
                          "/file/2021/06/15/94561ab6-4456-44c1-85d9-2aa47537a7bd/base64Test.jpg",
                          "/file/2021/06/15/94561ab6-4456-44c1-85d9-2aa47537a7bd/base64Test.jpg",
                          "/file/2021/06/15/0d5d89e6-2d30-4db5-96fc-ef7743399af7/base64Test.jpg"]
        }
        response = request.put_body01(url, body)
        assert response['msg'] == '上传的图片不能超过10张'

    data = get_datas.get_csv('/pickOrder/approval')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('拣货单——拣货单 审核拣货')
    @allure.title('{title}')
    def test_pickApproval(self, url, title, case, expected, PickOrder_pick_approval, PickOrder_picking02):
        body = request.body_replace(url, case)
        response = request.put_body01(url, body)
        assert response['msg'] == expected

    @allure.story('拣货单——拣货单 审核拣货')
    @allure.title('商品不存在')
    def test_pickApproval01(self, PickOrder_pickFinish02):
        url = '/pickOrder/approval'
        body = {
            "imagePath": ["/file/2021/06/03/04a82f82-e0f3-44d7-93f3-964d11c44326/base64Test.jpg"],
            "pickOrderId": PickOrder_pickFinish02[0],
            "pickingUiBeans": [{
                "goodsId": PickOrder_pickFinish02[1],
                "quantity": 0
            }]
        }
        response = request.put_body01(url, body)
        assert response['msg'] == '物资【锁定接骨板】待拣数量和审核数量不一致，请刷新后重试'

    data = get_datas.get_csv('/outboundOrder/delivery')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('出库单——出库发货')
    @allure.title('{title}')
    def test_outOrderDelivery(self, url, title, case, expected, OutboundOrder_delivery, OutboundOrder_getId):
        if title in ('物流公司为空', '物流单号为空', '发货日期为空'):
            body = request.body_replace(url, case)
            body['id'] = OutboundOrder_getId
            response = request.put_body01(url, body)
            assert response['msg'] == expected

    data = get_datas.get_csv('/outboundOrder/approval')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('出库单——出库发货')
    @allure.title('{title}')
    def test_outOrderApproval(self, url, title, case, expected, OutboundOrder_approve, OutboundOrder_getId01):
        if title == '物流单号为空':
            body = request.body_replace(url, case)
            body['id'] = OutboundOrder_getId01
            response = request.put_body01(url, body)
            assert response['msg'] == expected

    data = get_datas.get_csv('/inboundOrder/receiving')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('入库单——入库收货')
    @allure.title('{title}')
    def test_inOrderReceiving(self, url, title, case, expected, InboundOrder_receiving, OutboundOrder_approve01):
        if title == '商品错误':
            body = request.body_replace(url, case)
            body['inboundOrderId'] = OutboundOrder_approve01
            response = request.put_body01(url, body)
            assert response['msg'] == expected

    data = get_datas.get_csv('/putOnShelf/putOnShelf')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('上架单单——上架')
    @allure.title('{title}')
    def test_putOnShelf(self, url, title, case, expected, PutOnShelf_put, InboundOrder_receiving01):
        if title in ('商品错误', '商品数量错误', '货位号为空', '货位号错误'):
            body = request.body_replace(url, case)
            body['orderId'] = InboundOrder_receiving01
            response = request.post_body01(url, body)
            assert response['msg'] == expected

    def test1111(self, CheckOrder_check, PutOnShelf_put01):
        pass
