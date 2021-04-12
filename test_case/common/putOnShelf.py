# __author:"lsj"
# date:2021/4/7
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import jsonpath

from common import request, logger

log = logger.Log()


def put_all(allocateInboundOrderCode):
    put_Detail = request.get('/putOnShelf/findList?pageNum=0&pageSize=50&keyword=%s' % allocateInboundOrderCode)
    assert put_Detail['msg'] == '请求成功'
    # 获取上架单号
    putId = put_Detail['data']['rows'][0]['id']

    putCode = put_Detail['data']['rows'][0]['code']
    # 上架单详情
    log.info('上架单ID %s' % putId)
    # 获取上架物资信息
    putList = request.get('/putOnShelf/getDetail?orderId=%s' % putId)

    goodsId = jsonpath.jsonpath(putList, '$..goodsList[*].goodsId')
    goodsLotInfoId = jsonpath.jsonpath(putList, '$..goodsList[*].goodsLotInfoId')
    quantity = jsonpath.jsonpath(putList, '$..goodsList[*].quantity')
    storageLocationCode = jsonpath.jsonpath(putList, '$..goodsList[*].storageLocationCode')
    supplierId = jsonpath.jsonpath(putList, '$..goodsList[*].supplierId')
    kitStockId = jsonpath.jsonpath(putList, '$..toolsList[*].kitStockId')
    TstorageLocationCode = jsonpath.jsonpath(putList, '$..toolsList[*].storageLocationCode')
    # toolsList = jsonpath.jsonpath(putList,'$..toolsList')
    goodsList = []
    toolsList = []
    # 临调单 上架商品 只有物资 or 物资加工具包
    # log.info('abddd:%s' % kitStockId)
    # print('fffffffff:%s' % kitStockId)

    # toolsList = putList['data']['toolsList'] = map(lambda x: {
    #     "kitStockId": x["kitStockId"],
    #     "storageLocationCode": x["storageLocationCode"],
    # }, putList["data"]["toolsList"])
    #
    # goodsList =putList["data"]["goodsList"] = map(lambda x: {
    #     "goodsId": x["goodsId"],
    #     "goodsLotInfoId": x["goodsLotInfoId"],
    #     "quantity": x["quantity"],
    #     "storageLocationCode": x["storageLocationCode"],
    # }, putList["data"]["goodsList"])


    if goodsId:
        i = 0
        while i < len(goodsId):
            dict = {
                "goodsId": goodsId[i],
                "goodsLotInfoId": goodsLotInfoId[i],
                "quantity": quantity[i],
                "storageLocationCode": storageLocationCode[i]
            }
            goodsList.append(dict)
            i += 1
            if kitStockId:
                j = 0
                while j < len(kitStockId):
                    dict1 = {
                        "kitStockId": kitStockId[j],
                        "storageLocationCode": TstorageLocationCode[j]
                    }
                    toolsList.append(dict1)
                    j += 1
                body = {
                    "orderId": putId,
                    "goodsList": goodsList,
                    "toolsList": toolsList
                }
                log.info("上架物资加工具包")
            else:
                body = {
                    "orderId": putId,
                    "goodsList": goodsList
                }
                log.info("只上架商品")
    # 临调单上架商品只有 工具包
    elif kitStockId:
        j = 0
        while j < len(kitStockId):
            dict1 = {
                "kitStockId": kitStockId[j],
                "storageLocationCode": TstorageLocationCode[j]
            }
            toolsList.append(dict1)
            j += 1
        body = {
            "orderId": putId,
            "toolsList": toolsList
        }
        log.info("只上架工具包")
    # 临调单 没有物资上架
    else:
        body = {
            "orderId": putId
        }
        log.info("没有物资上架")

    log.info('传入的参数 %s' % body)
    put = request.post_body('/putOnShelf/putOnShelf', body)
    log.info('响应结果 %s' % put)

    return put
