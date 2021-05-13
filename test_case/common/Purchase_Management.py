# -*- coding: utf-8 -*-
# @Time : 2021/5/12 4:08 下午 
# @Author : lsj
# @File : Purchase_Management.py
# 采购管理
import time, datetime

from common import request

timeStamp = int(time.time() * 1000)
today = datetime.date.today()
fiveDaysAfter = today + datetime.timedelta(days=5)
fiveDaysAfter_stamp = int(time.mktime(fiveDaysAfter.timetuple())) * 1000


# 采购管理：调拨单
class AllocateOrder:

    # 获取出库仓ID
    def get_out_warehouse(self):
        url = '/warehouse/getUserRelationWarehouse'
        response = request.get(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response
        # 目前有库存的是丽都仓
        for i in response['data']:
            if i['warehouseName'] == '丽都仓':
                sourceWarehouseId = i['id']
                return sourceWarehouseId

    # 获取入库仓ID
    def get_in_warehouse(self):
        url = '/warehouse/getUserRelationWarehouse'
        response = request.get(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response
        # 目前有库存的是丽都仓
        for i in response['data']:
            if i['warehouseName'] == '天空一号仓':
                targetWarehouseId = i['id']
                return targetWarehouseId

    # 获取调拨理由
    def get_allocate_reason(self):
        url = '/dictionary/getByType/allocate_reason'
        response = request.get(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response
        # 索引最后一个是 其他
        reasonCode = response['data'][0]['code']
        return reasonCode

    # 获取调出仓的物资信息
    def get_goodsInfo(self, sourceWarehouseId):
        url = '/goodsStock/findAllocateGoodsStockList'
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'warehouseId': sourceWarehouseId
        }
        response = request.get_params(url, params)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response
        goodsId = response['data']['rows'][0]['goodsId']
        goodsLotInfoId = response['data']['rows'][0]['goodsLotInfoId']
        return goodsId, goodsLotInfoId

    # 获取调出仓的工具包信息
    def get_kitStockId(self, sourceWarehouseId):
        url = '/kitStock/findKitStockListByAllocate'
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'warehouseId': sourceWarehouseId
        }
        response = request.get_params(url, params)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response
        kitStockId = response['data']['rows'][0]['id']
        return kitStockId

    def push_body(self, reasonCode=None, sourceWarehouseId=None, targetWarehouseId=None,
                  goodsId=None, goodsLotInfoId=None, goodsQuantity=1, kitStockId=None, kitStockQuantity=1):
        body = {
            "baseOrderInfo": {
                "reasonCode": reasonCode,
                "reason": "",
                "sourceWarehouseId": sourceWarehouseId,
                "targetWarehouseId": targetWarehouseId
            },
            "goodsDetailUiBeans": [{
                "goodsId": goodsId,
                "goodsLotInfoId": goodsLotInfoId,
                "goodsQuantity": goodsQuantity
            }],
            "toolsDetailUiBeans": [],
            "toolKitDetailUiBeans": [{
                "kitStockId": kitStockId,
                "kitStockQuantity": kitStockQuantity
            }]
        }
        return body

    # 创建调拨单
    def create(self, body):
        url = '/allocateOrder/create'
        body = body
        response = request.post_body(url, body)
        Id = response['data']['id']
        code = response['data']['code']
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response
        return Id, code

    # body,调拨单ID ,code

    def all(self):
        # 调出仓、调入仓、调拨理由
        reasonCode = self.get_allocate_reason()
        sourceWarehouseId = self.get_out_warehouse()
        targetWarehouseId = self.get_in_warehouse()

        # 物资信息
        goodsInfo = self.get_goodsInfo(sourceWarehouseId)
        goodsId = goodsInfo[0]
        goodsLotInfoId = goodsInfo[1]

        # 工具包信息
        kitStockId = self.get_kitStockId(sourceWarehouseId)

        # 传body下来
        body = self.push_body(reasonCode, sourceWarehouseId, targetWarehouseId, goodsId, goodsLotInfoId,
                              kitStockId)

        # 创建调拨单
        body, Id, code = self.create(body)


if __name__ == '__main__':
    test = AllocateOrder()
    test.all()
