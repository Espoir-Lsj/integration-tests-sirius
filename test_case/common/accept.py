# -*- coding: utf-8 -*-
# @Time : 2021/4/8 12:41 下午 
# @Author : lsj
# @File : accept.py
from common import request


def success(id, deliveryMode='DELIVERY', warehouseId=6, goodsId=0, quantity=None, kitTemplateId=None, Tquantity=1):
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


def reject(id, reason=None):
    body = {
        "id": id,
        "reason": reason
    }
    reject = request.put_body('/adhocOrder/reject', body=body)

    return reject
