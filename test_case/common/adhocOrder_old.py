# __author:"zonglr"
# date:2020/11/9
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import time, datetime
from common import logger, request
from faker import Faker

log = logger.Log()
faker = Faker(locale='zh_CN')

# 获取今天、明天、后天、昨天的时间戳
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
twoDaysAfter = today + datetime.timedelta(days=2)
yesterday = today - datetime.timedelta(days=1)
today_stamp = int(time.mktime(today.timetuple())) * 1000
tomorrow_stamp = int(time.mktime(tomorrow.timetuple())) * 1000
twoDaysAfter_stamp = int(time.mktime(twoDaysAfter.timetuple())) * 1000
yesterday_stamp = int(time.mktime(yesterday.timetuple())) * 1000

# 获取供应商列表
# list = request.get('/supplier/dropDownSupplierList')
# 获取供应商id
# supplierId = list['data'][0]['id']
supplierId = 1
# 获取手术部位
site = request.get('/dictionary/getByType/procedure_site')
siteId = site['data'][0]['id']
# 获取品牌
brands = request.get('/manufacturer/allBrands')
brandId = brands['data'][0]['id']


# 小程序创建临调单
def appCreateAdhocOrder(goodsId, goodsQuantity=1, kitTemplateId=None, ageGroup='adult', gender='male',
                        goodsSupplierId=supplierId, supplierId=supplierId, hospitalName='测试', siteId=siteId,
                        surgeon=faker.name(), procedureTime=tomorrow_stamp, expectReturnTime=twoDaysAfter_stamp,
                        postcode=faker.postcode(), contactName='测试', contactPhone=faker.phone_number(),
                        manufacturerId=brandId, salesPerson=faker.name(), deliveryMode='DELIVERY',
                        receivingName=faker.name(), receivingIdCard=None, receivingPhone=faker.phone_number(),
                        districtCode=110101000000, receivingAddress=faker.address(), powerOfAttorney=None,
                        consignorName=None, consignorPhone=None):
    # # 查询商品主耗材列表
    # goods = request.get('/goods/findListByMainMaterial?pageNum=0&pageSize=50&manufacturerId=%d' % brandId)
    # goodsId = goods['data']['rows'][0]['id']
    # stockQuantity = goods['data']['rows'][0]['stockQuantity']

    # 创建临调单的参数
    body = {
        'toolsDetailUiBeans': [],
        'goodsDetailUiBeans': [],
        'orderUiBean': {
            'ageGroup': ageGroup,  # 年龄段
            'gender': gender,  # 性别
            'supplierId': supplierId,
            'hospitalName': hospitalName,
            'procedureSite': [siteId],
            'surgeon': surgeon,
            'procedureTime': procedureTime,
            'expectReturnTime': expectReturnTime,
            'postcode': postcode,
            'contactName': contactName,
            'contactPhone': contactPhone,
            'manufacturerId': manufacturerId,
            'salesPerson': salesPerson,  # 销售人员
            'deliveryMode': deliveryMode,  # 快递DELIVERY  自提SELF_PIKE_UP
            'receivingName': receivingName,  # 收件人
            'receivingIdCard': receivingIdCard,  # 提货人身份证号
            'receivingPhone': receivingPhone,  # 提货人电话
            'districtCode': districtCode,  # 收件区域
            'receivingAddress': receivingAddress,  # 收件地址
            'powerOfAttorney': powerOfAttorney,  # 提货委托书
            'consignorName': consignorName,  # 提货人姓名
            'consignorPhone': consignorPhone  # 提货人电话
        }
    }
    # 物资信息
    goods = {
        'goodsId': goodsId,
        'quantity': goodsQuantity,
        # 'supplierId': goodsSupplierId
    }
    body['goodsDetailUiBeans'] = [goods]
    if kitTemplateId != None:
        # 工具包信息
        tools = {
            "kitTemplateId": kitTemplateId,
            "quantity": 1,
            # "supplierId": goodsSupplierId
        }
        body['toolsDetailUiBeans'] = [tools]
    # 创建临调单
    create = request.post_body('/adhocOrder/appCreate', body=body)
    return create


