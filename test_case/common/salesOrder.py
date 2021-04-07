# __author:"zonglr"
# date:2020/12/9
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import json
import time, datetime, jsonpath
from common import logger, request
from faker import Faker

log = logger.Log()
faker = Faker(locale='zh_CN')


# 生成销售单
def check(adhocOrderId, subNum=0):
    """
    subNum: 协商数量与实际消耗数量的差值
    """
    # 查询临调单明细
    detail = request.get('/salesOrder/getDetailByAdhocId?adhocId=%s' % adhocOrderId)
    # if detail['data']['mainList'] == None and len(detail['data']['toolsList']) == 0:
    # 消耗明细为空
    if detail['data']['goodsList'] == None and detail['data']['toolsList'] == None:
        # 提交
        i = 0

        body = {
            "createUiBeans": [
                {
                    "adhocOrderId": adhocOrderId,
                    "detailUiBeanList": []
                }
            ],
            "parentId": adhocOrderId
        }

        # check = request.post_body('/salesOrder/checkSalesOrder', body=body)
        check = request.post_body('/salesOrder/createSalesOrder', body=body)
        assert check['msg'] == '请求成功'
        # log.info('响应结果22 %s' % check)
        log.info('响应结果%s' % check)

    # 消耗明细不为空
    else:
        # 耗材明细
        goodsIds = jsonpath.jsonpath(detail, '$..goodsId')
        quantity = jsonpath.jsonpath(detail, '$..receivedSaleQuantity')
        goodsLotInfoId = jsonpath.jsonpath(detail, '$..goodsLotInfoId')
        # 拼接明细
        detailUiBeanList = []
        i = 0
        while i < len(goodsIds):
            dict = {'goodsId': goodsIds[i], 'quantity': quantity[i] - subNum, 'goodsLotInfoId': goodsLotInfoId[i]}
            detailUiBeanList.append(dict)
            i += 1

        # 提交
        body = {
            "createUiBeans": [
                {
                    "adhocOrderId": adhocOrderId,
                    "detailUiBeanList": detailUiBeanList
                }
            ],
            "parentId": adhocOrderId
        }
        check = request.post_body('/salesOrder/checkSalesOrder', body=body)
        # 提示生成入库单，提交
        if check['msg'] == '请求成功' and check['data'] != None:
            log.info('------提交生成销售单的入库单------')
            # response = request.post_body('/salesOrder/createInboundOrder', body=body)
            response = request.post_body('/salesOrder/createSalesOrder', body=body)
            assert response['msg'] == '请求成功'
        log.info('响应结果%s' % check)
        return check
