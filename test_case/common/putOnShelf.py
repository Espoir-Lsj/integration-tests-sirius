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
    #
    # i = 0
    # while i < len(goodsId):
    #     dict = {
    #         "goodsId": goodsId[i],
    #         "goodsLotInfoId": goodsLotInfoId[i],
    #         "quantity": quantity[i],
    #         "storageLocationCode": storageLocationCode[i]
    #     }
    #     goodsList.append(dict)
    #     i += 1
    # j = 0
    # # log.info('sbbbbbs %s' % kitStockId)
    # if kitStockId :
    #     while j < len(kitStockId):
    #         dict1 = {
    #             "kitStockId": kitStockId[j],
    #             "storageLocationCode": TstorageLocationCode[j]
    #         }
    #         toolsList.append(dict1)
    #         j += 1
    #     # 上架
    #     body = {
    #         "orderId": putId,
    #         "goodsList": goodsList,
    #         "toolsList": toolsList
    #     }
    # else:
    #     body = {
    #         "orderId": putId,
    #         "goodsList": goodsList,
    #     }

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
            else:
                body = {
                    "orderId": putId,
                    "goodsList": goodsList
                }
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
    else:
        body = {
            "orderId": putId
        }

    log.info('传入的参数 %s' % body)
    put = request.post_body('/putOnShelf/putOnShelf', body)
    log.info('响应结果 %s' % put)

    return put
