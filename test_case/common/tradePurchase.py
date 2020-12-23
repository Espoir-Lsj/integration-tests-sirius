# __author:"zonglr"
# date:2020/12/11
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import datetime, time, jsonpath, random
from common import supplier_request, logger, supplier_request_02
from faker import Faker
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


# 新增求购信息
def addPurchase(skuCode=None, goodsName='test', manufacturerName='test', specification='test', model=None, price=1,
                quantity=1, category=categoryId, closingDate=tomorrow_stamp, contact=faker.name(),
                contactPhone=faker.phone_number(), receiverArea=110101000000, supplierName=supplier_name,
                remark=None):
    body = {
        'skuCode': skuCode,  # 原厂编号
        'goodsName': goodsName,
        'manufacturerName': manufacturerName,
        'specification': specification,
        'model': model,
        'price': price,
        'quantity': quantity,
        'category': category,  # 商品类型
        'closingDate': closingDate,  # 关闭日期
        'contact': contact,  # 联系人
        'contactPhone': contactPhone,  # 联系方式
        'receiverArea': receiverArea,  # 收货地址
        'supplierName': supplierName,  # 供应商名称
        'remark': remark
    }
    response = supplier_request.post_body('/purchase/add', body=body)
    return response


# 新增供应商B的求购信息
def addPurchase_02(skuCode=None, goodsName='test', manufacturerName='test', specification='test', model=None, price=1,
                   quantity=1, category=categoryId, closingDate=tomorrow_stamp, contact=faker.name(),
                   contactPhone=faker.phone_number(), receiverArea=110101000000, supplierName=supplier_name_02,
                   remark=None):
    body = {
        'skuCode': skuCode,  # 原厂编号
        'goodsName': goodsName,
        'manufacturerName': manufacturerName,
        'specification': specification,
        'model': model,
        'price': price,
        'quantity': quantity,
        'category': category,  # 商品类型
        'closingDate': closingDate,  # 关闭日期
        'contact': contact,  # 联系人
        'contactPhone': contactPhone,  # 联系方式
        'receiverArea': receiverArea,  # 收货地址
        'supplierName': supplierName,  # 供应商名称
        'remark': remark
    }
    response = supplier_request_02.post_body('/purchase/add', body=body)
    return response


# 取消求购信息
def cancelPurchase(**kwargs):
    """
    id:
    """
    response = supplier_request.put_body('/purchase/cancel', body=kwargs)
    return response


# 删除求购信息
def deletePurchase(**kwargs):
    """
    id
    """
    response = supplier_request.delete_body('/purchase/delete', body=kwargs)
    return response


# 求购信息详情
def detail(id):
    response = supplier_request.get('/purchase/detail?id=%s' % id)
    return response


# 编辑求购信息
def editPurchase(id, skuCode=None, goodsName='test', manufacturerName='test', specification='test', model=None, price=1,
                 quantity=1, category=categoryId, closingDate=tomorrow_stamp, contact=faker.name(),
                 contactPhone=faker.phone_number(), receiverArea=110101000000, supplierName=supplier_name,
                 remark=None):
    body = {
        'id': id,
        'skuCode': skuCode,  # 原厂编号
        'goodsName': goodsName,
        'manufacturerName': manufacturerName,
        'specification': specification,
        'model': model,
        'price': price,
        'quantity': quantity,
        'category': category,  # 商品类型
        'closingDate': closingDate,  # 关闭日期
        'contact': contact,  # 联系人
        'contactPhone': contactPhone,  # 联系方式
        'receiverArea': receiverArea,  # 收货地址
        'supplierName': supplierName,  # 供应商名称
        'remark': remark
    }
    response = supplier_request.put_body('/purchase/edit', body=body)
    return response


# 查询求购列表
def listPurchase(categoryId=None, keyword=None, pageNum=0, pageSize=20, sortName=None):
    params = {
        'categoryId': categoryId,
        'keyword': keyword,
        'pageNum': pageNum,
        'pageSize': pageSize,
        # 'sortList[0].desc': True,
        # 'sortList[0].nullsLast': True,
        # 'sortList[0].sortName': sortName
    }
    response = supplier_request.get_params('/purchase/list', params=params)
    return response


# 查询我的求购信息
def myPurchaseList(categoryId=None, keyword=None, pageNum=0, pageSize=20, sortName=None):
    params = {
        'categoryId': categoryId,
        'keyword': keyword,
        'pageNum': pageNum,
        'pageSize': pageSize,
        # 'sortList[0].desc': True,
        # 'sortList[0].nullsLast': True,
        # 'sortList[0].sortName': sortName
    }
    response = supplier_request.get_params('/purchase/myPurchaseList', params=params)
    return response
