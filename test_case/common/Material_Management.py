# -*- coding: utf-8 -*-
# @Time : 2021/5/8 11:02 上午 
# @Author : lsj
# @File : Material_Management.py
# 物资管理
import time, datetime

from common import request

timeStamp = int(time.time() * 1000)
today = datetime.date.today()
fiveDaysAfter = today + datetime.timedelta(days=5)
fiveDaysAfter_stamp = int(time.mktime(fiveDaysAfter.timetuple())) * 1000


# 物资管理： 物资 + 工具
class Goods:

    def __init__(self, Type):
        """
        实例变量，调用类的时候传 type
        :param Type: 物资： 'material' /  工具：'tool'
        """
        self.type = Type

    # 通过关键字查询列表(物资、工具)
    def getList(self, webKeyword=None, Type='material'):
        """

        :param webKeyword: 关键字
        :param Type: 'material' : 物资 、'tool' : 工具
        :return:
        """
        url = '/goods/queryGoodsList'
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'type': Type,
            'webKeyword': webKeyword
        }
        response = request.get_params(url, params)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response
        # 获取物资 id
        id = response['data']['rows'][0]['id']
        return id

    # 编辑 Di 码
    def edit_GoodsDi(self, di, webKeyword=timeStamp):
        url = '/goods/editGoodsDi'
        id = self.getList(webKeyword=webKeyword, )
        body = {
            "di": di,
            "id": id
        }
        response = request.put_body(url, body)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response

    # 创建物资 type = 'material'
    # 创建工具 type = 'tool'
    def create_Goods(self, name=str(timeStamp), skuCode=timeStamp, goodsCategory=101,
                     maintenanceCategory=126, manufacturerId=1, minGoodsUnit=23, origin='测试地址',
                     nearExpirationDate=5, std2012Category=373, storageConditions=100, model='333',
                     specification='222',
                     imageSource='/file/2021/05/08/699fac64-f246-44c2-b6d9-95fbca00b716/base64Test.jpeg',
                     registrationImg='/file/2021/05/08/699fac64-f246-44c2-b6d9-95fbca00b716/base64Test.jpeg',
                     longEffect=False, registrationEndDate=fiveDaysAfter_stamp, registrationBeginDate=timeStamp,
                     registrationNum='123456'):
        url = '/goods/createGoods'
        body = {
            "type": self.type,  # 物资
            "goodsCategory": goodsCategory,
            "maintenanceCategory": maintenanceCategory,
            "manufacturerId": manufacturerId,
            "minGoodsUnit": minGoodsUnit,
            "name": name,  # 物资名字
            "origin": origin,  # 产地
            "nearExpirationDate": nearExpirationDate,  # 近效期
            "std2012Category": std2012Category,
            "storageConditions": storageConditions,
            "specificationList": [{
                "model": model,  # 型号
                "skuCode": skuCode,  # 原厂编码 -- 不可重复
                "specification": specification,  # 规格
                "imageSource": [imageSource],  # 商品照片
                "createRegistrationInfoUiList": [{
                    "longEffect": longEffect,  # 是否长期有效
                    "registrationEndDate": registrationEndDate,  # 注册证失效日期
                    "registrationBeginDate": registrationBeginDate,  # 注册证生效日期
                    "registrationImg": registrationImg,  # 注册证照
                    "registrationNum": registrationNum  # 注册证号
                }]
            }]
        }
        response = request.post_body(url, body)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response
        return timeStamp

    # 编辑物资 type = 'material'
    # 编辑工具 type = 'tool'
    def edit_Goods(self, webKeyword, name=str(timeStamp), skuCode=timeStamp, goodsCategory=101,
                   maintenanceCategory=126, manufacturerId=1, minGoodsUnit=23, origin='测试地址',
                   nearExpirationDate=5, std2012Category=373, storageConditions=100, model='333',
                   specification='222',
                   imageSource='/file/2021/05/08/699fac64-f246-44c2-b6d9-95fbca00b716/base64Test.jpeg',
                   registrationImg='/file/2021/05/08/699fac64-f246-44c2-b6d9-95fbca00b716/base64Test.jpeg',
                   longEffect=False, registrationEndDate=fiveDaysAfter_stamp, registrationBeginDate=timeStamp,
                   registrationNum='123456'):
        url = '/goods/editGoods'
        id = self.getList(webKeyword=webKeyword, Type=self.type)
        body = {
            "id": id,
            "name": name,
            "goodsCategory": goodsCategory,
            "maintenanceCategory": maintenanceCategory,
            "manufacturerId": manufacturerId,
            "minGoodsUnit": minGoodsUnit,
            "storageConditions": storageConditions,
            "nearExpirationDate": nearExpirationDate,
            "origin": origin,
            "model": model,
            "skuCode": skuCode,
            "specification": specification,
            "imageSource": [imageSource],
            "std2012Category": std2012Category,
            "registrationUiBeanList": [{
                "longEffect": longEffect,
                "registrationBeginDate": registrationBeginDate,
                "registrationEndDate": registrationEndDate,
                "registrationImg": registrationImg,
                "registrationNum": registrationNum
            }]
        }
        response1 = request.put_body(url, body)
        try:
            assert response1['msg'] == '请求成功'
        except Exception:
            raise response1

    # 删除物资 type = 'material'
    # 删除工具 type = 'tool'
    def delete_Goods(self, webKeyword):
        url = '/goods/deleteGoods'
        id = self.getList(webKeyword=webKeyword, Type=self.type)
        body = {
            'ids': [id]
        }
        response1 = request.put_body(url, body)
        try:
            assert response1['msg'] == '请求成功'
        except Exception:
            raise response1


