# __author:"zonglr"
# date:2020/12/9
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import time, datetime, jsonpath
from common import logger, request
from faker import Faker
from test_config import param_config

log = logger.Log()
faker = Faker(locale='zh_CN')
# 新增参数type
type = param_config.Ordertpye

# 提交入库单
def submit(adhocOrderId, consumeQuantity):
    # 根据临调单id查询入库单详情(只能查出待入库的单据)
    inbound_detail = request.get('/allocateInboundOrder/getDetailByOrderId?orderId=%s' % adhocOrderId)
    assert inbound_detail['msg'] == '请求成功'

    # 获取入库单id
    allocateInboundOrderId = inbound_detail['data']['allocateInboundOrderId']
    allocateInboundOrderCode = inbound_detail['data']['allocateInboundOrderCode']
    log.info('待入库的单据id %s' % allocateInboundOrderCode)

    # 获取所有的批次号Id和对应的出库数量
    goodsId = jsonpath.jsonpath(inbound_detail, '$..goodsList[*].goodsId')
    goodsLotInfoId = jsonpath.jsonpath(inbound_detail, '$..goodsLotInfoId')
    nums = jsonpath.jsonpath(inbound_detail, '$..quantity')
    log.info('物资id %s' % goodsId)
    log.info('批次号id %s' % goodsLotInfoId)
    log.info('商品出库数量 %s' % nums)
    # 拼接明细
    list = []
    i = 0
    while i < len(goodsId):
        dict = {'goodsId': goodsId[i],
                'goodsLotInfoId': goodsLotInfoId[i],
                'quantity': consumeQuantity}  # 消耗数量
                # 'quantity': nums}  # 消耗数量
        list.append(dict)
        i += 1
    # 提交入库单
    body = {
        'allocateInboundOrderId': allocateInboundOrderId,
        'allocateInboundOrderDetailCheckBeanList': list,
        'type': 'adhoc'
    }
    log.info('传入的参数 %s' % body)
    submit = request.put_body('/allocateInboundOrder/submit', body)
    log.info('响应结果 %s' % submit)
    return submit


# 入库单验收
def check(allocateInboundOrderId, subNum=0,):
    """
    subNum: 待验收数量与实际验收数量的差值
    """
    # 根据入库单id查询明细

    inbound_detail = request.get(
        '/allocateInboundOrder/getDetailById?allocateInboundOrderId=%s&type=%s' % (allocateInboundOrderId,type))
    assert inbound_detail['msg'] == '请求成功'

    # 获取所有的goodsId和对应的出库数量
    goodsId = jsonpath.jsonpath(inbound_detail, '$..goodsId')
    # 批次号id
    goodsLotInfoId = jsonpath.jsonpath(inbound_detail, '$..goodsLotInfoId')
    # 出库数量
    outboundQuantity = jsonpath.jsonpath(inbound_detail, '$..outboundQuantity')
    # 待验收数量
    submitQuantity = jsonpath.jsonpath(inbound_detail, '$..submitQuantity')

    log.info('goodsId %s' % goodsId)
    log.info('批次号id %s' % goodsLotInfoId)
    log.info('商品出库数量 %s' % outboundQuantity)

    # 拼接明细
    list = []
    i = 0
    while i < len(goodsId):
        dict = {'goodsId': goodsId[i],
                'goodsLotInfoId': goodsLotInfoId[i],
                'quantity': submitQuantity[i] - subNum}
        list.append(dict)
        i += 1
    # 验收入库单
    body = {
        'allocateInboundOrderId': allocateInboundOrderId,
        'allocateInboundOrderDetailCheckBeanList': list,
        'type': type
    }
    log.info('传入的参数 %s' % body)
    check = request.put_body('/allocateInboundOrder/check', body)
    log.info('响应结果 %s' % check)
    return check