# 创建临调单
def createAdhocOrder(goodsId, goodsQuantity=1, kitTemplateId=None, ageGroup='adult', gender='male',
                     goodsSupplierId=supplierId, supplierId=supplierId, hospitalName='测试', siteId=siteId,
                     surgeon=faker.name(), procedureTime=tomorrow_stamp, expectReturnTime=twoDaysAfter_stamp,
                     postcode=faker.postcode(), contactName='测试', contactPhone=faker.phone_number(),
                     manufacturerId=brandId, salesPerson=faker.name(), deliveryMode='DELIVERY',
                     receivingName=faker.name(), receivingIdCard=None, receivingPhone=faker.phone_number(),
                     districtCode=110101000000, receivingAddress=faker.address(), powerOfAttorney=None,
                     consignorName=None, consignorPhone=None):
    # # 查询商品主耗材列表
    # goods = request.get('/goods/findListByMainMaterial?pageNum=0&pageSize=50&manufacturerId=%d' % brandId)
    # goodsId = goods['data']['rows'][0]['id']
    # stockQuantity = goods['data']['rows'][0]['stockQuantity']

    # 创建临调单的参数
    body = {
        'toolsDetailUiBeans': [],
        'goodsDetailUiBeans': [],
        'orderUiBean': {
            'ageGroup': ageGroup,  # 年龄段
            'gender': gender,  # 性别
            'supplierId': supplierId,
            'hospitalName': hospitalName,
            'procedureSite': [siteId],
            'surgeon': surgeon,
            'procedureTime': procedureTime,
            'expectReturnTime': expectReturnTime,
            'postcode': postcode,
            'contactName': contactName,
            'contactPhone': contactPhone,
            'manufacturerId': manufacturerId,
            'salesPerson': salesPerson,
            'deliveryMode': deliveryMode,  # 快递DELIVERY  自提SELF_PIKE_UP
            'receivingName': receivingName,
            'receivingIdCard': receivingIdCard,
            'receivingPhone': receivingPhone,
            'districtCode': districtCode,
            'receivingAddress': receivingAddress,
            # 'powerOfAttorney': powerOfAttorney,
            # 'consignorName': consignorName,
            # 'consignorPhone': consignorPhone
        }
    }
    # 物资信息
    goods = {
        'goodsId': goodsId,
        'quantity': goodsQuantity,
        'supplierId': goodsSupplierId
    }
    body['goodsDetailUiBeans'] = [goods]
    if kitTemplateId != None:
        # 工具包信息
        tools = {
            "kitTemplateId": kitTemplateId,
            "quantity": 1,
            # "supplierId": goodsSupplierId
        }
        body['toolsDetailUiBeans'] = [tools]
    # 创建临调单
    create = request.post_body('/adhocOrder/create', body=body)
    return create


# 小程序编辑临调单
def app_edit_order(id, goodsDetail, toolsDetail):
    body = {
        'id': id,
        'goodsDetailUiBeans': goodsDetail,
        'toolsDetailUiBeans': toolsDetail
    }
    response = request.put_body('/adhocOrder/appEdit', body=body)
    return response


# web 编辑临调单
def edit_order(id, goodsId=320, goodsQuantity=1, kitTemplateId=None, ageGroup='adult', gender='male',
               goodsSupplierId=supplierId, supplierId=supplierId, hospitalName='测试', siteId=siteId,
               surgeon=faker.name(), procedureTime=tomorrow_stamp, expectReturnTime=twoDaysAfter_stamp,
               postcode=faker.postcode(), contactName='测试', contactPhone=faker.phone_number(),
               manufacturerId=brandId, salesPerson=faker.name(), salesPhone=faker.phone_number(),
               deliveryMode='SELF_PIKE_UP',
               receivingName=faker.name(), receivingIdCard=None, receivingPhone=faker.phone_number(),
               districtCode=110101000000, receivingAddress=faker.address(), powerOfAttorney=None,
               consignorName=None, consignorPhone=None):
    body = {
        'goodsDetailUiBeans': [],
        'toolsDetailUiBeans': [],
        'orderUiBean': {
            "ageGroup": ageGroup,
            "consignorName": consignorName,
            "consignorPhone": consignorPhone,
            "contactName": contactName,
            "contactPhone": contactPhone,
            "deliveryMode": deliveryMode,
            "districtCode": districtCode,
            "expectReturnTime": expectReturnTime,
            "gender": gender,
            "hospitalName": hospitalName,
            "id": id,
            "manufacturerId": manufacturerId,
            # "payOnDelivery": False,
            "postcode": postcode,
            "powerOfAttorney": powerOfAttorney,
            "procedureSite": [siteId],
            "procedureTime": procedureTime,
            "receivingAddress": receivingAddress,
            "receivingIdCard": receivingIdCard,
            "receivingName": receivingName,
            "receivingPhone": receivingPhone,
            "salesPerson": salesPerson,
            "salesPhone": salesPhone,
            "supplierId": supplierId,
            "surgeon": surgeon
        }
    }
    goods = {
        'goodsId': goodsId,
        'quantity': goodsQuantity
    }
    body['goodsDetailUiBeans'] = [goods]
    response = request.put_body('/adhocOrder/edit', body=body)
    return response