class KitTemplate:
    # 获取工具包列表
    def get_KitTemplateList(self, toolKitName):
        """

        :param toolKitName: 工具包名称
        :return:
        """
        url = '/kitTemplate/queryToolsKitList'
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'toolKitName': toolKitName
        }
        response = request.get_params(url, params)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response
        # 获取工具包 id
        id = response['data']['rows'][0]['id']
        return id

    # 获取工具包模版列表
    def get_ToolsList(self):
        url = '/kitTemplate/queryToolsList'
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        response = request.get_params(url, params)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response
        # 获取工具包模版 id
        id = response['data']['rows'][0]['id']
        return id

    # 创建工具包
    def create_ToolsKit(self, goodsId=None, name=str(timeStamp), skuCode=timeStamp, remark='哈哈哈',
                        toolsKitCategory=174, manufacturerId=1, goodsQuantity=1):
        url = '/kitTemplate/addToolsKit'
        body = {
            "name": name,
            "skuCode": skuCode,
            "toolsKitCategory": toolsKitCategory,
            "manufacturerId": manufacturerId,
            "remark": remark,
            "toolsDetails": [{
                "goodsId": goodsId,
                "goodsQuantity": goodsQuantity
            }]
        }
        response = request.post_body(url, body)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response

    # 编辑工具包
    def edit_ToolsKit(self, goodsId=None, toolKitName=timeStamp, skuCode=timeStamp, remark='哈哈哈', goodsQuantity=1,
                      kitCategory=1, kitTemplateName=str(timeStamp), manufacturerId=1):
        kitTemplateId = self.get_KitTemplateList(toolKitName=toolKitName)
        url = '/kitTemplate/editToolsKit'
        body = {
            "skuCode": skuCode,
            "remark": remark,
            "manufacturerId": manufacturerId,
            "toolsDetails": [{
                "goodsId": goodsId,
                "goodsQuantity": goodsQuantity
            }],
            "kitCategory": kitCategory,
            "kitTemplateId": kitTemplateId,  # 工具包id
            "kitTemplateName": kitTemplateName
        }
        response = request.put_body(url, body)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response

    # 删除工具包
    def delete_ToolsKit(self, toolKitName=timeStamp):
        kitTemplateId = self.get_KitTemplateList(toolKitName=toolKitName)
        url = '/kitTemplate/deleteKitTemplate'
        body = {
            "ids": [kitTemplateId]
        }
        response = request.put_body(url, body)
        try:
            assert response['msg'] == '请求成功'
        except Exception:
            raise response


if __name__ == '__main__':
    # test = Goods('material')
    # # 物资
    # create = test.create_Goods()
    # test.edit_Goods(create)
    # test.delete_Goods(create)
    # # 工具
    # test = Goods('tool')
    # create = test.create_Goods()
    # test.edit_Goods(create)
    # test.delete_Goods(create)

    test = KitTemplate()
    ToolsId = test.get_ToolsList()
    test.create_ToolsKit(goodsId=ToolsId)
    test.edit_ToolsKit(goodsId=ToolsId)
    test.delete_ToolsKit()
