# -*- coding: utf-8 -*-
# @Time : 2021/6/1 11:24 上午 
# @Author : lsj
# @File : Warehouse_Management.py
from test_case.common import request, Purchase_Management, PostgresSql


class OutboundOrder:
    keyword = Purchase_Management.AllocateOrder().all()

    # 通过临调单code 获取拣货单id
    def get_out_orderInfo(self, keyword=keyword):
        url = '/outboundOrder/list'
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'keyword': keyword
        }
        response = request.get_params01(url, params)
        data = response['data']['rows'][0]
        outId = data['id']
        pickOrderId = data['pickOrderId']
        return pickOrderId


class PickOrder:

    def get_pick_orderInfo(self, pickOrderId):
        url = '/pickOrder/detail/%s' % pickOrderId

        response = request.get01(url)
        # udi1 = response['data']['goodsDetail'][0]['udi']
        # aa = str(udi1).replace('(', '')
        # udi = str(aa).replace(')', '')
        materialCode = response['data']['goodsDetail'][0]['materialCode']
        warehouseId = response['data']['warehouseId']
        storageLocationId = response['data']['goodsDetail'][0]['storageLocationId']
        quantity = response['data']['goodsDetail'][0]['quantity']
        return materialCode, warehouseId, storageLocationId, quantity

    def get_goodsInfo(self, warehouseId, materialCode):
        url = '/stockBaseData/findAllocateGoodsStockList'
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'warehouseId': warehouseId,
            'keyword': materialCode
        }
        response = request.get_params01(url, params)
        goodsId = response['data']['rows'][0]['goodsId']
        lotNum = response['data']['rows'][0]['lotNum']
        return goodsId, lotNum

    def picking(self, goodsId=None, lotNum=None, pickOrderId=None, storageLocationId=None):
        url = '/pickOrder/picking'
        body = {
            "goodsId": goodsId,
            "lotNum": lotNum,
            "pickOrderId": pickOrderId,
            "serialNumber": None,
            "storageLocationId": storageLocationId
        }
        response = request.put_body01(url, body)

    def pick_approval(self, pickOrderId=None, goodsId=None, quantity=None, kitStockId=None, kitquantity=None
                      , imagePath='http://192.168.10.254:9191/server/file/2021/05/17/5b'
                                  '15b54d-de1f-4aab-ab5b-ffe6bc5a6998/base64Test.jpg'):
        url = '/pickOrder/approval'
        body = {
            "imagePath": imagePath,
            "pickOrderId": pickOrderId,
            "pickingUiBeans": [
                {
                    "goodsId": goodsId,
                    "quantity": quantity
                }
            ]
        }
        kitInfo = {
            "kitStockId": kitStockId,
            "quantity": kitquantity
        }
        if kitStockId:
            body['pickingUiBeans'].append(kitInfo)
        response = request.put_body01(url, body)


if __name__ == '__main__':
    test = OutboundOrder()
    pickOrderId = test.get_out_orderInfo()

    test1 = PickOrder()
    data = test1.get_pick_orderInfo(pickOrderId)
    materialCode = data[0]
    warehouseId = data[1]
    storageLocationId = data[2]
    quantity = data[3]

    goodsInfo = test1.get_goodsInfo(warehouseId, materialCode)
    goodsId = goodsInfo[0]
    lotNum = goodsInfo[1]

    test1.picking(goodsId=goodsId, lotNum=lotNum, pickOrderId=pickOrderId, storageLocationId=storageLocationId)

    test1.pick_approval(goodsId=goodsId, quantity=quantity, pickOrderId=pickOrderId)
