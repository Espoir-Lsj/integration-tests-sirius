# -*- coding: utf-8 -*-
# @Time : 2021/4/8 12:41 下午 
# @Author : lsj
# @File : accept.py
import jsonpath

from common import request


def success(id, deliveryMode='DELIVERY', warehouseId=6, goodsId=None, quantity=None, kitTemplateId=None, Tquantity=1):
    body = {
        "detail": [
            {
                "deliveryMode": deliveryMode,
                "goodsDetailUiBeans": [],
                "toolsDetailUiBeans": [],
                "warehouseId": warehouseId
            }
        ],
        "id": id
    }
    if goodsId != None:
        goods = {
            "goodsId": goodsId,
            "quantity": quantity
        }
        body['detail'][0]['goodsDetailUiBeans'] = [goods]

    if kitTemplateId != None:
        tools = {

            "kitTemplateId": kitTemplateId,
            "quantity": Tquantity

        }
        body['detail'][0]['toolsDetailUiBeans'] = [tools]
    success = request.put_body('/adhocOrder/accept', body=body)

    return success


# 判断 审核内容： 物资 + 工具包 、物资 、工具包    根据不同情况传参数
def check(adhocOrderId):
    response = request.get('/adhocOrder/getDetailByOrderId?orderId=%s' % adhocOrderId)

    goodsList = response['data']['childUiList'][0]['detailBeanUiList']
    toolsList = response['data']['childUiList'][0]['toolsKitUiBeans']
    deliveryMode = response['data']['adhocOrderUiBean']['deliveryMode']
    warehouseId = response['data']['adhocOrderUiBean']['sourceWarehouse']

    goodsId = jsonpath.jsonpath(goodsList, '$..[*].goodsId')
    quantity = jsonpath.jsonpath(goodsList, '$..[*].quantity')
    kitTemplateId = jsonpath.jsonpath(toolsList, '$..[*].id')
    goods = []
    tools = []

    if goodsId:
        i = 0
        while i < len(goodsId):
            dict = {
                "goodsId": goodsId[i],
                "quantity": quantity[i],
            }
            goods.append(dict)
            i += 1
            if kitTemplateId:
                j = 0
                while j < len(kitTemplateId):
                    dict1 = {
                        "kitTemplateId": kitTemplateId[j],
                        "quantity": 1
                    }
                    tools.append(dict1)
                    j += 1
                body = {
                    "detail": [
                        {
                            "deliveryMode": deliveryMode,
                            "goodsDetailUiBeans": goods,
                            "toolsDetailUiBeans": tools,
                            "warehouseId": warehouseId
                        }
                    ],
                    "id": adhocOrderId
                }
            else:
                body = {
                    "detail": [
                        {
                            "deliveryMode": deliveryMode,
                            "goodsDetailUiBeans": goods,
                            "warehouseId": warehouseId
                        }
                    ],
                    "id": adhocOrderId
                }
    elif kitTemplateId:
        j = 0
        while j < len(kitTemplateId):
            dict1 = {
                "kitTemplateId": kitTemplateId[j],
                "quantity": 1
            }
            tools.append(dict1)
            j += 1
        body = {
            "detail": [
                {
                    "deliveryMode": deliveryMode,
                    "toolsDetailUiBeans": tools,
                    "warehouseId": warehouseId
                }
            ],
            "id": adhocOrderId
        }
    else:
        body = {
            "detail": [
                {
                    "deliveryMode": deliveryMode,
                    "warehouseId": warehouseId
                }
            ],
            "id": adhocOrderId
        }

    check = request.put_body('/adhocOrder/accept', body=body)
    return check


def reject(id, reason=None):
    body = {
        "id": id,
        "reason": reason
    }
    reject = request.put_body('/adhocOrder/reject', body=body)

    return reject