def edit_order1(orderUiBean, goodsDetail, toolsDetail):
    body = {
        'orderUiBean': orderUiBean,
        'goodsDetailUiBeans': goodsDetail,
        'toolsDetailUiBeans': toolsDetail
    }
    response = request.put_body('/adhocOrder/edit', body=body)
    return response


# 临时保存临调单  不需要了
# def saveAdhocOrder(goodsId, goodsQuantity=1, ageGroup='adult', gender='male', goodsSupplierId=supplierId,
#                    supplierId=supplierId, hospitalName='测试', siteId=siteId, surgeon=faker.name(),
#                    procedureTime=tomorrow_stamp, expectReturnTime=twoDaysAfter_stamp, postcode=faker.postcode(),
#                    contactName='测试', contactPhone=faker.phone_number(), manufacturerId=brandId,
#                    salesPerson=faker.name(), deliveryMode='SELF_PIKE_UP', receivingName=faker.name(),
#                    receivingPhone=faker.phone_number(), districtCode=110101000000, receivingAddress=faker.address()):
#     # # 查询商品主耗材列表
#     # goods = request.get('/goods/findListByMainMaterial?pageNum=0&pageSize=50&manufacturerId=%d' % brandId)
#     # goodsId = goods['data']['rows'][0]['id']
#     # stockQuantity = goods['data']['rows'][0]['stockQuantity']
#
#     # 创建临调单的参数
#     body = {
#         'toolsDetailUiBeans': [],
#         'goodsDetailUiBeans': [],
#         'orderUiBean': {
#             'ageGroup': ageGroup,  # 年龄段
#             'gender': gender,  # 性别
#             'supplierId': supplierId,
#             'hospitalName': hospitalName,
#             'procedureSite': [siteId],
#             'surgeon': surgeon,
#             'procedureTime': procedureTime,
#             'expectReturnTime': expectReturnTime,
#             'postcode': postcode,
#             'contactName': contactName,
#             'contactPhone': contactPhone,
#             'manufacturerId': manufacturerId,
#             'salesPerson': salesPerson,
#             'deliveryMode': deliveryMode,  # 快递DELIVERY  自提SELF_PIKE_UP
#             'receivingName': receivingName,
#             # 'receivingIdCard': receivingIdCard,
#             'receivingPhone': receivingPhone,
#             'districtCode': districtCode,
#             'receivingAddress': receivingAddress,
#             # 'powerOfAttorney': powerOfAttorney,
#             # 'consignorName': consignorName,
#             # 'consignorPhone': consignorPhone
#         }
#     }
#     # 物资信息
#     goods = {
#         'goodsId': goodsId,
#         'quantity': goodsQuantity,
#         'supplierId': goodsSupplierId
#     }
#     body['goodsDetailUiBeans'] = [goods]
#     # 创建临调单 adhoc
#     save = request.post_body('/adhocOrder/save', body=body)
#     return save


def updateAddress(orderId, consignorName=faker.name(), consignorPhone=faker.phone_number(), deliveryMode='SELF_PIKE_UP',
                  districtCode=110101000000, payOnDelivery=True, postcode=faker.postcode(), file='file',
                  receivingAddress=faker.address(), receivingIdCard=faker.ssn(), receivingName=faker.name(),
                  receivingPhone=faker.phone_number()):
    body = {
        'consignorName': consignorName,  # 提货人姓名
        'consignorPhone': consignorPhone,  # 提货人电话
        'deliveryMode': deliveryMode,  # 收货方式
        'districtCode': districtCode,  # 收件区域
        'orderId': orderId,
        'payOnDelivery': payOnDelivery,  # 是否到付
        'postcode': postcode,
        'powerOfAttorney': file,  # 提货委托书
        'receivingAddress': receivingAddress,  # 收件地址
        'receivingIdCard': receivingIdCard,  # 身份证号
        'receivingName': receivingName,  # 收件人
        'receivingPhone': receivingPhone  # 收件人联系电话
    }
    response = request.post_body('/adhocOrder/updateAddress', body=body)
    return response


# 根据临调单id查看详情
def getDetail(adhocOrderId):
    log.info('------小程序查询临调订单明细------')
    response = request.get_params('/adhocOrder/getDetail', params={'orderId': adhocOrderId})
    assert response['msg'] == '请求成功'
    log.info('------查询订单详情------')
    response2 = request.get_params('/adhocOrder/getDetailByOrderId', params={'orderId': adhocOrderId})
    assert response2['msg'] == '请求成功'
