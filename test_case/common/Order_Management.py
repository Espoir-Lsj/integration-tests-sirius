# -*- coding: utf-8 -*-
# @Time : 2021/5/17 3:18 下午 
# @Author : lsj
# @File : Order_Management.py
import time, datetime
from faker import Faker
from common import request, login

faker = Faker(locale='zh_CN')

timeStamp = int(time.time() * 1000)
today = datetime.date.today()
fiveDaysAfter = today + datetime.timedelta(days=5)
fiveDaysAfter_stamp = int(time.mktime(fiveDaysAfter.timetuple())) * 1000
supplierId = login.supplierId


# 订单管理：临调订单
class AdhocOrder:
    # 获取经销商ID

    # 获取品牌id
    def get_manufacturerId(self):
        url = '/formBaseData/allBrands'
        response = request.get(url)
        try:
            response['msg'] == '请求成功'
        except Exception:
            raise response
        manufacturerId = response['data'][0]['id']
        return manufacturerId

    # 获取手术部位
    def get_procedureSite(self):
        url = '/dictionary/getByType/procedure_site'
        response = request.get(url)
        try:
            response['msg'] == '请求成功'
        except Exception:
            raise response
        procedureSite = response['data'][0]['id']
        return procedureSite

    # 获取患者年龄段
    def get_ageGroup(self):
        url = '/dictionary/getByType/age_group'
        response = request.get(url)
        try:
            response['msg'] == '请求成功'
        except Exception:
            raise response
        ageGroup = response['data'][0]['code']
        return ageGroup

    # 设置默认地址 （这里有权限鉴别 决定用功能测试实现,目前登录的是有权限的账户）
    def add_default_address(self):
        url = '/supplier/addReceivingAddress'
        body = {
            "receivingName": "收件人",
            "receivingPhone": "13333333338",
            "districtCode": 110101000000,  # 地址代码
            "receivingAddress": "详情地址"
        }
        response = request.post_body(url, body)

    # 获取默认地址ID
    def get_addressId(self):
        url = '/supplier/getReceivingAddress?dealerId=%s' % supplierId
        response = request.get(url)
        try:
            response['msg'] == '请求成功'
        except Exception:
            raise response
        addressId = response['data'][0]['id']
        return addressId

    # 获取商品信息
    def get_goodsInfo(self):
        url = '/goods/findGoodsList?pageNum=0&pageSize=50&manufacturerId=1'
        response = request.get(url)
        goodsId = response['data']['rows'][0]['id']
        supplierId = response['data']['rows'][0]['supplierId']
        return goodsId, supplierId

    # 获取工具包信息
    def get_toolsInfo(self):
        url = '/kitTemplate/findToolsKitList?pageNum=0&pageSize=50&manufacturerId=1'
        response = request.get(url)
        kitTemplateId = response['data']['rows'][0]['id']
        toolsSupplierId = response['data']['rows'][0]['supplierId']
        return kitTemplateId, toolsSupplierId

    # 创建临调单
    def adhocOrder_create(self, procedureSite=95, procedureTime=timeStamp, expectReturnTime=fiveDaysAfter_stamp,
                          manufacturerId=None, gender='FEMALE', ageGroup='TEENAGERS', deliveryMode='SELF_PIKE_UP',
                          addressId=None, supplierId=supplierId, goodsId=None, goodsQuantity=1, goodsSupplierId=8,
                          kitTemplateId=None, toolsQuantity=1, toolsSupplierId=3, hospitalName="医院名称",
                          contactName="订单联系人", contactPhone="13333333333", receivingName="收件人", surgeon='主刀医生'
                          ):
        url = '/adhocOrder/create'
        body = {
            "toolsDetailUiBeans": [],
            "goodsDetailUiBeans": [],
            "orderUiBean": {
                "hospitalName": hospitalName,  # 医院名称
                "procedureSite": [procedureSite],  # 手术部位
                "surgeon": surgeon,  # 主刀医生
                "procedureTime": procedureTime,  # 手术日期
                "expectReturnTime": expectReturnTime,  # 归还日期
                "contactName": contactName,  # 订单联系人
                "contactPhone": contactPhone,  # 联系人电话
                "manufacturerId": manufacturerId,  # 品牌
                "salesPerson": "销售人员",  # 销售人员
                "gender": gender,  # 性别 ： 女
                "ageGroup": ageGroup,  # 患者年龄段 ：青少年
                "deliveryMode": deliveryMode,  # 提货方式 ：自提
                "payOnDelivery": True,  # 是否到付： 默认只能选择 到付
                "receivingName": receivingName,  # 收件人
                "consignorName": "提货人",  # 提货人
                "consignorPhone": "13212345567",  # 提货人电话
                "receivingIdCard": "421322199811044619",  # 提货人身份证号
                "powerOfAttorney": "http://192.168.10.254:9191/server/file/2021/05/17/5b15b54d-de1f-4aab-ab5b"
                                   "-ffe6bc5a6998/base64Test.jpg",  # 提货委托书照片
                "addressId": addressId,  # 默认地址
                "supplierId": supplierId  # 经销商ID
            }
        }
        goodsDetailUiBeans = {
            "goodsId": goodsId,  # 物资ID
            "quantity": goodsQuantity,  # 物资数量
            "supplierId": goodsSupplierId  # 物资供应商
        }
        toolsDetailUiBeans = {
            "kitTemplateId": kitTemplateId,  # 工具包ID
            "quantity": toolsQuantity,  # 工具包数量
            "supplierId": toolsSupplierId  # 工具包供应商
        }
        if goodsId is not None:
            body['goodsDetailUiBeans'].append(goodsDetailUiBeans)
        if kitTemplateId is not None:
            body['toolsDetailUiBeans'].append(toolsDetailUiBeans)
        if deliveryMode == 'DELIVERY':
            del body['consignorName'], body['consignorPhone'], body['receivingIdCard'], body['powerOfAttorney']
        response = request.post_body(url, body)
        try:
            response['msg'] == '请求成功'
        except Exception:
            raise response

    def all(self):
        # 品牌
        manufacturerId = self.get_manufacturerId()
        # 默认地址
        addressId = self.get_addressId()
        # 年龄段
        ageGroup = self.get_ageGroup()
        # 手术部位
        procedureSite = self.get_procedureSite()
        # 商品信息
        goodsInfo = self.get_goodsInfo()
        goodsId = goodsInfo[0]
        goodsSupplierId = goodsInfo[1]
        # 工具包信息
        toolsInfo = self.get_toolsInfo()
        kitTemplateId = toolsInfo[0]
        toolsSupplierId = toolsInfo[1]

        self.adhocOrder_create(procedureSite=procedureSite, manufacturerId=manufacturerId,
                               ageGroup=ageGroup, addressId=addressId, supplierId=supplierId,
                               goodsId=goodsId, goodsSupplierId=goodsSupplierId, kitTemplateId=kitTemplateId,
                               toolsSupplierId=toolsSupplierId)
        # 无工具包
        # self.adhocOrder_create(procedureSite=procedureSite, manufacturerId=manufacturerId,
        #                        ageGroup=ageGroup, addressId=addressId, supplierId=supplierId,
        #                        goodsId=goodsId, goodsSupplierId=goodsSupplierId,
        #                        toolsSupplierId=toolsSupplierId)


if __name__ == '__main__':
    test = AdhocOrder()
    # test.adhocOrder_create()
    test.get_manufacturerId()
