# -*- coding: utf-8 -*-
# @Time : 2021/5/12 4:08 下午
# @Author : lsj
# @File : Purchase_Management.py
# 采购管理
import time, datetime
import request, Warehouse_Management

timeStamp = int(time.time() * 1000)
today = datetime.date.today()
fiveDaysAfter = today + datetime.timedelta(days=5)
fiveDaysAfter_stamp = int(time.mktime(fiveDaysAfter.timetuple())) * 1000


# 采购管理：调拨单
class AllocateOrder:
    # 获取出库仓ID
    def get_out_warehouse(self):
        url = '/warehouse/getUserRelationWarehouse'
        response = request.get01(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response
        # 目前有库存的是丽都仓
        for i in response['data']:
            if i['warehouseName'] == '骨科-丽都临调仓':
                sourceWarehouseId = i['id']
                return sourceWarehouseId

    # 获取入库仓ID
    def get_in_warehouse(self):
        url = '/warehouse/getUserRelationWarehouse'
        response = request.get01(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response
        for i in response['data']:
            if i['warehouseName'] == '骨科-北京临调仓':
                targetWarehouseId = i['id']
                return targetWarehouseId

    # 获取调拨理由
    def get_allocate_reason(self):
        url = '/dictionary/getByType/allocate_reason'
        response = request.get01(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response
        # 索引最后一个是 其他
        reasonCode = response['data'][0]['code']
        return reasonCode

    # 获取调出仓的物资信息
    def get_goodsInfo(self, sourceWarehouseId):
        url = '/stockBaseData/findAllocateGoodsStockList'
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'warehouseId': sourceWarehouseId
        }
        response = request.get_params01(url, params)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response
        goodsId = response['data']['rows'][1]['goodsId']
        goodsLotInfoId = response['data']['rows'][1]['goodsLotInfoId']
        return goodsId, goodsLotInfoId

    # 获取goodInfoId
    def get_all_goodInfoId(self, keyword, warehouseId):
        url = '/stockBaseData/findAllocateGoodsStockList?warehouseId=%s&pageNum=0&pageSize=50&keyword=%s' % (
            warehouseId, keyword)
        response = request.get01(url)
        goodInfoId = response['data']['rows'][0]['goodsLotInfoId']
        goodsId = response['data']['rows'][0]['goodsId']
        return goodsId, goodInfoId

    # 获取调出仓的工具包信息
    def get_kitStockId(self, sourceWarehouseId):
        url = '/stockBaseData/findKitStockListByAllocate'
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'warehouseId': sourceWarehouseId
        }
        response = request.get_params01(url, params)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response
        kitStockId = response['data']['rows'][0]['id']
        return kitStockId

    # 调拨单创建、编辑（编辑要传 ID）
    def create(self, reasonCode=None, sourceWarehouseId=None, targetWarehouseId=None,
               goodsId=None, goodsLotInfoId=None, goodsQuantity=1, kitStockId=None, kitStockQuantity=1, Id=None,
               goodsDetailUiBeans=list()):
        url = '/allocateOrder/create'
        body = {
            "baseOrderInfo": {
                "id": Id,
                "reasonCode": reasonCode,
                "reason": "",
                "sourceWarehouseId": sourceWarehouseId,
                "targetWarehouseId": targetWarehouseId
            },
            "goodsDetailUiBeans": goodsDetailUiBeans,
            "toolsDetailUiBeans": [],
            "toolKitDetailUiBeans": []
        }
        toolKitDetailUiBeans = {
            "kitStockId": kitStockId,
            "kitStockQuantity": kitStockQuantity
        }
        if goodsId:
            goodsDetailUiBeans = {
                "goodsId": goodsId,
                "goodsLotInfoId": goodsLotInfoId,
                "goodsQuantity": goodsQuantity
            }
            body['goodsDetailUiBeans'] = [goodsDetailUiBeans]
        if kitStockId:
            body['toolKitDetailUiBeans'] = [toolKitDetailUiBeans]
        #     只有供应商可创建调拨
        response = request.post_body01(url, body)
        allocateId = response['data']['id']
        code = response['data']['code']
        return allocateId, code

    def create_more(self, goodsList=None, quantityList=None, goodsLotInfoIdList=None, sourceWarehouseId=None,
                    targetWarehouseId=None, reasonCode=None):
        goodsDetailUiBeans = []
        for x, y, z in zip(goodsList, quantityList, goodsLotInfoIdList):
            goods = {
                "goodsId": x,
                "goodsLotInfoId": z,
                "goodsQuantity": y
            }
            goodsDetailUiBeans.append(goods)
        data = self.create(goodsDetailUiBeans=goodsDetailUiBeans, sourceWarehouseId=sourceWarehouseId,
                           targetWarehouseId=targetWarehouseId, reasonCode=reasonCode)
        return data

    # body,调拨单ID ,code

    # 审核调拨单：驳回、通过
    def approve(self, approve=False, allocateId=None, rejectReason='不通过'):
        """

        :param approve: False 驳回  、True  通过
        :param Id: 调拨单ID
        :param rejectReason: 驳回理由
        :return:
        """
        url = '/allocateOrder/approve'
        body = {
            "approve": approve,
            "id": allocateId,
            "rejectReason": rejectReason
        }
        response = request.put_body01(url, body)
        return response

    # 关闭订单
    def close(self, allocateId):
        url = '/allocateOrder/close?orderId=%s' % allocateId

        response = request.put01(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response

    # 删除订单
    def remove(self, allocateId):
        url = '/allocateOrder/remove?orderId=%s' % allocateId

        response = request.delete01(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response

    # 查询 调拨单详情
    def get_allocate_detail(self, allocateId):
        url = '/allocateOrder/detail?orderId=%s' % allocateId
        response = request.get01(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response

    # 查询 调拨单列表
    def get_allocate_list(self):
        url = '/allocateOrder/findList?pageNum=0&pageSize=50'
        response = request.get01(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response

    # 主流程：创建调拨单
    def all(self):

        # 调出仓、调入仓、调拨理由
        reasonCode = self.get_allocate_reason()

        # sourceWarehouseId = self.get_out_warehouse()
        # targetWarehouseId = self.get_in_warehouse()
        sourceWarehouseId = 1
        targetWarehouseId = 89

        # 物资信息
        goodsInfo = self.get_goodsInfo(sourceWarehouseId)
        # goodsId = goodsInfo[0]
        # 6/3 号，后续商品ID需要动态获取，目前这个是 在数据库准备的数据
        goodsId = 20538
        # goodsLotInfoId = goodsInfo[1]
        goodsLotInfoId = 1
        kitStockId = None
        # 工具包信息
        # kitStockId = self.get_kitStockId(sourceWarehouseId)

        #  创建调拨单 --有工具包
        # Id, code = self.create(reasonCode, sourceWarehouseId, targetWarehouseId, goodsId, goodsLotInfoId,
        #                        kitStockId)
        # 创建调拨单
        allocateId, allocateCode = self.create(reasonCode=reasonCode, sourceWarehouseId=sourceWarehouseId,
                                               targetWarehouseId=targetWarehouseId, goodsId=goodsId,
                                               goodsLotInfoId=goodsLotInfoId, kitStockId=kitStockId)
        # 查询调拨单详情
        self.get_allocate_detail(allocateId=allocateId)
        # 查询调拨单列表
        self.get_allocate_list()
        # 驳回调拨单---修改
        self.approve(allocateId=allocateId)
        # 修改调拨单
        self.create(reasonCode, sourceWarehouseId, targetWarehouseId, goodsId,
                    goodsLotInfoId, Id=allocateId)
        # 驳回调拨单 -- 关闭
        self.approve(allocateId=allocateId)
        # 关闭调拨单
        self.close(allocateId=allocateId)

        # 创建调拨单
        allocateId, allocateCode = self.create(reasonCode=reasonCode, sourceWarehouseId=sourceWarehouseId,
                                               targetWarehouseId=targetWarehouseId, goodsId=goodsId,
                                               goodsLotInfoId=goodsLotInfoId, kitStockId=kitStockId)

        # 接收调拨单
        self.approve(allocateId=allocateId, approve=True, rejectReason='')
        return allocateCode

    def all_moreGoods(self):
        sourceWarehouseId = 1
        targetWarehouseId = 89

        reasonCode = self.get_allocate_reason()
        goods = ['ID_20538', 'ID_22344']
        quantityList = [1, 2]
        goodsIdList = []
        goodInfoIdList = []
        for i in goods:
            data = self.get_all_goodInfoId(i, 1)
            goodsId = data[0]
            goodInfoId = data[1]
            goodsIdList.append(goodsId)
            goodInfoIdList.append(goodInfoId)
        data = self.create_more(goodsList=goodsIdList, quantityList=quantityList, goodsLotInfoIdList=goodInfoIdList,
                                sourceWarehouseId=sourceWarehouseId,
                                targetWarehouseId=targetWarehouseId, reasonCode=reasonCode)
        self.approve(allocateId=data[0], approve=True, rejectReason='')
        # 拣货
        Warehouse_Management.All(data[1]).all_goods_pick()


if __name__ == '__main__':
    sourceWarehouseId = 1
    targetWarehouseId = 89
    test = AllocateOrder()
    # a = test.all()
    # print(a)
    test.all_moreGoods()
    # test.approve(True)
    # test.close(115)
    # # test.remove(112)
    # reasonCode = test.get_allocate_reason()
    # goods = ['ID_20538', 'ID_22344']
    # quantityList = [1, 2]
    # goodsIdList = []
    # goodInfoIdList = []
    # for i in goods:
    #     data = test.get_all_goodInfoId(i, 1)
    #     goodsId = data[0]
    #     goodInfoId = data[1]
    #     goodsIdList.append(goodsId)
    #     goodInfoIdList.append(goodInfoId)
    # test.create_more(goodsList=goodsIdList, quantityList=quantityList, goodsLotInfoIdList=goodInfoIdList,
    #                  sourceWarehouseId=sourceWarehouseId,
    #                  targetWarehouseId=targetWarehouseId, reasonCode=reasonCode)
