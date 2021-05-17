# -*- coding: utf-8 -*-
# @Time : 2021/5/17 3:18 下午 
# @Author : lsj
# @File : Order_Management.py
from faker import Faker
from common import request

faker = Faker(locale='zh_CN')


# 订单管理：临调订单
class AdhocOrder:

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
        ageGroup = response['data'][0]['id']
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
        url = '/getReceivingAddress?dealerId=1'
        url = '/dictionary/getByType/age_group'
        response = request.get(url)
        try:
            response['msg'] == '请求成功'
        except Exception:
            raise response
        addressId = response['data'][0]['id']
        return addressId

    # 创建临调单
    def adhocOrder_create(self):
        url = '/adhocOrder/create'
        body = {
            "toolsDetailUiBeans": [{
                "kitTemplateId": 23,  # 工具包ID
                "quantity": 1,  # 工具包数量
                "supplierId": 3  # 工具包供应商
            }],
            "goodsDetailUiBeans": [{
                "goodsId": 294,  # 物资ID
                "quantity": 1,  # 物资数量
                "supplierId": 8  # 物资供应商
            }],
            "orderUiBean": {
                "hospitalName": "医院名称",  # 医院名称
                "procedureSite": [95],  # 手术部位
                "surgeon": "主刀医生",  # 主刀医生
                "procedureTime": 1621243416029,  # 手术日期
                "expectReturnTime": 1621589016029,  # 归还日期
                "contactName": "订单联系人",  # 订单联系人
                "contactPhone": "13333333333",  # 联系人电话
                "manufacturerId": 1,  # 品牌
                "salesPerson": "销售人员",  # 销售人员
                "gender": "FEMALE",  # 性别 ： 女
                "ageGroup": "TEENAGERS",  # 患者年龄段 ：青少年
                "deliveryMode": "SELF_PIKE_UP",  # 提货方式 ：自提
                "payOnDelivery": True,  # 是否到付： 默认只能选择 到付
                "receivingName": "收件人",  # 收件人
                "consignorName": "提货人",  # 提货人
                "consignorPhone": "13212345567",  # 提货人电话
                "receivingIdCard": "421322199811044619",  # 提货人身份证好
                "powerOfAttorney": "http://192.168.10.254:9191/server/file/2021/05/17/5b15b54d-de1f-4aab-ab5b"
                                   "-ffe6bc5a6998/base64Test.jpg",  # 提货委托书照片
                "addressId": [],  # 默认地址
                "supplierId": 1
            }
        }

        response = request.post_body(url, body)


if __name__ == '__main__':
    test = AdhocOrder()
    test.create()
