# __author:"zonglr"
# date:2020/12/8
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, datetime, time
from common import params, request, logger, accept, outboundOrder
from faker import Faker
from common import adhocOrder, outboundOrder, pick
from test_config import param_config

log = logger.Log()


# 创建一个入库单

@pytest.fixture(scope="module")
def createInboundOrder():
    # 创建临调单
    create = adhocOrder.createAdhocOrder(param_config.goodsId)
    try:
        assert create['msg'] == "请求成功"
    except:
        raise Exception(create['msg'], create['exMsg'])
        # 保存临调单id，code
    adhocOrderId = create['data']['id']
    log.info('生成的临调单id: %s' % adhocOrderId)
    adhocOrderCode = create['data']['code']
    log.info('生成的临调单code: %s' % adhocOrderCode)
    # 接收临调单
    success = accept.check(adhocOrderId)
    try:
        assert success['msg'] == "请求成功"
    except:
        raise Exception(success['msg'], success['exMsg'])
    log.info('临调单接收成功 %s' % success)
    # 根据临调单code查询拣货单id
    getList = request.get(
        '/allocateOutboundOrder/list?pageNum=0&pageSize=20&keyword=%s' % adhocOrderCode)
    assert getList['msg'] == '请求成功'
    # 保存拣货单id
    pickOrderId = getList['data']['rows'][0]['pickOrderId']
    log.info('生成的拣货单id: %s' % pickOrderId)
    # 拣货
    pick_response = pick.finishPick(pickOrderId)
    assert pick_response['msg'] == '请求成功'
    # # 根据keyword查询列表详情
    # getList = request.get(
    #     '/allocateOutboundOrder/list?pageNum=0&pageSize=20&keyword=%s' % adhocOrderCode)
    # # 出库单id
    # outboundOrderId = getList['data']['rows'][0]['id']

    # 审核发货
    approval = outboundOrder.approval(adhocOrderCode)
    assert approval['msg'] == '请求成功'
    #
    # # 入库单id
    # response = request.get('/allocateInboundOrder/getDetailByOrderId?orderId=%s' % adhocOrderId)
    # assert response['msg'] == '请求成功'
    # allocateInboundOrderId = response['data']['allocateInboundOrderId']
    # # goodsLotInfoId = response['data']['goodsList'][0]['infoList'][0]['goodsLotInfoId']
    # log.info('入库单ID %s' % allocateInboundOrderId)
    return adhocOrderId


# 提交消耗明细
def submit(adhocOrderId, quantity=0):
    response = request.get('/allocateInboundOrder/getDetailByOrderId?orderId=%s' % adhocOrderId)
    assert response['msg'] == '请求成功'
    goodsId = response['data']['goodsList'][0]['goodsId']
    log.info('商品---------------%s' % goodsId)
    goodsLotInfoId = response['data']['goodsList'][0]['infoList'][0]['goodsLotInfoId']
    log.info(goodsLotInfoId)

    allocateInboundOrderId = response['data']['allocateInboundOrderId']
    # quantity = response['data']['goodsList'][0]['infoList'][0]['quantity']
    body = {
        "allocateInboundOrderDetailCheckBeanList": [
            {
                "goodsId": goodsId,
                "goodsLotInfoId": goodsLotInfoId,
                "quantity": quantity
            }
        ],
        "allocateInboundOrderId": allocateInboundOrderId,
        "type": "adhoc"
    }
    response1 = request.put_body('/allocateInboundOrder/submit', body=body)
    log.info('提交销用成功 %s' % response1)
    return response1


def check(allocateInboundOrderId, quantity):
    response = request.get('/allocateInboundOrder/getDetailByOrderId?orderId=%s' % allocateInboundOrderId)
    assert response['msg'] == ['请求成功']
    goodsId = response['data']['goodsList'][0]['goodsId']

    goodsLotInfoId = response['data']['goodsList'][0]['infoList'][0]['goodsLotInfoId']
    # quantity = response['data']['goodsList'][0]['infoList'][0]['quantity']
    body = {
        {
            "allocateInboundOrderDetailCheckBeanList": [
                {
                    "goodsId": goodsId,
                    "goodsLotInfoId": goodsLotInfoId,
                    "quantity": quantity
                }
            ],
            "allocateInboundOrderId": allocateInboundOrderId,
            "type": "adhoc"
        }
    }
    response1 = request.put_body('/allocateInboundOrder/check', body=body)
    return response1


class TestSumbit:
    """调拨出库单发货信息"""

    def test_01_sum(self, createInboundOrder):
        """销用数量大于临调数量"""
        response = submit(createInboundOrder, 99)
        # log.info('响应结果 %s' % response)
        assert response['msg'] == '提交数量不能大于出库数量'
