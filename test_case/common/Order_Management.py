# -*- coding: utf-8 -*-
# @Time : 2021/5/17 3:18 下午 
# @Author : lsj
# @File : Order_Management.py
import time, datetime
from faker import Faker
import request, login, Warehouse_Management
from test_case.common import PostgresSql

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
    def add_default_address(self, receivingName="收件人"):
        url = '/supplier/addReceivingAddress'
        body = {
            "receivingName": receivingName,
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
    def adhocOrder_create(self,
                          toolsDetailUiBeans=list(), goodsDetailUiBeans=list(), procedureSite=100,
                          procedureTime=timeStamp, expectReturnTime=fiveDaysAfter_stamp,
                          manufacturerId=None, gender='FEMALE', ageGroup='TEENAGERS', deliveryMode='SELF_PIKE_UP',
                          addressId=None, supplierId=supplierId, goodsId=None, goodsQuantity=1, goodsSupplierId=None,
                          kitTemplateId=None, toolsQuantity=None, toolsSupplierId=None, hospitalName="医院名称",
                          contactName="订单联系人", contactPhone="13333333333", receivingName="收件人", surgeon='主刀医生',

                          ):
        url = '/adhocOrder/create'
        body = {
            "toolsDetailUiBeans": toolsDetailUiBeans,
            "goodsDetailUiBeans": goodsDetailUiBeans,
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

        if goodsId:
            body['goodsDetailUiBeans'] = [goodsDetailUiBeans]
        if kitTemplateId:
            body['toolsDetailUiBeans'] = [toolsDetailUiBeans]
        if deliveryMode == 'DELIVERY':
            del body['orderUiBean']['consignorName'], body['orderUiBean']['consignorPhone'], body['orderUiBean'][
                'receivingIdCard'], body['orderUiBean']['powerOfAttorney']
        response = request.post_body(url, body)
        try:
            response['msg'] == '请求成功'
        except Exception:
            raise response
        return response

    # 创建临调单 多个商品+多个工具包
    def adhocOrder_create_more(self, goodsIds: list, goodsQuantity: list,
                               goodsSupplierId=None, addressId=None, manufacturerId=None):
        goodsDetailUiBeans = []
        toolsDetailUiBeans = []
        goods_acceptList = []
        toolsacceptList = []
        for goodsId, goodsQuantity in zip(goodsIds, goodsQuantity):
            goods = {
                "goodsId": goodsId,  # 物资ID
                "quantity": goodsQuantity,  # 物资数量
                "supplierId": goodsSupplierId  # 物资供应商
            }
            goods1 = {
                "goodsId": goodsId,
                "quantity": goodsQuantity
            }

            goodsDetailUiBeans.append(goods)
            goods_acceptList.append(goods1)
        res = self.adhocOrder_create(goodsDetailUiBeans=goodsDetailUiBeans, toolsDetailUiBeans=toolsDetailUiBeans,
                                     addressId=addressId,
                                     manufacturerId=manufacturerId)
        adhocOrderId = res['data']['id']

        return res, goodsDetailUiBeans, toolsDetailUiBeans, goods_acceptList, toolsacceptList

    # 获取拆单结果
    def get_result(self, orderId):
        url = '/adhocOrder/getAssignAdhocOrderResult?orderId=%s' % orderId
        response = request.get01(url)

    # 接收临调单
    def adhocOrder_accept(self, goodsDetailUiBeans=list(), toolsDetailUiBeans=list(), goodsId=None, Gquantity=None,
                          kitTemplateId=None, Kquantity=None, warehouseId=None,
                          id=None, deliveryMode="SELF_PIKE_UP"):
        url = '/adhocOrder/accept'
        body = {
            "detail": [{
                "deliveryMode": deliveryMode,
                "goodsDetailUiBeans": goodsDetailUiBeans,
                "toolsDetailUiBeans": toolsDetailUiBeans,
                "warehouseId": warehouseId
            }],
            "id": id
        }
        toolsDetailUiBeans = {
            "kitTemplateId": kitTemplateId,
            "quantity": Kquantity
        }
        goodsDetailUiBeans = {
            "goodsId": goodsId,
            "quantity": Gquantity
        }
        if goodsId:
            body['detail'][0]['goodsDetailUiBeans'] = [goodsDetailUiBeans]
        if kitTemplateId:
            body['detail'][0]['toolsDetailUiBeans'] = [toolsDetailUiBeans]
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
        if goodsId:
            body['goodsDetailUiBeans'].append(goodsDetailUiBeans)
        if kitTemplateId:
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
                          parentAdhocOrderId=None, goodsList=list()):

        url = '/adhocOrder/adhocReturn'
        body = {
            "detail": [{
                "childAdhocOrderId": childAdhocOrderId,
                "goodsList": goodsList
            }],
            "parentAdhocOrderId": parentAdhocOrderId
        }
        if goodsId:
            goods = {
                "goodsId": goodsId,
                "goodsLotInfoId": goodsLotInfoId,
                "quantity": Usequantity
            }
            body['detail'][0]['goodsList'] = [goods]
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
        return response

    # 查询商品批次号
    def get_goodsLotInfoId(self, adhocOrderId):
        url = '/adhocOrder/getWebAdhocOrderConsumed?id=%s' % adhocOrderId
        response = request.get01(url)
        get_goodsLotInfoId = response['data']['childList'][0]['goodsList'][0]['goodsLotInfoId']
        return get_goodsLotInfoId

    # 提交销用需要加入的参数
    def get_return_(self, adhocOrderId):
        data = request.get01('/adhocOrder/getWebAdhocOrderConsumed?id=%s' % adhocOrderId)

        goodsList = []
        for i in data['data']['childList'][0]['goodsList']:
            goods = {
                "goodsId": i['goodsId'],
                "goodsLotInfoId": i['goodsLotInfoId'],
                "kitStockId": None,
                "quantity": i['quantity']
            }
            goodsList.append(goods)
        return goodsList

    def get_goodsExtraAttrId(self, adhocOrderId):
        url = '/salesOrder/getDetailByAdhocId?adhocId=%s' % adhocOrderId
        response = request.get01(url)
        get_goodsLotInfoId = response['data']['childList'][0]['goodsUiList'][0]['goodsExtraAttrId']
        return get_goodsLotInfoId

    def get_salesOrder_details(self, adhocOrderId):
        url = '/salesOrder/getDetailByAdhocId?adhocId=%s' % adhocOrderId
        data = request.get01(url)['data']['childList'][0]['goodsUiList']
        goodsList = []
        for i in data:
            goods = {
                "goodsId": i['goodsId'],
                "goodsLotInfoId": i['goodsLotInfoId'],
                "goodsExtraAttrId": i['goodsExtraAttrId'],
                "quantity": i['receivedSaleQuantity']
            }
            goodsList.append(goods)
        return goodsList

    # 生成销售单
    def create_salesOrder(self, parentId=None, adhocOrderId=None, goodsId=None, goodsExtraAttrId=None,
                          goodsLotInfoId=None, Usequantity=None, warehouseId=None, detailUiBeanList=list()):
        url = '/salesOrder/createSalesOrder'
        body = {
            "parentId": parentId,
            "createUiBeans": [{
                "adhocOrderId": adhocOrderId,
                "warehouseId": warehouseId,
                "detailUiBeanList": detailUiBeanList
            }]
        }
        goods = {
            "goodsId": goodsId,
            "goodsLotInfoId": goodsLotInfoId,
            "goodsExtraAttrId": goodsExtraAttrId,
            "quantity": Usequantity
        }
        response = request.post_body01(url, body)

    # 确认生成销售单
    def check_salesOrder(self, parentId=None, adhocOrderId=None, goodsId=None, goodsLotInfoId=None,
                         goodsExtraAttrId=None, Usequantity=None, warehouseId=None, detailUiBeanList=list()):
        url = '/salesOrder/checkSalesOrder'
        body = {
            "parentId": parentId,
            "createUiBeans": [{
                "adhocOrderId": adhocOrderId,
                "warehouseId": warehouseId,
                "detailUiBeanList": detailUiBeanList
            }]
        }
        goods = {
            "goodsId": goodsId,
            "goodsLotInfoId": goodsLotInfoId,
            "goodsExtraAttrId": goodsExtraAttrId,
            "quantity": Usequantity
        }
        if goodsId:
            body['createUiBeans'][0]['detailUiBeanList'] = [goods]
        if goodsId:
            body['createUiBeans'][0]['detailUiBeanList'] = [goods]
        response = request.post_body01(url, body)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response

    # 获取临调单 销用详情
    def get_Web_consumed(self, adhocOrderId):
        url = '/adhocOrder/getWebAdhocOrderConsumed?id=%s' % adhocOrderId
        response = request.get01(url)

    # 创建流程
    def all(self):
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

        # 创建临调单
        data = self.adhocOrder_create(procedureSite=procedureSite,
                                      manufacturerId=manufacturerId,
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
        self.adhocOrder_create(goodsDetailUiBeans=[], toolsDetailUiBeans=[], procedureSite=procedureSite,
                               manufacturerId=manufacturerId,
                               ageGroup=ageGroup, addressId=addressId, supplierId=supplierId,
                               goodsId=goodsId, goodsSupplierId=goodsSupplierId)
        self.delete_default_address(addressId)

    # 临调单单物资主流程
    def all_process(self, Usequantity=None):
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
        Gquantity = 10
        # 使用数量
        Usequantity = Usequantity
        # 创建临调单
        data = self.adhocOrder_create(goodsQuantity=Gquantity,
                                      procedureSite=procedureSite,
                                      manufacturerId=manufacturerId,
                                      ageGroup=ageGroup, addressId=addressId, supplierId=supplierId,
                                      goodsId=goodsId, goodsSupplierId=goodsSupplierId,
                                      kitTemplateId=None,
                                      toolsSupplierId=None)
        adhocOrderId = data['data']['id']
        adhocOrderCode = data['data']['code']

        # 接收临调单
        self.adhocOrder_accept(goodsId=goodsId, Gquantity=Gquantity,
                               kitTemplateId=kitTemplateId, Kquantity=1,
                               warehouseId=warehouseId, id=adhocOrderId)
        # 发货流程：出库、拣货
        Warehouse_Management.All(adhocOrderCode).all_pick_out()

        # 获取批次号
        goodsLotInfoId = self.get_goodsLotInfoId(adhocOrderId)

        # 提交销用
        self.adhocOrder_return(childAdhocOrderId=adhocOrderId, goodsId=goodsId, goodsLotInfoId=goodsLotInfoId,
                               Usequantity=Usequantity, parentAdhocOrderId=adhocOrderId)
        print('临调单号-----%s----------------' % adhocOrderCode)

        # 收货流程：入库收货、验收
        Warehouse_Management.All(adhocOrderCode).all_in_putOnShelf()

        if Usequantity >= 0:
            goodsExtraAttrId = self.get_goodsExtraAttrId(adhocOrderId)

            # 生成销售单

            self.check_salesOrder(parentId=adhocOrderId, adhocOrderId=adhocOrderId, goodsId=goodsId,
                                  goodsLotInfoId=goodsLotInfoId, goodsExtraAttrId=goodsExtraAttrId,
                                  Usequantity=Usequantity,
                                  warehouseId=warehouseId)
            self.create_salesOrder(parentId=adhocOrderId, adhocOrderId=adhocOrderId, goodsId=goodsId,
                                   goodsLotInfoId=goodsLotInfoId, goodsExtraAttrId=goodsExtraAttrId,
                                   Usequantity=Usequantity,
                                   warehouseId=warehouseId)
        self.delete_default_address(addressId)
        #
        # # 查询临调单列表
        # self.get_adhocOrder_list()

        return adhocOrderCode

    # 临调单拆单主流程
    def all_process_spit(self, UsequantityList=None):
        """
         临调物资20539 :两个仓库（1，89）库存分别为10
         临调数量16: 1仓发货9，89仓发货7
         """
        goodsId = 20539
        warehouse1 = 1
        warehouse2 = 89
        goodsLotInfoId = 8962
        usequantity1 = UsequantityList[0]
        usequantity2 = UsequantityList[1]
        test = PostgresSql.PostgresSql()
        sql = """update wms_goods_stock set quantity = 10 where goods_id=20539 and status = 'put_on_shelf' and warehouse_id in (1,89)"""
        test.execute(sql)
        # 创建地址
        addressId = self.add_default_address(receivingName="拆单专用")
        # 创建临调单
        info = self.adhocOrder_create([], [], goodsId=goodsId, goodsQuantity=16, addressId=addressId, supplierId=216,
                                      manufacturerId=1, deliveryMode="DELIVERY")
        orderId = info['data']['id']
        orderCode = info['data']['code']
        self.get_result(orderId)
        # 审核临调单
        url = '/adhocOrder/accept'
        body = {
            "detail": [{
                "deliveryMode": "DELIVERY",
                "goodsDetailUiBeans": [{
                    "goodsId": goodsId,
                    "quantity": 9
                }],
                "toolsDetailUiBeans": [],
                "warehouseId": warehouse1
            }, {
                "deliveryMode": "DELIVERY",
                "goodsDetailUiBeans": [{
                    "goodsId": goodsId,
                    "quantity": 7
                }],
                "toolsDetailUiBeans": [],
                "warehouseId": warehouse2
            }],
            "id": orderId
        }
        response = request.put_body01(url, body)
        # 获取拆单结果
        data = self.get_adhocOrder_detail(orderId)['data']['childUiList']
        code1 = data[1]['childAdhocOrderUiBean']['code']
        code2 = data[0]['childAdhocOrderUiBean']['code']
        orderId1 = data[1]['childAdhocOrderUiBean']['id']
        orderId2 = data[0]['childAdhocOrderUiBean']['id']
        codelist = [code1, code2]
        self.delete_default_address(addressId)
        # 根据code 拣货出库
        # for i in codelist:
        #     Warehouse_Management.All(i).all_pick_out()
        Warehouse_Management.All(code1).all_pick_out()
        Warehouse_Management.All(code2).all_pick_out()
        # 提交销用
        url = '/adhocOrder/adhocReturn'
        body = {
            "detail": [{
                "childAdhocOrderId": orderId2,
                "goodsList": [{
                    "goodsId": goodsId,
                    "goodsLotInfoId": goodsLotInfoId,
                    "kitStockId": None,
                    "quantity": usequantity1
                }]
            }, {
                "childAdhocOrderId": orderId1,
                "goodsList": [{
                    "goodsId": goodsId,
                    "goodsLotInfoId": goodsLotInfoId,
                    "kitStockId": None,
                    "quantity": usequantity2
                }]
            }],
            "parentAdhocOrderId": orderId
        }
        response1 = request.post_body(url, body)

        # 根据code入库验收
        for i in codelist:
            Warehouse_Management.All(i).all_in_putOnShelf()

        # 生成销售单
        body = {
            "parentId": orderId,
            "createUiBeans": [{
                "adhocOrderId": orderId2,
                "warehouseId": warehouse2,
                "detailUiBeanList": [{
                    "goodsId": goodsId,
                    "goodsLotInfoId": goodsLotInfoId,
                    "goodsExtraAttrId": 8117,
                    "quantity": usequantity1
                }]
            }, {
                "adhocOrderId": orderId1,
                "warehouseId": warehouse1,
                "detailUiBeanList": [{
                    "goodsId": goodsId,
                    "goodsLotInfoId": goodsLotInfoId,
                    "goodsExtraAttrId": 8117,
                    "quantity": usequantity2
                }]
            }]
        }
        for i in ['/salesOrder/checkSalesOrder', '/salesOrder/createSalesOrder']:
            response2 = request.post_body01(i, body)
        print(orderCode)

    def all_process_more(self, goodsList=None, quantityList=None, Usequantity=None):

        addressId = self.add_default_address()
        manufacturerId = self.get_manufacturerId()
        warehouseId = self.get_warehouse()
        # goodsList = [20538, 20540]
        # quantityList = [1, 2]
        goodsList = goodsList
        quantityList = quantityList
        info = self.adhocOrder_create_more(goodsList, quantityList, addressId=addressId, manufacturerId=manufacturerId)
        res = info[0]
        goodsDetailUiBeans = info[3]
        orderId = res['data']['id']
        self.adhocOrder_accept(goodsDetailUiBeans, id=orderId, warehouseId=warehouseId)
        code = res['data']['code']
        Warehouse_Management.All(code).all_goods_pick()
        goodsList = self.get_return_(orderId)
        for x, y in zip(goodsList, Usequantity):
            x['quantity'] = y

        self.adhocOrder_return(parentAdhocOrderId=orderId, childAdhocOrderId=orderId, goodsList=goodsList)
        print(code)

        Warehouse_Management.All(code).all_goods_inbound()

        detailUiBeanList = self.get_salesOrder_details(orderId)
        self.check_salesOrder(parentId=orderId, adhocOrderId=orderId, detailUiBeanList=detailUiBeanList,
                              warehouseId=warehouseId)
        self.create_salesOrder(parentId=orderId, adhocOrderId=orderId, detailUiBeanList=detailUiBeanList,
                               warehouseId=warehouseId)


if __name__ == '__main__':
    test = AdhocOrder()
    # test.adhocOrder_create()
    # test.get_warehouse()

    # test.all()
    test.all_process(Usequantity=6)
    # test.all_process_spit([1, 1])
    # test.all_process_more([20538, 20540], [10, 10], [6, 0])
    # test.adhocOrder_return(182,20538,1,6,182)
    #
    # goodsList = [20538, 20540]
    # quantityList = [1, 2]
    # info = test.adhocOrder_create_more(goodsList, quantityList, addressId=428, manufacturerId=1)
    # # return res, goodsDetailUiBeans, toolsDetailUiBeans, goods_acceptList, toolsacceptList
    # res = info[0]
    # goodsDetailUiBeans = info[3]
    # orderId = res['data']['id']
    # test.adhocOrder_accept(goodsDetailUiBeans, id=orderId, warehouseId=1)
    # code = res['data']['code']
    # Warehouse_Management.All(code).all_goods_pick()
    # goodsList = test.get_return_(orderId)
    # test.adhocOrder_return(parentAdhocOrderId=orderId, childAdhocOrderId=orderId, goodsList=goodsList)
    # Warehouse_Management.All(code).all_goods_inbound()
    # print(code)
