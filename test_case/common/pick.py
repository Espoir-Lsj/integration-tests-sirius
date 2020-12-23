# __author:"zonglr"
# date:2020/12/9
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import time, datetime, re
from common import logger, request
from faker import Faker

log = logger.Log()
faker = Faker(locale='zh_CN')


# 拣单个商品-仅一次
def pickOne(goodsId, lotNum, serialNumber, storageLocationId, pickOrderId):
    body = {
        'goodsId': goodsId,
        'lotNum': lotNum,
        'pickOrderId': pickOrderId,
        'serialNumber': serialNumber,
        'storageLocationId': storageLocationId
    }
    pick_response = request.put_body('/pickOrder/picking', body=body)
    return pick_response


def finishPick(pickOrderId):
    # 根据拣货单id查询详情
    detail = request.get('/pickOrder/detail/%s' % pickOrderId)
    assert detail['msg'] == '请求成功'
    goodsDetail = detail['data']['goodsDetail']
    kitDetail = detail['data']['kitDetail']
    toolsKitDetail = detail['data']['toolsKitDetail']

    # 物资列表
    for goods in goodsDetail:
        # 物资udi
        udi = goods['udi']
        new_udi = re.sub(r'\D', "", udi)
        # 物资编号
        materialCode = goods['materialCode']
        # 货位号
        storageLocationId = goods['storageLocationId']
        # 物资待拣数量
        unpickedQuantity = int(goods['quantity']) - int(goods['pickedQuantity'])

        # 扫码获取批号信息
        gs1Decode = request.get('/goods/gs1Decode?code=%s' % new_udi)
        # 序列号
        serialNumber = gs1Decode['data']['serialNumber']
        # 物资id
        goodsId = gs1Decode['data']['goodsId']
        # 批号
        lotNum = gs1Decode['data']['lotNum']
        body = {
            'goodsId': goodsId,
            'lotNum': lotNum,
            'pickOrderId': pickOrderId,
            'serialNumber': serialNumber,
            'storageLocationId': storageLocationId
        }
        # 商品待拣货数量大于1时需多次拣货
        num = 0
        while num < unpickedQuantity:
            pick_response = request.put_body('/pickOrder/picking', body=body)
            assert pick_response['msg'] == '请求成功'
            num += 1
        log.info('物资%s拣货完成' % materialCode)

    # 套包列表 TODO
    for kit in kitDetail:
        print(kit)

    # 工具包列表
    for tools in toolsKitDetail:
        # 工具包条码
        operatorBarcode = tools['operatorBarcode']
        # kitStockId
        kitStockId = tools['kitStockId']
        # 货位号
        storageLocationId = tools['storageLocationId']
        # 物资待拣数量
        unpickedQuantity = int(tools['quantity']) - int(tools['pickedQuantity'])

        body = {
            'kitStockId': kitStockId,
            'pickOrderId': pickOrderId,
            'storageLocationId': storageLocationId
        }
        num = 0
        while num < unpickedQuantity:
            pick_response = request.put_body('/pickOrder/picking', body=body)
            assert pick_response['msg'] == '请求成功'
            num += 1
        log.info('工具包%s拣货完成' % operatorBarcode)

    # 完成拣货
    body2 = {
        'pickOrderId': pickOrderId,
        'imagePath': ['/file/2020/11/16/ac110bd6-ff1f-41ed-b645-a570a8c34df9/提货委托书.jpg']
    }
    finishPick = request.put_body('/pickOrder/pickFinished', body=body2)
    log.info('拣货单完成 %s' % finishPick)
    return finishPick
