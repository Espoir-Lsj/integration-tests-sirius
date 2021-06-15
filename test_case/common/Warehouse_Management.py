# -*- coding: utf-8 -*-
# @Time : 2021/6/1 11:24 上午
# @Author : lsj
# @File : Warehouse_Management.py
import time

from test_case.common import request, Purchase_Management, Order_Management

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
        outCode = data['code']
        pickCode = data['pickOrderCode']
        print('出库单号---------------%s' % outCode)
        print('拣货单号---------------%s' % pickCode)
        return pickOrderId, outOrderId, outCode

    # 出库发货
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

    # 出货审核
    def approval(self, logisticsCompany=None, deliveryDate=None, expressNo=None, outOrderId=None):
        url = '/outboundOrder/approval'
        body = {
            "logisticsCompany": logisticsCompany,
            "deliveryDate": deliveryDate,
            "expressNo": expressNo,
            "id": outOrderId
        }
        response = request.put_body01(url, body)

    # 查询出库单列表
    def get_outOrder_list(self):
        url = '/outboundOrder/list?pageNum=0&pageSize=50'
        response = request.get01(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response

    # 查询 出库单详情
    def get_outOrder_detail(self, outOrderId):
        url = '/outboundOrder/detail/%s' % outOrderId
        response = request.get01(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response


# 拣货单
class PickOrder:

    # 查询拣货单信息
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
    # 查询拣货单信息1
    def get_pick_orderInfo01(self, pickOrderId):
        url = '/pickOrder/detail/%s' % pickOrderId

        response = request.get01(url)
        # udi1 = response['data']['goodsDetail'][0]['udi']
        # aa = str(udi1).replace('(', '')
        # udi = str(aa).replace(')', '')
        materialCode = response['data']['goodsDetail'][0]['materialCode']
        warehouseId = response['data']['warehouseId']
        storageLocationId = response['data']['goodsDetail'][0]['storageLocationId']
        quantity = response['data']['goodsDetail'][0]['quantity']

        return response

    # 查询拣货物资信息
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

    # 拣货
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

    # 完成拣货
    def pickFinished(self, pickOrderId=None,
                     imagePath=["/file/2021/06/03/04a82f82-e0f3-44d7-93f3-964d11c44326/base64Test.jpg]"]):
        url = '/pickOrder/pickFinished'
        body = {
            "pickOrderId": pickOrderId,
            "imagePath": imagePath
        }
        response = request.put_body01(url, body)

    # 审核拣货单
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

    # 查询拣货单列表
    def get_pickOrder_list(self):
        url = '/pickOrder/list?pageNum=0&pageSize=50'
        response = request.get01(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response


# 入库单
class InboundOrder:
    # 获取入库单ID
    def get_inboundOrderId(self, keyword=None):
        url = '/inboundOrder/findList'
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'keyword': keyword
        }
        response = request.get_params01(url, params)
        data = response['data']['rows'][0]
        inboundOrderId = data['inboundOrderId']
        inboundCode = data['inboundOrderCode']
        print('入库单号---------------%s' % inboundCode)
        return inboundOrderId, inboundCode

    # 获取入库单信息
    def get_InboundOrder_Info(self, inboundOrderId=None):
        url = '/inboundOrder/getDetailById?inboundOrderId=%s' % inboundOrderId
        response = request.get01(url)
        data = response['data']['goodsList'][0]
        registrationNum = data['registrationNumList'][0]
        return registrationNum

    # 入库单收货
    def inbound_receiving(self, inboundOrderId=None, goodsId=None, quantity=None, lotNum=None, registrationNum=None,
                          serialNumber=None):
        url = '/inboundOrder/receiving'
        body = {
            "inboundOrderId": inboundOrderId,
            "inboundOrderDetailReceiveBeanList": [{
                "goodsId": goodsId,
                "quantity": quantity,
                "lotNum": lotNum,
                "registrationNum": registrationNum,
                "serialNumber": serialNumber
            }]
        }
        response = request.put_body01(url, body)


# 上架单
class PutOnShelf():
    # 获取上架单号
    def get_putOnShelfId(self, inboundCode):
        """

        :param inboundCode: 入库单code
        :return:
        """
        url = '/putOnShelf/findList?pageNum=0&pageSize=50&keyword=%s' % inboundCode
        response = request.get01(url)
        putOnShelfId = response['data']['rows'][0]['id']
        return putOnShelfId

    # 查询上架单详情
    def get_putOnshelf_detail(self, putOnShelfId):
        """

        :param putOnShelfId: 上架单ID
        :return:
        """
        url = '/putOnShelf/getDetail?orderId=%s' % putOnShelfId
        response = request.get01(url)


# 验收单
class CheckOrder:

    # 获取验收单id
    def get_checkOrder_list(self, inboundCode):
        url = '/checkOrder/list?pageNum=0&pageSize=50&keyword=%s' % inboundCode
        response = request.get01(url)
        checkId = response['data']['rows'][0]['id']
        checkCode = response['data']['rows'][0]['code']
        return checkId, checkCode

    # 获取验收单详情
    def get_checkOrder_Info(self, checkId):
        url = '/checkOrder/detail?orderId=%s' % checkId
        response = request.get01(url)
        checkId = response['data']['checkOrderId']
        goodsList = response['data']['goodsList'][0]
        # 实际收到的数量
        receivedQuantity = goodsList['receivedQuantity']
        # 入库数量
        inboundingQuantity = goodsList['inboundingQuantity']
        goodsLotInfoId = goodsList['goodsLotInfoId']
        goodsId = goodsList['goodsId']
        # 注册证
        registrationNum = goodsList['registrationNumList']
        lotNum = goodsList['lotNum']
        # toolsList = response['data']['toolsList'][0]
        return checkId, goodsLotInfoId, goodsId, lotNum, inboundingQuantity, registrationNum

    def check(self, checkId=None, goodsLotInfoId=None, unqualifiedQuantity=0, goodsId=None, lotNum=None,
              receivedQuantity=None,
              registrationNum=None):
        """

        :param checkId: 验收单号
        :param goodsLotInfoId: 货位ID
        :param unqualifiedQuantity: 未通过数量 默认为0  不需要协商
        :param goodsId: 商品ID
        :param lotNum: 货位
        :param receivedQuantity: 实际收货数量
        :param registrationNum: 注册证号
        :return:
        """
        url = '/checkOrder/check'
        body = {
            "orderId": checkId,
            "inboundOrderDetailCheckBeanList": [{
                "checkInstructionUiList": [],
                "goodsLotInfoId": goodsLotInfoId,
                "unqualifiedQuantity": unqualifiedQuantity,
                "goodsId": goodsId,
                "lotNum": lotNum,
                "quantity": receivedQuantity,
                "registrationNum": registrationNum,
                "serialNumber": None
            }]
        }
        response = request.put_body01(url, body)


# 主流程
class All:
    def __init__(self, keyword):
        self.keyword = keyword
        # 出库单
        self.test = OutboundOrder()
        # 拣货单
        self.test1 = PickOrder()
        # 入库单
        self.test2 = InboundOrder()
        # 验收单
        self.test3 = CheckOrder()

        self.pickOrderId = self.test.get_out_orderInfo(keyword)[0]
        self.outOrderId = self.test.get_out_orderInfo(keyword)[1]

        data = self.test1.get_pick_orderInfo(self.pickOrderId)
        self.materialCode = data[0]
        self.warehouseId = data[1]
        self.storageLocationId = data[2]
        self.quantity = data[3]

        goodsInfo = self.test1.get_goodsInfo(self.warehouseId, self.materialCode)
        self.goodsId = goodsInfo[0]
        self.lotNum = goodsInfo[1]

        # 查询接口
        self.test.get_outOrder_list()
        self.test.get_outOrder_detail(self.outOrderId)

        self.test1.get_pickOrder_list()

    # 拣货出库流程
    def all_pick_out(self):
        # 拣货
        i = 0
        while i < self.quantity:
            self.test1.picking(goodsId=self.goodsId, lotNum=self.lotNum, pickOrderId=self.pickOrderId,
                               storageLocationId=self.storageLocationId)
            i += 1

        # 拣货单 拣货完成
        self.test1.pickFinished(pickOrderId=self.pickOrderId)
        # 拣货单 审核拣货
        self.test1.pick_approval(goodsId=self.goodsId, quantity=self.quantity, pickOrderId=self.pickOrderId)
        # 出库单 发货
        self.test.delivery(logisticsCompany='京东', deliveryDate=timeStamp, expressNo='123123',
                           outOrderId=self.outOrderId,
                           deliveryMode='DELIVERY')
        # 出库单 审核发货
        self.test.approval(logisticsCompany='京东', deliveryDate=timeStamp, expressNo='123123',
                           outOrderId=self.outOrderId)

    # 入库、验收、上架流程
    def all_in_putOnShelf(self):
        inboundOrderId = self.test2.get_inboundOrderId(self.keyword)[0]
        inboundCode = self.test2.get_inboundOrderId(self.keyword)[1]

        registrationNum = self.test2.get_InboundOrder_Info(inboundOrderId)

        # 入库单 收货
        self.test2.inbound_receiving(inboundOrderId=inboundOrderId, goodsId=self.goodsId, quantity=self.quantity,
                                     lotNum=self.lotNum,
                                     registrationNum=registrationNum)

        checkId = self.test3.get_checkOrder_list(inboundCode)[0]
        checkCode = self.test3.get_checkOrder_list(inboundCode)[1]
        data = self.test3.get_checkOrder_Info(checkId)
        #     checkId, goodsLotInfoId, goodsId, lotNum, receivedQuantity, registrationNum
        goodsLotInfoId = data[1]
        goodsId = data[2]
        lotNum = data[3]
        inboundingQuantity = data[4]
        registrationNum = data[5]
        # 验收单 验收
        self.test3.check(checkId=checkId, goodsLotInfoId=goodsLotInfoId, goodsId=goodsId, lotNum=lotNum,
                         receivedQuantity=inboundingQuantity, registrationNum=str(registrationNum))


if __name__ == '__main__':
    test = CheckOrder()
    checkId = test.get_checkOrder_list('OIO_20210615_0014')[0]
    checkCode = test.get_checkOrder_list('OIO_20210615_0014')[1]
    data = test.get_checkOrder_Info(checkId)
    #     checkId, goodsLotInfoId, goodsId, lotNum, receivedQuantity, registrationNum
    goodsLotInfoId = data[1]
    goodsId = data[2]
    lotNum = data[3]
    receivedQuantity = data[4]
    registrationNum = data[5]
    test.check(checkId=checkId, goodsLotInfoId=goodsLotInfoId, goodsId=goodsId, lotNum=lotNum,
               receivedQuantity=receivedQuantity, registrationNum=str(registrationNum))
