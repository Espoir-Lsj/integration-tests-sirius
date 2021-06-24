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

    # 查询出库单发货信息
    def get_outOrder_deliveryInfo(self, outOrderId):
        url = '/outboundOrder/deliveryInfo/%s' % outOrderId
        response = request.get01(url)

    def outOrder_print(self, outOrderId):
        url = '/outboundOrder/print/{}?id={}'.format(outOrderId, outOrderId)
        response = request.get01(url)

    def get_outOrder_adress(self, outOrderId):
        url = '/outboundOrder/getAddress?outboundOrderId=%s' % outOrderId
        response = request.get01(url)


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

    # 查询拣货单信息1 前置条件用
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

    # 多物资拣货
    def pick_goods(self, pickOrderId):
        url = '/pickOrder/detail/%s' % pickOrderId
        quantityList = []
        goodsIdList = []
        lotNumList = []
        storageLocationIdList = []
        res = request.get01(url)
        warehouseId = res['data']['warehouseId']
        for i in res['data']['goodsDetail']:
            storageLocationId = i['storageLocationId']
            quantity = i['quantity']
            goodsId = i['goodsId']
            lotNum = i['lotNum']
            storageLocationIdList.append(storageLocationId)
            quantityList.append(quantity)
            goodsIdList.append(goodsId)
            lotNumList.append(lotNum)
        url = '/pickOrder/picking'
        for goodsId, lotNum, storageLocationId, quantity in zip(goodsIdList, lotNumList, storageLocationIdList,
                                                                quantityList):
            body = {
                "goodsId": goodsId,
                "lotNum": lotNum,
                "pickOrderId": pickOrderId,
                "serialNumber": None,
                "storageLocationId": storageLocationId
            }
            for i in range(quantity):
                response = request.put_body01(url, body)
        pickingUiBeans = []
        for goodsId, quantity in zip(goodsIdList, quantityList):
            goods = {
                "goodsId": goodsId,
                "quantity": quantity
            }
            pickingUiBeans.append(goods)
        return pickingUiBeans

    # 工具包拣货
    def pick_tools(self, pickOrderId):
        url = '/pickOrder/detail/%s' % pickOrderId
        response = request.get01(url)
        operatorBarcode = response['data']['toolsKitDetail']
        pickingUiBeansList = []
        for i in operatorBarcode:
            body = {
                "code": i['operatorBarcode'],
                "pickOrderId": pickOrderId,
                "storageLocationId": i['storageLocationId']
            }
            response1 = self.picking_bycode(body)
            pickingUiBeans = {
                "kitStockId": i['kitStockId'],
                "quantity": i['quantity']
            }
            pickingUiBeansList.append(pickingUiBeans)
        return pickingUiBeansList

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

    # 拣货
    def picking_bycode(self, code=None, pickOrderId=None, storageLocationId=None):
        url = '/pickOrder/pickingByCode'
        body = {
            "code": code,
            "pickOrderId": pickOrderId,
            "storageLocationId": storageLocationId
        }
        response = request.put_body01(url, body)

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
    def pick_approval(self, pickingUiBeans=list(), pickOrderId=None, goodsId=None, quantity=None, kitStockId=None,
                      kitquantity=None
                      , imagePath=["/file/2021/06/03/04a82f82-e0f3-44d7-93f3-964d11c44326/base64Test.jpg"]):
        url = '/pickOrder/approval'
        body = {
            "imagePath": imagePath,
            "pickOrderId": pickOrderId,
            "pickingUiBeans": pickingUiBeans
        }

        goods = {
            "goodsId": goodsId,
            "quantity": quantity

        }

        kitInfo = {
            "kitStockId": kitStockId,
            "quantity": kitquantity
        }

        if goodsId:
            body['pickingUiBeans'] = [goods]

        if kitStockId:
            body['pickingUiBeans'] = [kitInfo]
        response = request.put_body01(url, body)

    # 查询拣货单列表
    def get_pickOrder_list(self):
        url = '/pickOrder/list?pageNum=0&pageSize=50'
        response = request.get01(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response

    # pda获取拣货单详情
    def get_pda_detail(self, pickOrderId):
        url = '/pickOrder/detailByPda/%s' % pickOrderId
        response = request.get01(url)

    # 解析gs1
    def get_gs1(self, pickOrderId):
        url = '/pickOrder/gs1Decode?code=010761181981206217781117104135392&id=%s' % pickOrderId
        response = request.get01(url)

    #
    def pickOrder_print(self, pickOrderId):
        url = '/pickOrder/detail/{}?id={}'.format(pickOrderId, pickOrderId)
        response = request.get01(url)

    def get_byCode(self, pickOrderId):
        url = '/pickOrder/pickingByCode'
        body = {
            "code": "20538",
            "pickOrderId": pickOrderId,
            "storageLocationId": 0
        }
        response = request.put_body01(url, body)


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
        data = response['data']['goodsList']
        data1 = response['data']['toolsList']
        if len(data) > 0:
            for i in data:
                registrationNum = i['registrationNumList'][0]
                inboundingQuantity = i['inboundingQuantity']
                goodsId = i['goodsId']
                lotNum = i['lotNum']
                return registrationNum, inboundingQuantity, goodsId, lotNum
        elif len(data1) > 0:
            for j in data1:
                for i in j['goodsList']:
                    registrationNum = i['registrationNumList'][0]
                    inboundingQuantity = i['inboundingQuantity']
                    goodsId = i['goodsId']
                    lotNum = i['lotNum']

                    return registrationNum, inboundingQuantity, goodsId, lotNum

    # 获取入库单信息
    def get_InboundOrder_Infos(self, inboundOrderId=None):
        url = '/inboundOrder/getDetailById?inboundOrderId=%s' % inboundOrderId
        response = request.get01(url)
        data = response['data']['goodsList']
        data1 = response['data']['toolsList']
        inboundOrderDetailReceiveBeanList = []
        if len(data) > 0:
            for i in data:
                goods = {
                    "goodsId": i['goodsId'],
                    "quantity": i['inboundingQuantity'],
                    "lotNum": i['lotNum'],
                    "registrationNum": i['registrationNumList'][0],
                    "serialNumber": None
                }
                inboundOrderDetailReceiveBeanList.append(goods)
        if len(data1) > 0:
            for j in data1:
                kitStockId = j['kitStockId']
                for i in j['goodsList']:
                    goods1 = {
                        "goodsId": i['goodsId'],
                        "kitStockId": kitStockId,
                        "quantity": i['inboundingQuantity'],
                        "lotNum": i['lotNum'],
                        "registrationNum": i['registrationNumList'][0],
                        "serialNumber": None
                    }
                    inboundOrderDetailReceiveBeanList.append(goods1)
        return inboundOrderDetailReceiveBeanList

    # 入库单收货
    def inbound_receiving(self, inboundOrderId=None, goodsId=None, quantity=None, lotNum=None, registrationNum=None,
                          serialNumber=None, inboundOrderDetailReceiveBeanList=list()):
        url = '/inboundOrder/receiving'
        body = {
            "inboundOrderId": inboundOrderId,
            "inboundOrderDetailReceiveBeanList": inboundOrderDetailReceiveBeanList
        }
        if goodsId:
            goods = {
                "goodsId": goodsId,
                "quantity": quantity,
                "lotNum": lotNum,
                "registrationNum": registrationNum,
                "serialNumber": serialNumber
            }
            body['inboundOrderDetailReceiveBeanList'] = [goods]
        response = request.put_body01(url, body)

    # 获取入库单列表
    def get_inbound_list(self):
        url = '/inboundOrder/findList?pageNum=0&pageSize=50'
        response = request.get01(url)

    # 导出入库单
    def inbound_export(self):
        url = '/inboundOrder/export'
        response = request.get01(url)


# 上架单
class PutOnShelf:
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
        data = response['data']['goodsList'][0]
        goodsId = data['goodsId']
        goodsLotInfoId = data['goodsLotInfoId']
        storageLocationCode = str(data['storageLocationCode'])
        quantity = data['quantity']
        putOnShelfCode = response['data']['code']
        goodsList = data = response['data']['goodsList']
        print('上架单号---------------%s' % putOnShelfCode)
        putOnShelfId = putOnShelfId
        return goodsId, goodsLotInfoId, storageLocationCode, quantity, putOnShelfId, goodsList

    # 多物资 上架单信息
    def get_putOnshelf_details(self, putOnShelfId):
        url = '/putOnShelf/getDetail?orderId=%s' % putOnShelfId
        response = request.get01(url)
        putOnShelfCode = response['data']['code']
        print('上架单号---------------%s' % putOnShelfCode)

        goodsList = []
        toolsList = []
        data = response['data']['goodsList']
        data1 = response['data']['toolsList']
        if len(data) > 0:
            for i in data:
                goods = {
                    "goodsId": i['goodsId'],
                    "goodsLotInfoId": i['goodsLotInfoId'],
                    "quantity": i['quantity'],
                    "storageLocationCode": i['storageLocationCode'],
                    "supplierId": None
                }
                goodsList.append(goods)
        if len(data1) > 0:
            for j in data1:
                goods1 = {
                    "kitStockId": j['kitStockId'],
                    "storageLocationCode": j['storageLocationCode'],
                }
                toolsList.append(goods1)

        return goodsList, toolsList

    # 上架商品
    def putOnshelf(self, goodsId=None, goodsLotInfoId=None, quantity=None, storageLocationCode=None,
                   putOnShelfId=None, goodsList=list(), toolsList=list()):
        url = '/putOnShelf/putOnShelf'
        body = {
            "goodsList": goodsList,
            "orderId": putOnShelfId,
            "toolsList": toolsList
        }
        goodsList = {
            "goodsId": goodsId,
            "goodsLotInfoId": goodsLotInfoId,
            "quantity": quantity,
            "storageLocationCode": storageLocationCode,
            "supplierId": None
        }
        if goodsId:
            body['goodsList'] = [goodsList]
        response = request.post_body01(url, body)


# 验收单
class CheckOrder:

    # 获取验收单id
    def get_checkOrder_list(self, inboundCode):
        url = '/checkOrder/list?pageNum=0&pageSize=50&keyword=%s' % inboundCode
        response = request.get01(url)
        if response['data']['rows'] != []:
            checkId = response['data']['rows'][0]['id']
            checkCode = response['data']['rows'][0]['code']
        else:
            checkId, checkCode = None, None
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
        registrationNum = str(goodsList['registrationNumList'])
        lotNum = goodsList['lotNum']
        # toolsList = response['data']['toolsList'][0]
        return checkId, goodsLotInfoId, goodsId, lotNum, inboundingQuantity, registrationNum

    # 获取多物资验收单详情
    def get_checkOrder_Infos(self, checkId):
        url = '/checkOrder/detail?orderId=%s' % checkId
        response = request.get01(url)
        inboundOrderDetailCheckBeanList = []
        for i in response['data']['goodsList']:
            unqualifiedQuantity = 0
            goods = {
                "checkInstructionUiList": [],
                "goodsLotInfoId": i['goodsLotInfoId'],
                "unqualifiedQuantity": 0,
                "goodsId": i['goodsId'],
                "lotNum": i['lotNum'],
                "quantity": i['inboundingQuantity'] - unqualifiedQuantity,
                "registrationNum": i['registrationNumList'][0],
                "serialNumber": None
            }

            inboundOrderDetailCheckBeanList.append(goods)
        return inboundOrderDetailCheckBeanList

    def check(self, checkId=None, goodsLotInfoId=None, unqualifiedQuantity=0, goodsId=None, lotNum=None,
              receivedQuantity=None,
              registrationNum=None, inboundOrderDetailCheckBeanList=list()):
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
            "inboundOrderDetailCheckBeanList": inboundOrderDetailCheckBeanList
        }

        if goodsId:
            inboundOrderDetailCheckBeanList = {
                "checkInstructionUiList": [],
                "goodsLotInfoId": goodsLotInfoId,
                "unqualifiedQuantity": unqualifiedQuantity,
                "goodsId": goodsId,
                "lotNum": lotNum,
                "quantity": receivedQuantity,
                "registrationNum": registrationNum,
                "serialNumber": None
            }
            body['inboundOrderDetailCheckBeanList'] = [inboundOrderDetailCheckBeanList]
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
        # 上架单
        self.test4 = PutOnShelf()

        self.pickOrderId = self.test.get_out_orderInfo(keyword)[0]
        self.outOrderId = self.test.get_out_orderInfo(keyword)[1]

        # ----------------------查询相关--------------------------
        # 拣货单 pda查询接口
        # self.test1.get_pda_detail(pickOrderId=self.pickOrderId)
        # # 拣货单 gs1解析
        # self.test1.get_gs1(pickOrderId=self.pickOrderId)
        # # 拣货单 code解析
        # self.test1.get_byCode(pickOrderId=self.pickOrderId)
        # # 拣货单 打印
        # self.test1.pickOrder_print(self.pickOrderId)
        #
        # # 出库单 查看发货详情
        # self.test.get_outOrder_deliveryInfo(self.outOrderId)
        # # 出库单 打印
        # self.test.outOrder_print(self.outOrderId)
        # # 出库单 详情
        # self.test.get_outOrder_detail(self.outOrderId)
        # # 出库单 地址详情
        # self.test.get_outOrder_adress(self.outOrderId)
        # # 查询接口
        # self.test.get_outOrder_list()
        # self.test1.get_pickOrder_list()
        # self.test2.get_inbound_list()
        #
        # self.test2.inbound_export()

        # ----------------------查询相关--------------------------

    # 拣货出库流程
    def all_pick_out(self):
        data = self.test1.get_pick_orderInfo(self.pickOrderId)
        self.materialCode = data[0]
        self.warehouseId = data[1]
        self.storageLocationId = data[2]
        self.quantity = data[3]

        goodsInfo = self.test1.get_goodsInfo(self.warehouseId, self.materialCode)
        self.goodsId = goodsInfo[0]
        self.lotNum = goodsInfo[1]
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
        data = self.test1.get_pick_orderInfo(self.pickOrderId)
        self.materialCode = data[0]
        self.warehouseId = data[1]
        self.storageLocationId = data[2]
        self.quantity = data[3]

        goodsInfo = self.test1.get_goodsInfo(self.warehouseId, self.materialCode)
        self.goodsId = goodsInfo[0]
        self.lotNum = goodsInfo[1]

        inboundOrderId = self.test2.get_inboundOrderId(self.keyword)[0]
        inboundCode = self.test2.get_inboundOrderId(self.keyword)[1]

        registrationNum = self.test2.get_InboundOrder_Info(inboundOrderId)[0]
        inboundingQuantity = self.test2.get_InboundOrder_Info(inboundOrderId)[1]

        # 入库单 收货
        self.test2.inbound_receiving(inboundOrderId=inboundOrderId, goodsId=self.goodsId, quantity=inboundingQuantity,
                                     lotNum=self.lotNum,
                                     registrationNum=registrationNum)

        data1 = self.test3.get_checkOrder_list(inboundCode)
        if data1[0]:
            checkId = data1[0]
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
        if inboundingQuantity > 0:
            # 上架单 上架
            putOnShelfId = self.test4.get_putOnShelfId(inboundCode)
            # return goodsId, goodsLotInfoId, storageLocationCode, quantity, putOnShelfId

            data = self.test4.get_putOnshelf_detail(putOnShelfId)
            goodsId = data[0]
            goodsLotInfoId = data[1]
            storageLocationCode = data[2]
            quantity = data[3]

            self.test4.putOnshelf(goodsId=goodsId, goodsLotInfoId=goodsLotInfoId, quantity=quantity,
                                  storageLocationCode=storageLocationCode, putOnShelfId=putOnShelfId)

        # # 验收单 验收
        # self.test3.check(checkId=checkId, goodsLotInfoId=goodsLotInfoId, goodsId=goodsId, lotNum=lotNum,
        #                  receivedQuantity=inboundingQuantity, registrationNum=str(registrationNum))

    def all_goods_pick(self):
        # 多物资拣货
        pickingUiBeans = self.test1.pick_goods(pickOrderId=self.pickOrderId)
        # 拣货单 拣货完成
        self.test1.pickFinished(pickOrderId=self.pickOrderId)

        # 拣货单 审核拣货
        self.test1.pick_approval(pickingUiBeans=pickingUiBeans, pickOrderId=self.pickOrderId)
        # 出库单 发货
        self.test.delivery(logisticsCompany='京东', deliveryDate=timeStamp, expressNo='123123',
                           outOrderId=self.outOrderId,
                           deliveryMode='DELIVERY')
        # 出库单 审核发货
        self.test.approval(logisticsCompany='京东', deliveryDate=timeStamp, expressNo='123123',
                           outOrderId=self.outOrderId)

    def all_tools_pick(self):
        # 工具包拣货
        pickingUiBeans = self.test1.pick_tools(pickOrderId=self.pickOrderId)
        # 拣货单 拣货完成
        self.test1.pickFinished(pickOrderId=self.pickOrderId)

        # 拣货单 审核拣货
        self.test1.pick_approval(pickingUiBeans=pickingUiBeans, pickOrderId=self.pickOrderId)
        # 出库单 发货
        self.test.delivery(logisticsCompany='京东', deliveryDate=timeStamp, expressNo='123123',
                           outOrderId=self.outOrderId,
                           deliveryMode='DELIVERY')
        # 出库单 审核发货
        self.test.approval(logisticsCompany='京东', deliveryDate=timeStamp, expressNo='123123',
                           outOrderId=self.outOrderId)

    def all_tools_goods_pick(self):
        # 拣工具包
        pickingUiBeans_tools = self.test1.pick_tools(pickOrderId=self.pickOrderId)
        # 拣物资
        pickingUiBeans_goods = self.test1.pick_goods(pickOrderId=self.pickOrderId)
        self.test1.pickFinished(pickOrderId=self.pickOrderId)
        pickingUiBeansList = []
        for x in pickingUiBeans_tools:
            pickingUiBeansList.append(x)
        for y in pickingUiBeans_goods:
            pickingUiBeansList.append(y)
        self.test1.pick_approval(pickingUiBeans=pickingUiBeansList, pickOrderId=self.pickOrderId)
        # 出库单 发货
        self.test.delivery(logisticsCompany='京东', deliveryDate=timeStamp, expressNo='123123',
                           outOrderId=self.outOrderId,
                           deliveryMode='DELIVERY')
        # 出库单 审核发货
        self.test.approval(logisticsCompany='京东', deliveryDate=timeStamp, expressNo='123123',
                           outOrderId=self.outOrderId)

    #     多物资入库
    def all_goods_inbound(self):
        # 入库
        inboundOrderId = self.test2.get_inboundOrderId(self.keyword)[0]
        inboundCode = self.test2.get_inboundOrderId(self.keyword)[1]
        inboundOrderDetailReceiveBeanList = self.test2.get_InboundOrder_Infos(inboundOrderId)
        self.test2.inbound_receiving(inboundOrderDetailReceiveBeanList=inboundOrderDetailReceiveBeanList,
                                     inboundOrderId=inboundOrderId)

        inboundingQuantity = self.test2.get_InboundOrder_Info(inboundOrderId)[1]

        if inboundingQuantity > 0:
            # 上架单 上架
            putOnShelfId = self.test4.get_putOnShelfId(inboundCode)

            dataList = self.test4.get_putOnshelf_details(putOnShelfId)
            goodsList = dataList[0]
            toolsList = dataList[1]

            self.test4.putOnshelf(putOnShelfId=putOnShelfId, toolsList=toolsList, goodsList=goodsList)
        # 验收
        data = self.test3.get_checkOrder_list(inboundCode)

        if data[0]:
            checkId = data[0]
            # 获取验收接口参数
            inboundOrderDetailCheckBeanList = self.test3.get_checkOrder_Infos(checkId)

            # 验收
            self.test3.check(inboundOrderDetailCheckBeanList=inboundOrderDetailCheckBeanList, checkId=checkId)


if __name__ == '__main__':
    test = InboundOrder()
    a = test.get_InboundOrder_Info(1319)
    print(a)
    # test = PutOnShelf()
    # test.get_putOnshelf_details(803)
    # test = All('AH_20210623_0033')
    # test.all_tools_pick()
