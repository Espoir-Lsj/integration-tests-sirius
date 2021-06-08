# -*- coding: utf-8 -*-
# @Time : 2021/6/1 11:24 上午
# @Author : lsj
# @File : Warehouse_Management.py
import time

from test_case.common import request, Purchase_Management

timeStamp = int(time.time() * 1000)


# 出库单
class OutboundOrder:

    # 通过临调单code 获取拣货单id
    def get_out_orderInfo(self, keyword=None):
        url = '/outboundOrder/list'
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'keyword': keyword
        }
        response = request.get_params01(url, params)
        data = response['data']['rows'][0]
        pickOrderId = data['pickOrderId']
        outOrderId = data['id']
        return pickOrderId, outOrderId

    def delivery(self, logisticsCompany=None, deliveryDate=None, expressNo=None, outOrderId=None, deliveryMode=None):
        url = '/outboundOrder/delivery'
        body = {
            "logisticsCompany": logisticsCompany,
            "deliveryDate": deliveryDate,
            "expressNo": expressNo,
            "id": outOrderId,
            "deliveryMode": deliveryMode
        }
        response = request.put_body01(url, body)

    def approval(self, logisticsCompany=None, deliveryDate=None, expressNo=None, outOrderId=None):
        url = '/outboundOrder/approval'
        body = {
            "logisticsCompany": logisticsCompany,
            "deliveryDate": deliveryDate,
            "expressNo": expressNo,
            "id": outOrderId
        }
        response = request.put_body01(url, body)


# 拣货单
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
        try:
            response['msg'] == '请求成功'
        except Exception:
            raise response

    def pickFinished(self, pickOrderId=None,
                     imagePath=["/file/2021/06/03/04a82f82-e0f3-44d7-93f3-964d11c44326/base64Test.jpg]"]):
        url = '/pickOrder/pickFinished'
        body = {
            "pickOrderId": pickOrderId,
            "imagePath": imagePath
        }
        response = request.put_body01(url, body)

    def pick_approval(self, pickOrderId=None, goodsId=None, quantity=None, kitStockId=None, kitquantity=None
                      , imagePath=["/file/2021/06/03/04a82f82-e0f3-44d7-93f3-964d11c44326/base64Test.jpg"]):
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


# 入库单
class InboundOrder:
    def get_in_OrderInfo(self, keyword=None):
        url = '/inboundOrder/findList'
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'keyword': keyword
        }
        response = request.get_params01(url, params)
        data = response['data']['rows'][0]
        inboundOrderId = data['inboundOrderId']
        return inboundOrderId


# 上架单
class putOnShelf:
    pass


# 主流程
def all(keyword=None):
    """

    :param keyword: 关联单号
    :return:
    """
    #
    # test = OutboundOrder()
    #
    # pickOrderId = test.get_out_orderInfo(keyword)[0]
    # outOrderId = test.get_out_orderInfo(keyword)[1]
    #
    test1 = PickOrder()
    # data = test1.get_pick_orderInfo(pickOrderId)
    # materialCode = data[0]
    # warehouseId = data[1]
    # storageLocationId = data[2]
    # quantity = data[3]
    #
    # goodsInfo = test1.get_goodsInfo(warehouseId, materialCode)
    # goodsId = goodsInfo[0]
    # lotNum = goodsInfo[1]
    # # 拣货
    # test1.picking(goodsId=goodsId, lotNum=lotNum, pickOrderId=pickOrderId, storageLocationId=storageLocationId)
    # # 拣货完成
    # test1.pickFinished(pickOrderId=pickOrderId)
    # print(pickOrderId)
    # 审核拣货
    # test1.pick_approval(goodsId=goodsId, quantity=quantity, pickOrderId=pickOrderId)
    # 发货
    # test.delivery(logisticsCompany='京东', deliveryDate=timeStamp, expressNo='123123', outOrderId=outOrderId,
    #               deliveryMode='DELIVERY')
    # # 审核发货
    # test.approval(logisticsCompany='京东', deliveryDate=timeStamp, expressNo='123123', outOrderId=outOrderId)


if __name__ == '__main__':
    keyword = Purchase_Management.AllocateOrder().all()
    print(keyword)
    all(keyword)

    # test = OutboundOrder()
    #
    # pickOrderId = test.get_out_orderInfo(keyword)[0]
    # outOrderId = test.get_out_orderInfo(keyword)[1]
    #
    # test1 = PickOrder()
    # data = test1.get_pick_orderInfo(pickOrderId)
    # materialCode = data[0]
    # warehouseId = data[1]
    # storageLocationId = data[2]
    # quantity = data[3]
    #
    # goodsInfo = test1.get_goodsInfo(warehouseId, materialCode)
    # goodsId = goodsInfo[0]
    # lotNum = goodsInfo[1]
    # # 拣货
    # test1.picking(goodsId=goodsId, lotNum=lotNum, pickOrderId=pickOrderId, storageLocationId=storageLocationId)
    # # 拣货完成
    # test1.pickFinished(pickOrderId=pickOrderId)
    # # 审核拣货
    # test1.pick_approval(goodsId=goodsId, quantity=quantity, pickOrderId=pickOrderId)
    # # 发货
    # test.delivery(logisticsCompany='京东', deliveryDate=timeStamp, expressNo='123123', outOrderId=outOrderId,
    #               deliveryMode='DELIVERY')
    # # # 审核发货
    # test.approval(logisticsCompany='京东', deliveryDate=timeStamp, expressNo='123123', outOrderId=outOrderId)
