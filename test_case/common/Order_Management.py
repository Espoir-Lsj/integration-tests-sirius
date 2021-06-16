# -*- coding: utf-8 -*-
# @Time : 2021/5/17 3:18 下午 
# @Author : lsj
# @File : Order_Management.py
import time, datetime
from faker import Faker
import request, login, Warehouse_Management

faker = Faker(locale='zh_CN')

timeStamp = int(time.time() * 1000)
today = datetime.date.today()
fiveDaysAfter = today + datetime.timedelta(days=5)
fiveDaysAfter_stamp = int(time.mktime(fiveDaysAfter.timetuple())) * 1000
supplierId = login.supplierId
dealerId = login.dealerId


# 订单管理：临调订单
class AdhocOrder:
    # # 获取生产企业
    # 获取品牌id
    def get_manufacturerId(self):
        url = '/fromBaseData/allBrands'
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

    # 设置默认地址
    def add_default_address(self):
        url = '/supplier/addReceivingAddress'
        body = {
            "receivingName": "收件人",
            "receivingPhone": "13333333338",
            "districtCode": 110101000000,  # 地址代码
            "receivingAddress": "详情地址"
        }
        response = request.post_body(url, body)
        addressId = response['data']
        return addressId

    def update_default_address(self, id=None):
        url = '/supplier/updateReceivingAddress'
        body = {
            "receivingName": "收件人",
            "receivingPhone": "13333333338",
            "districtCode": 110101000000,  # 地址代码
            "receivingAddress": "详情地址",
            "id": id
        }
        response = request.put_body(url, body)
        return response

    def delete_default_address(self, addressId=None):
        url = '/supplier/deleteReceivingAddress'
        body = {
            'id': addressId
        }
        response = request.delete_body(url, body)

    # 获取默认地址ID
    def get_addressId(self):
        url = '/supplier/getReceivingAddress?dealerId=%s' % dealerId
        response = request.get01(url)
        try:
            response['msg'] == '请求成功'
        except Exception:
            raise response
        addressId = response['data'][0]['id']
        return addressId

    # 获取仓库ID
    def get_warehouse(self):
        url = '/warehouse/getActualWarehouse'
        response = request.get(url)
        data = response['data']
        for i in data:
            if i['name'] == '骨科-丽都临调仓':
                warehouseId = i['id']
                return warehouseId

    # 获取商品信息
    def get_goodsInfo(self):
        url = '/stockBaseData/findGoodsList?pageNum=0&pageSize=50&manufacturerId={}&warehouseId={}' \
            .format(self.get_manufacturerId(), self.get_warehouse())
        response = request.get(url)
        goodsId = response['data']['rows'][0]['id']
        supplierId = response['data']['rows'][2]['supplierId']
        return goodsId, supplierId

    # 获取工具包信息
    def get_toolsInfo(self):
        url = '/stockBaseData/findToolsKitList?pageNum=0&pageSize=50&manufacturerId={}&warehouseId={}' \
            .format(self.get_manufacturerId(), self.get_warehouse())
        response = request.get(url)
        kitTemplateId = response['data']['rows'][0]['id']
        toolsSupplierId = response['data']['rows'][0]['supplierId']
        return kitTemplateId, toolsSupplierId

    # 创建临调单
    def adhocOrder_create(self, procedureSite=95, procedureTime=timeStamp, expectReturnTime=fiveDaysAfter_stamp,
                          manufacturerId=None, gender='FEMALE', ageGroup='TEENAGERS', deliveryMode='SELF_PIKE_UP',
                          addressId=None, supplierId=supplierId, goodsId=None, goodsQuantity=1, goodsSupplierId=None,
                          kitTemplateId=None, toolsQuantity=None, toolsSupplierId=None, hospitalName="医院名称",
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
        return response

    # 接收临调单
    def adhocOrder_accept(self, goodsId=None, Gquantity=None, kitTemplateId=None, Kquantity=None, warehouseId=None,
                          id=None):
        url = '/adhocOrder/accept'
        body = {
            "detail": [{
                "deliveryMode": "SELF_PIKE_UP",
                "goodsDetailUiBeans": [{
                    "goodsId": goodsId,
                    "quantity": Gquantity
                }],
                "toolsDetailUiBeans": [],
                "warehouseId": warehouseId
            }],
            "id": id
        }
        tools = {
            "kitTemplateId": kitTemplateId,
            "quantity": Kquantity
        }
        if kitTemplateId:
            body['detail'][0]['toolsDetailUiBeans'].append(tools)
        response = request.put_body01(url, body)

    # 拒绝临调单
    def adhocOrder_reject(self, reason="拒绝", id=None):
        url = '/adhocOrder/reject'
        body = {
            "reason": reason,
            "accept": False,
            "id": id
        }
        response = request.put_body01(url, body)

    # 编辑临调单
    def adhocOrder_edit(self, id=None, procedureSite=95, procedureTime=timeStamp, expectReturnTime=fiveDaysAfter_stamp,
                        manufacturerId=None, gender='FEMALE', ageGroup='TEENAGERS', deliveryMode='SELF_PIKE_UP',
                        addressId=None, supplierId=supplierId, goodsId=None, goodsQuantity=1, goodsSupplierId=8,
                        kitTemplateId=None, toolsQuantity=1, toolsSupplierId=None, hospitalName="医院名称",
                        contactName="订单联系人", contactPhone="13333333333", receivingName="收件人", surgeon='主刀医生'
                        ):
        url = '/adhocOrder/edit'
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
                "supplierId": supplierId,  # 经销商ID
                "id": id
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
        response = request.put_body(url, body)
        try:
            response['msg'] == '请求成功'
        except Exception:
            raise response
        return response

    # 提交销用
    def adhocOrder_return(self, childAdhocOrderId=None, goodsId=None, goodsLotInfoId=None, Usequantity=None,
                          parentAdhocOrderId=None):
        url = '/adhocOrder/adhocReturn'
        body = {
            "detail": [{
                "childAdhocOrderId": childAdhocOrderId,
                "goodsList": [{
                    "goodsId": goodsId,
                    "goodsLotInfoId": goodsLotInfoId,
                    "quantity": Usequantity
                }]
            }],
            "parentAdhocOrderId": parentAdhocOrderId
        }
        response = request.post_body(url, body)

    # 关闭临调单
    def adhocOrder_close(self, adhocOrderId=None):
        url = '/adhocOrder/close'
        body = {
            'id': adhocOrderId
        }
        response = request.put_body01(url, body)

    # 修改收货方式
    def adhocOrder_updataAddress(self, payOnDelivery=True, deliveryMode='SELF_PIKE_UP', consignorName='提货人',
                                 consignorPhone=13212345567, receivingIdCard=421322199811044619,
                                 powerOfAttorney='http://192.168.10.254:9191/server/file/2021/05/17/5b'
                                                 '15b54d-de1f-4aab-ab5b-ffe6bc5a6998/base64Test.jpg',
                                 orderId=None, addressId=None, parentId=None
                                 ):
        url = '/adhocOrder/updateAddress'
        body = {
            "parentId": parentId,
            "addressId": addressId,
            "payOnDelivery": payOnDelivery,
            "addressList": [{
                "orderId": orderId,
                "deliveryMode": deliveryMode,
                "powerOfAttorney": powerOfAttorney,
                "consignorName": consignorName,
                "consignorPhone": consignorPhone,
                "receivingIdCard": receivingIdCard
            }]
        }
        response = request.post_body(url, body)

    # 查询临调单列表
    def get_adhocOrder_list(self):
        url = '/adhocOrder/findList?pageNum=0&pageSize=50'
        response = request.get01(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response

    # 查询临调单详情
    def get_adhocOrder_detail(self, adhocOrderId):
        url = '/adhocOrder/getDetailByOrderId?orderId=%s' % adhocOrderId
        response = request.get01(url)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response

    # 查询商品批次号
    def get_goodsLotInfoId(self, adhocOrderId):
        url = '/adhocOrder/getWebAdhocOrderConsumed?id=%s' % adhocOrderId
        response = request.get01(url)
        get_goodsLotInfoId = response['data']['childList'][0]['goodsList'][0]['goodsLotInfoId']
        return get_goodsLotInfoId

    # 生成销售单
    def create_salesOrder(self, parentId=None, adhocOrderId=None, goodsId=None, goodsLotInfoId=None, Usequantity=None):
        url = '/salesOrder/checkSalesOrder'
        body = {
            "parentId": parentId,
            "createUiBeans": [{
                "adhocOrderId": adhocOrderId,
                "detailUiBeanList": [{
                    "goodsId": goodsId,
                    "goodsLotInfoId": goodsLotInfoId,
                    "quantity": Usequantity
                }]
            }]
        }
        response = request.post_body01(url, body)

    # 确认生成销售单
    def check_salesOrder(self, parentId=None, adhocOrderId=None, goodsId=None, goodsLotInfoId=None, Usequantity=None):
        url = '/salesOrder/checkSalesOrder'
        body = {
            "parentId": parentId,
            "createUiBeans": [{
                "adhocOrderId": adhocOrderId,
                "detailUiBeanList": [{
                    "goodsId": goodsId,
                    "goodsLotInfoId": goodsLotInfoId,
                    "quantity": Usequantity
                }]
            }]
        }
        response = request.post_body01(url, body)

    # 获取临调单 销用详情
    def get_Web_consumed(self, adhocOrderId):
        url = '/adhocOrder/getWebAdhocOrderConsumed?id=%s' % adhocOrderId
        response = request.get01(url)

    # 创建流程
    def all(self):
        # 品牌
        # manufacturerId = self.get_manufacturerId()
        manufacturerId = 1
        # 默认地址
        addressId = self.add_default_address()
        # 仓库地址
        # warehouseId = self.get_warehouse()
        warehouseId = 3
        # 年龄段
        ageGroup = self.get_ageGroup()
        # 手术部位
        procedureSite = self.get_procedureSite()
        # 商品信息
        goodsInfo = self.get_goodsInfo()
        # goodsId = goodsInfo[0]
        goodsId = 20538
        goodsSupplierId = goodsInfo[1]
        # 工具包信息

        # 创建临调单
        data = self.adhocOrder_create(procedureSite=procedureSite, manufacturerId=manufacturerId,
                                      ageGroup=ageGroup, addressId=addressId, supplierId=supplierId,
                                      goodsId=goodsId, goodsSupplierId=goodsSupplierId,
                                      kitTemplateId=None,
                                      )
        adhocOrderId = data['data']['id']
        adhocOrderCode = data['data']['code']

        # 拒绝临调单
        self.adhocOrder_reject(id=adhocOrderId)
        # 编辑临调单
        self.adhocOrder_edit(id=adhocOrderId, procedureSite=procedureSite, procedureTime=timeStamp,
                             expectReturnTime=fiveDaysAfter_stamp,
                             manufacturerId=manufacturerId, ageGroup=ageGroup, addressId=addressId,
                             supplierId=supplierId, goodsId=goodsId,
                             goodsSupplierId=goodsSupplierId, goodsQuantity=10)
        # 接收临调单
        self.adhocOrder_accept(goodsId=goodsId, Gquantity=10,
                               warehouseId=warehouseId, id=adhocOrderId)

        # 更新收货地址
        self.adhocOrder_updataAddress(orderId=adhocOrderId, addressId=addressId, parentId=adhocOrderId)

        # 关闭临调单  待接收才可以关闭
        # self.adhocOrder_close(adhocOrderId=adhocOrderId)

        # 无工具包
        self.adhocOrder_create(procedureSite=procedureSite, manufacturerId=manufacturerId,
                               ageGroup=ageGroup, addressId=addressId, supplierId=supplierId,
                               goodsId=goodsId, goodsSupplierId=goodsSupplierId)
        self.delete_default_address(addressId)

    # 临调单主流程
    def all_process(self):
        # 品牌
        manufacturerId = self.get_manufacturerId()
        # 默认地址
        addressId = self.add_default_address()
        # 仓库地址
        warehouseId = self.get_warehouse()
        # 年龄段
        ageGroup = self.get_ageGroup()
        # 手术部位
        procedureSite = self.get_procedureSite()
        # 商品信息
        goodsInfo = self.get_goodsInfo()
        # goodsId = goodsInfo[0]
        goodsId = 20538
        goodsSupplierId = goodsInfo[1]
        # 工具包信息
        # toolsInfo = self.get_toolsInfo()
        # kitTemplateId = toolsInfo[0]
        kitTemplateId = None
        # toolsSupplierId = toolsInfo[1]
        Gquantity = 3
        # 创建临调单
        data = self.adhocOrder_create(goodsQuantity=Gquantity, procedureSite=procedureSite,
                                      manufacturerId=manufacturerId,
                                      ageGroup=ageGroup, addressId=addressId, supplierId=supplierId,
                                      goodsId=goodsId, goodsSupplierId=goodsSupplierId,
                                      kitTemplateId=None,
                                      toolsSupplierId=None)
        adhocOrderId = data['data']['id']
        adhocOrderCode = data['data']['code']

        # 接收临调单
        self.adhocOrder_accept(goodsId=goodsId, Gquantity=Gquantity, kitTemplateId=kitTemplateId, Kquantity=1,
                               warehouseId=warehouseId, id=adhocOrderId)
        # 发货流程：出库、拣货
        Warehouse_Management.All(adhocOrderCode).all_pick_out()

        # 获取批次号
        goodsLotInfoId = self.get_goodsLotInfoId(adhocOrderId)

        # 提交销用
        self.adhocOrder_return(childAdhocOrderId=adhocOrderId, goodsId=goodsId, goodsLotInfoId=goodsLotInfoId,
                               Usequantity=1, parentAdhocOrderId=adhocOrderId)
        # 收货流程：入库收货、验收
        Warehouse_Management.All(adhocOrderCode).all_in_putOnShelf()

        # 生成销售单
        # self.create_salesOrder(parentId=adhocOrderId, adhocOrderId=adhocOrderId, goodsId=goodsId,
        #                        goodsLotInfoId=goodsLotInfoId, Usequantity=1)
        # self.check_salesOrder(parentId=adhocOrderId, adhocOrderId=adhocOrderId, goodsId=goodsId,
        #                       goodsLotInfoId=goodsLotInfoId, Usequantity=1)

        self.delete_default_address(addressId)
        print('临调单号---------------%s' % adhocOrderCode)

        # 查询临调单列表
        self.get_adhocOrder_list()

        return adhocOrderCode


if __name__ == '__main__':
    test = AdhocOrder()
    # test.adhocOrder_create()
    # test.get_warehouse()

    test.all_process()
    # test.adhocOrder_return(182,20538,1,6,182)
