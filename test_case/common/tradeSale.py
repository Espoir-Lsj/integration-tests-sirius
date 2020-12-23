# __author:"zonglr"
# date:2020/12/16
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import datetime, time, jsonpath, random
from common import logger
from faker import Faker
from common import supplier_request, supplier_request_02
from test_config import param_config

log = logger.Log()
faker = Faker(locale='zh_CN')

# 获取供应商名称
supplier_name = param_config.supplierName
supplier_name_02 = param_config.supplierName02
# 获取今天、明天、后天、昨天的时间戳
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
twoDaysAfter = today + datetime.timedelta(days=2)
yesterday = today - datetime.timedelta(days=1)
today_stamp = int(time.mktime(today.timetuple())) * 1000
tomorrow_stamp = int(time.mktime(tomorrow.timetuple())) * 1000
twoDaysAfter_stamp = int(time.mktime(twoDaysAfter.timetuple())) * 1000
yesterday_stamp = int(time.mktime(yesterday.timetuple())) * 1000
# 获取商品分类列表
list = supplier_request.get('/category/getTree?parentCode=MATERIAL')
# 获取所有的分类id，包括一级二级分类
ids = jsonpath.jsonpath(list, '$..id')
# 随机取一个分类id
categoryId = ids[random.randint(0, len(ids))]


# 供应商A新增售卖信息
def addSale(skuCode=None, goodsName='test', manufacturerName='test', specification='test', model=None, price=1,
            expirationDate=tomorrow_stamp, imageResource='123', newAndOldStandard='brand_new',
            abrasionStandard='not_used', packingIntactStandard='package_is_complete', quantity=1, category=categoryId,
            contact=faker.name(), contactPhone=faker.phone_number(), deliveryArea=110101000000,
            supplierName=supplier_name, remark=None):
    body = {
        'skuCode': skuCode,  # 原厂编号
        'goodsName': goodsName,
        'manufacturerName': manufacturerName,
        'specification': specification,
        'model': model,
        'price': price,
        'expirationDate': expirationDate,  # 失效日期
        'imageResource': [imageResource],  # 物资照片 array
        # 新旧程度 brand_new, eighty_percent, fifty_percent, less_than_fifty_percent, sixty_percent
        'newAndOldStandard': newAndOldStandard,
        'abrasionStandard': abrasionStandard,  # 是否有磨损 abrasion, not_used, used_new
        'packingIntactStandard': packingIntactStandard,  # 包装是否完整 incomplete_packing, no_packaging, package_is_complete
        'quantity': quantity,
        'category': category,  # 商品类型
        'contact': contact,  # 联系人
        'contactPhone': contactPhone,  # 联系方式
        'deliveryArea': deliveryArea,  # 发货地址
        'supplierName': supplierName,  # 供应商名称
        'remark': remark
    }
    response = supplier_request.post_body('/sale/add', body=body)
    return response


# 供应商B新增售卖信息
def addSale_02(skuCode=None, goodsName='test', manufacturerName='test', specification='test', model=None, price=1,
               expirationDate=tomorrow_stamp, imageResource='123', newAndOldStandard='brand_new',
               abrasionStandard='not_used', packingIntactStandard='package_is_complete', quantity=1,
               category=categoryId,
               contact=faker.name(), contactPhone=faker.phone_number(), deliveryArea=110101000000,
               supplierName=supplier_name_02, remark=None):
    body = {
        'skuCode': skuCode,  # 原厂编号
        'goodsName': goodsName,
        'manufacturerName': manufacturerName,
        'specification': specification,
        'model': model,
        'price': price,
        'expirationDate': expirationDate,  # 失效日期
        'imageResource': [imageResource],  # 物资照片 array
        # 新旧程度 brand_new, eighty_percent, fifty_percent, less_than_fifty_percent, sixty_percent
        'newAndOldStandard': newAndOldStandard,
        'abrasionStandard': abrasionStandard,  # 是否有磨损 abrasion, not_used, used_new
        'packingIntactStandard': packingIntactStandard,  # 包装是否完整 incomplete_packing, no_packaging, package_is_complete
        'quantity': quantity,
        'category': category,  # 商品类型
        'contact': contact,  # 联系人
        'contactPhone': contactPhone,  # 联系方式
        'deliveryArea': deliveryArea,  # 发货地址
        'supplierName': supplierName,  # 供应商名称
        'remark': remark
    }
    response = supplier_request_02.post_body('/sale/add', body=body)
    return response


# 删除售卖信息
def deleteSale(**kwargs):
    response = supplier_request.delete_body('/sale/delete', body=kwargs)
    return response


# 查询售卖详情
def saleDetail(id):
    response = supplier_request.get('/sale/detail?id=%s' % id)
    return response


# 编辑售卖信息
def editSale(id, skuCode=None, goodsName='test', manufacturerName='test', specification='test', model=None, price=1,
             expirationDate=tomorrow_stamp, imageResource='123', newAndOldStandard='brand_new',
             abrasionStandard='not_used', packingIntactStandard='package_is_complete', quantity=1, category=categoryId,
             contact=faker.name(), contactPhone=faker.phone_number(), deliveryArea=110101000000,
             supplierName=supplier_name, remark=None):
    body = {
        'id': id,
        'skuCode': skuCode,  # 原厂编号
        'goodsName': goodsName,
        'manufacturerName': manufacturerName,
        'specification': specification,
        'model': model,
        'price': price,
        'expirationDate': expirationDate,  # 失效日期
        'imageResource': [imageResource],  # 物资照片 array
        # 新旧程度 brand_new, eighty_percent, fifty_percent, less_than_fifty_percent, sixty_percent
        'newAndOldStandard': newAndOldStandard,
        'abrasionStandard': abrasionStandard,  # 是否有磨损 abrasion, not_used, used_new
        'packingIntactStandard': packingIntactStandard,  # 包装是否完整 incomplete_packing, no_packaging, package_is_complete
        'quantity': quantity,
        'category': category,  # 商品类型
        'contact': contact,  # 联系人
        'contactPhone': contactPhone,  # 联系方式
        'deliveryArea': deliveryArea,  # 发货地址
        'supplierName': supplierName,  # 供应商名称
        'remark': remark
    }
    response = supplier_request.put_body('/sale/edit', body=body)
    return response


# 查询售卖列表
def listSale(categoryId=None, keyword=None, pageNum=0, pageSize=20, sortName=None):
    params = {
        'categoryId': categoryId,
        'keyword': keyword,
        'pageNum': pageNum,
        'pageSize': pageSize,
        # 'sortList[0].desc': True,
        # 'sortList[0].nullsLast': True,
        # 'sortList[0].sortName': sortName
    }
    response = supplier_request.get_params('/sale/list', params=params)
    return response


# 查询我的售卖信息
def mySaleList(categoryId=None, keyword=None, pageNum=0, pageSize=20, sortName=None):
    params = {
        'categoryId': categoryId,
        'keyword': keyword,
        'pageNum': pageNum,
        'pageSize': pageSize,
        # 'sortList[0].desc': True,
        # 'sortList[0].nullsLast': True,
        # 'sortList[0].sortName': sortName
    }
    response = supplier_request.get_params('/sale/mySaleList', params=params)
    return response


# 已经售卖
def sold(**kwargs):
    response = supplier_request.put_body('/sale/sold', body=kwargs)
    return response
