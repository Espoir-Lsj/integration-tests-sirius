# -*- coding: utf-8 -*-
# @Time : 2021/5/10 1:35 下午 
# @Author : lsj
# @File : test_material_management.py
# 物资管理case
import time, datetime

import allure
import pytest

from test_case.common import Material_Management, logger, request

timeStamp = int(time.time() * 1000)
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday_stamp = int(time.mktime(yesterday.timetuple())) * 1000
oneDaysAfter = today + datetime.timedelta(days=1)
oneDaysAfter_stamp = int(time.mktime(oneDaysAfter.timetuple())) * 1000
fiveDaysAfter = today + datetime.timedelta(days=5)
fiveDaysAfter_stamp = int(time.mktime(fiveDaysAfter.timetuple())) * 1000
log = logger.Log()


# 物资 工具接口
# @pytest.mark.TestGoods
# @pytest.mark.usefixtures('res_data')
@allure.feature('物资管理')
@allure.story('创建物资')
class TestGoods:
    Id = None
    goodsCategory = None

    # @allure.step('创建物资，返回物资ID')
    @pytest.fixture(scope="module")
    def create(self):
        log.info('------测试新增物资---------')
        test = Material_Management.Goods('material')
        TestGoods.goodsCategory = test.get_goodsCategory()
        test.create_Goods(name=timeStamp, goodsCategory=TestGoods.goodsCategory)
        Id = test.getList(timeStamp)
        TestGoods.Id = Id
        log.info('新增物资的ID：%s' % Id)
        yield
        test.delete_Goods(Id)

    @pytest.mark.主流程
    #   创建物资接口异常
    @allure.title('物资名称为空')
    def test_01(self):
        """物资名称为空"""
        response = Material_Management.Goods('material').create_Goods(name=None)
        assert response['msg'] == '请填写商品名称'

    @allure.title('skuCode为空')
    def test_02(self):
        """skuCode为空"""
        response = Material_Management.Goods('material').create_Goods(skuCode=None)
        assert response['msg'] == '请输入原厂编码'

    @allure.title('物资类别为空')
    def test_03(self):
        """物资类别为空"""
        response = Material_Management.Goods('material').create_Goods(goodsCategory=None)
        assert response['msg'] == '请选择耗材类型'

    @allure.title('养护类型为空')
    def test_04(self):
        """养护类型为空"""
        response = Material_Management.Goods('material').create_Goods(maintenanceCategory=None)
        assert response['msg'] == '请选择养护类别'

    @allure.title('生产企业为空')
    def test_05(self):
        """生产企业为空"""
        response = Material_Management.Goods('material').create_Goods(manufacturerId=None)
        assert response['msg'] == '请选择生产企业'

    @allure.title('产地为空')
    def test_06(self):
        """产地为空"""
        response = Material_Management.Goods('material').create_Goods(origin=None)
        assert response['msg'] == '请填写商品产地'

    @allure.title('基本单位为空')
    def test_07(self):
        """基本单位为空"""
        response = Material_Management.Goods('material').create_Goods(minGoodsUnit=None)
        assert response['msg'] == '请输入基本单位'

    @allure.title('型号为空')
    def test_08(self, create):
        """型号为空"""
        response = Material_Management.Goods('material').create_Goods(model=None, goodsCategory=self.goodsCategory,
                                                                      specification=None, skuCode=timeStamp + 1)
        assert response['msg'] == '请输入规格或型号'

    @allure.title('商品照片为空')
    def test_10(self):
        """商品照片为空"""
        response = Material_Management.Goods('material').create_Goods(imageSource=None)
        assert response['msg'] == '请添加图片'

    @allure.title('注册证照为空')
    def test_11(self):
        """注册证照为空"""
        response = Material_Management.Goods('material').create_Goods(registrationImg=None)
        assert response['msg'] == '请上传注册证照'

    @allure.title('注册证号为空')
    def test_12(self):
        """注册证号为空"""
        response = Material_Management.Goods('material').create_Goods(registrationNum=None)
        assert response['msg'] == '请输入注册证号'

    @allure.title('存储条件为空')
    def test_13(self):
        """存储条件为空"""
        response = Material_Management.Goods('material').create_Goods(storageConditions=None)
        assert response['msg'] == '请选择存储条件'

    @allure.title('物资分类 为空')
    def test_14(self):
        """物资分类 为空"""
        response = Material_Management.Goods('material').create_Goods(std2012Category=None)
        assert response['msg'] == '请选择物资分类'

    @allure.title('')
    def test_1401(self):
        """参数异常"""
        response = Material_Management.Goods('material').create_Goods(minGoodsUnit='kkk')
        assert response['msg'] == '请求参数异常'

    @allure.title('skuCode重复')
    def test_15(self, create):
        """skuCode重复"""
        response = Material_Management.Goods('material').create_Goods(goodsCategory=self.goodsCategory)
        response1 = Material_Management.Goods('material').create_Goods(goodsCategory=self.goodsCategory)
        assert response1['msg'] == '原厂编码已经存在'

    @allure.title('注册证生效日期大于失效时间')
    def test_16(self, create):
        """注册证生效日期大于失效时间"""
        response = Material_Management.Goods('material').create_Goods(skuCode=str(timeStamp + 1),
                                                                      registrationEndDate=oneDaysAfter_stamp,
                                                                      registrationBeginDate=fiveDaysAfter_stamp,
                                                                      goodsCategory=self.goodsCategory)
        assert response['msg'] == '注册证生效日期不能大于失效日期'

    @allure.title('注册证已失效')
    def test_1601(self, create):
        """注册证已失效"""
        response = Material_Management.Goods('material').create_Goods(skuCode=str(timeStamp + 1),
                                                                      registrationEndDate=yesterday_stamp,
                                                                      registrationBeginDate=yesterday_stamp,
                                                                      goodsCategory=self.goodsCategory)
        assert response['msg'] == '注册证已失效'

    @allure.title('Edit：商品名为空')
    #   编辑商品接口异常
    def test_17(self, create):
        """商品名为空"""
        response = Material_Management.Goods('material').edit_Goods(self.Id, name=None)
        assert response['msg'] == '请输入物资名称'

    @allure.title('Edit：原厂编码为空')
    def test_18(self, create):
        """原厂编码为空"""
        response = Material_Management.Goods('material').edit_Goods(self.Id, skuCode=None)
        assert response['msg'] == '请选择原厂编码'

    @allure.title('Edit：物资类别为空')
    def test_19(self, create):
        """物资类别为空"""
        response = Material_Management.Goods('material').edit_Goods(self.Id, goodsCategory=None)
        assert response['msg'] == '请选择耗材类型'

    @allure.title('Edit：养护类型为空')
    def test_20(self, create):
        """养护类型为空"""
        response = Material_Management.Goods('material').edit_Goods(self.Id, maintenanceCategory=None)
        assert response['msg'] == '请输入养护类别'

    @allure.title('Edit：生产企业为空')
    def test_21(self, create):
        """生产企业为空"""
        response = Material_Management.Goods('material').edit_Goods(self.Id, manufacturerId=None)
        assert response['msg'] == '请输入生产企业'

    @allure.title('Edit：产地为空')
    def test_2101(self, create):
        """产地为空"""
        response = Material_Management.Goods('material').edit_Goods(self.Id, origin=None)
        assert response['msg'] == '请输入商品产地'

    @allure.title('Edit基：本单位为空')
    def test_22(self, create):
        """基本单位为空"""
        response = Material_Management.Goods('material').edit_Goods(self.Id, minGoodsUnit=None)
        assert response['msg'] == '请选择基本单位'

    @allure.title('Edit：规格 /型号为空')
    def test_23(self, create):
        """规格 /型号为空"""
        response = Material_Management.Goods('material').edit_Goods(self.Id, model=None, specification=None)
        assert response['msg'] == '请输入规格或型号'

    #
    # def test_24(self, create):
    #     """规格为空"""
    #     response = Material_Management.Goods('material').edit_Goods(self.Id, specification=None)
    #     assert response['msg'] == '请选择规格'

    @allure.title('Edit：商品照片为空')
    def test_25(self, create):
        """商品照片为空"""
        response = Material_Management.Goods('material').edit_Goods(self.Id, imageSource=None
                                                                    , goodsCategory=self.goodsCategory)
        assert response['msg'] == '请选择上传图片'

    @allure.title('Edit：注册证照为空')
    def test_26(self, create):
        """注册证照为空"""
        response = Material_Management.Goods('material').edit_Goods(self.Id, registrationImg=None)
        assert response['msg'] == '请上传注册证照'

    @allure.title('Edit：注册证号为空')
    def test_27(self, create):
        """注册证号为空"""
        response = Material_Management.Goods('material').edit_Goods(self.Id, registrationNum=None)
        assert response['msg'] == '请输入注册证号'

    @allure.title('Edit：商品不存在')
    def test_2701(self, create):
        """商品不存在"""
        response = Material_Management.Goods('material').edit_Goods(id=0)
        assert response['msg'] == '商品不存在'

    @allure.title('Edit：存储条件为空')
    def test_28(self, create):
        """存储条件为空"""
        response = Material_Management.Goods('material').edit_Goods(self.Id, storageConditions=None)
        assert response['msg'] == '请选择存储条件'

    @allure.title('Edit：商品分类 为空')
    def test_29(self, create):
        """商品分类 为空"""
        response = Material_Management.Goods('material').edit_Goods(self.Id, std2012Category=None)
        assert response['msg'] == '请选择商品分类'

    @allure.title('Edit：参数异常')
    def test_2901(self, create):
        """ 参数异常"""
        response = Material_Management.Goods('material').edit_Goods('sss')
        assert response['msg'] == '请求参数异常'

    @allure.title('Edit：skuCode重复')
    def test_30(self, create):
        """skuCode重复"""
        response = Material_Management.Goods('material').create_Goods(fiveDaysAfter_stamp,
                                                                      goodsCategory=self.goodsCategory)
        assert response['msg'] == '原厂编码已经存在'

    @allure.title('Edit：注册证失效日期小于于生效日期')
    def test_3001(self):
        """注册证生效日期不能大于失效日期"""
        response = Material_Management.Goods('material').edit_Goods(self.Id, registrationEndDate=oneDaysAfter_stamp,
                                                                    registrationBeginDate=fiveDaysAfter_stamp)
        assert response['msg'] == '注册证生效日期不能大于失效日期'

    @allure.title('Edit：注册证已失效')
    def test_3002(self, create):
        """注册证已失效"""
        response = Material_Management.Goods('material').edit_Goods(self.Id, registrationEndDate=yesterday_stamp,
                                                                    registrationBeginDate=yesterday_stamp,
                                                                    goodsCategory=self.goodsCategory)
        assert response['msg'] == '注册证已失效'

    # 编辑di码
    @allure.title('di码为空')
    def test_31(self, create):
        """di码为空"""
        response = Material_Management.Goods('material').edit_GoodsDi(None, self.Id)
        assert response['msg'] == '请填写物资di码'

    @allure.title('di码 少于14位')
    def test_32(self, create):
        """di码 少于14位"""
        response = Material_Management.Goods('material').edit_GoodsDi(1, self.Id)
        assert response['msg'] == 'DI码长度异常，必须为14位'

    @allure.title('di码：商品ID为空')
    def test_33(self, create):
        """商品ID为空"""
        response = Material_Management.Goods('material').edit_GoodsDi(12345671234567, None)
        assert response['msg'] == '请选择要编辑的物资'

    # 编辑价格
    @allure.title('price:商品ID为空')
    def test_41(self, create):
        """商品ID为空"""
        response = Material_Management.Goods('material').edit_price(None)
        assert response['msg'] == '请填写商品id'

    @allure.title('price:折扣率为0')
    def test_42(self, create):
        """折扣率为0"""
        response = Material_Management.Goods('material').edit_price(self.Id, discountRate=0)
        assert response['msg'] == '折扣率不能为空或小于0'

    @allure.title('price:税率为0')
    def test_43(self, create):
        """税率为0"""
        response = Material_Management.Goods('material').edit_price(self.Id, taxRate=0)
        assert response['msg'] == '税率不能为空或小于0'

    @allure.title('price:采购价格为0')
    def test_44(self, create):
        """采购价格为0"""
        response = Material_Management.Goods('material').edit_price(self.Id, purchasePrice=0)
        assert response['msg'] == '采购价格不能为空或小于0'

    @allure.title('price:临调价为0')
    def test_45(self, create):
        """临调价为0"""
        response = Material_Management.Goods('material').edit_price(self.Id, type='adhoc', price=0)
        assert response['msg'] == '临调价格不能小于0'

    @allure.title('price:请求参数异常')
    def test_46(self, create):
        """请求参数异常"""
        response = Material_Management.Goods('material').edit_price(self.Id, type='adhoc', price='ss')
        assert response['msg'] == '请求参数异常'

    @allure.title('price:商品不存在')
    def test_46(self, create):
        """请求参数异常"""
        response = Material_Management.Goods('material').edit_price(99999999999, type='adhoc', price='0')
        assert response['msg'] == '未找到该物资，请刷新后重试'

    @allure.title('删除物资')
    def test_47(self, create):
        """删除物资"""
        response = Material_Management.Goods('material').delete_Goods(self.Id)
        assert response['msg'] == '请求成功'


# 新建工具包
# @pytest.mark.TestKitTemplate
@pytest.mark.usefixtures('res_data')
@allure.feature('物资管理')
@allure.story('创建工具包')
class TestKitTemplate:
    toolsId = None
    goodsId = None
    toolsKitCategory = None
    data = [()]

    @pytest.fixture(scope="class")
    def create(self):
        timeStamp1 = timeStamp
        TestKitTemplate.toolsKitCategory = Material_Management.KitTemplate().get_toolsKitCategoryId()
        TestKitTemplate.goodsId = Material_Management.KitTemplate().get_ToolsList()
        response = Material_Management.KitTemplate().create_ToolsKit(TestKitTemplate.goodsId,
                                                                     name=timeStamp1,
                                                                     toolsKitCategory=TestKitTemplate.toolsKitCategory)
        TestKitTemplate.toolsId = Material_Management.KitTemplate().get_KitTemplateList(timeStamp1)

    # 创建工具包接口异常
    def test_01(self, create):
        """商品ID 为空"""
        response = Material_Management.KitTemplate().create_ToolsKit(None, toolsKitCategory=self.toolsKitCategory)
        assert response['msg'] == '参数异常，请刷新后重试'

    def test_02(self):
        """商品ID 错误"""
        response = Material_Management.KitTemplate().create_ToolsKit('None')
        assert response['msg'] == '请求参数异常'

    def test_03(self, create):
        """工具包名字 为空"""
        response = Material_Management.KitTemplate().create_ToolsKit(self.toolsId, name=None,
                                                                     toolsKitCategory=self.toolsKitCategory)
        assert response['msg'] == '工具包名称不能为空'

    def test_04(self, create):
        """原厂编码为空"""
        response = Material_Management.KitTemplate().create_ToolsKit(self.goodsId, skuCode=None,
                                                                     toolsKitCategory=self.toolsKitCategory)
        assert response['msg'] == '原厂编码不能为空'

    def test_05(self, create):
        """工具包类型 为空"""
        response = Material_Management.KitTemplate().create_ToolsKit(self.goodsId, toolsKitCategory=None)
        assert response['msg'] == '请选择工具包类型'

    def test_06(self, create):
        """生成企业 为空"""
        response = Material_Management.KitTemplate().create_ToolsKit(self.goodsId, manufacturerId=None,
                                                                     toolsKitCategory=self.toolsKitCategory)
        assert response['msg'] == '请选择生产企业'

    def test_0601(self, create):
        """工具包类型异常"""
        response = Material_Management.KitTemplate().create_ToolsKit(self.goodsId, skuCode=timeStamp + 1,
                                                                     toolsKitCategory=111111)
        assert response['msg'] == '工具包类型异常，请刷新后重试'

    def test_07(self, create):
        """商品数量 为空"""
        response = Material_Management.KitTemplate().create_ToolsKit(self.goodsId, goodsQuantity=None,
                                                                     skuCode=str(timeStamp + 1),
                                                                     toolsKitCategory=self.toolsKitCategory)
        assert response['msg'] == '参数异常，请刷新后重试'

    # def test_0701(self, create):
    #     """工具包描述 为空"""
    #     response = Material_Management.KitTemplate().create_ToolsKit(self.goodsId, remark=None,
    #                                                                  skuCode=str(timeStamp + 1),
    #                                                                  toolsKitCategory=self.toolsKitCategory)
    #     assert response['msg'] == ''

    # 编辑工具包接口异常
    def test_08(self, create):
        """工具包ID为空"""
        response = Material_Management.KitTemplate().edit_ToolsKit(self.goodsId, None)
        assert response['msg'] == '参数异常，请刷新后重试'

    def test_09(self, create):
        """工具包类型异常"""
        response = Material_Management.KitTemplate().edit_ToolsKit(self.goodsId, self.toolsId, kitCategory=909999)
        assert response['msg'] == '工具包类型异常，请刷新后重试'

    # def test_10(self, create):
    #     """原厂编码已经存在"""
    #     response = Material_Management.KitTemplate().edit_ToolsKit(self.goodsId, self.toolsId, skuCode=timeStamp)
    #     assert response['msg'] == '原厂编码已经存在"'

    def test_11(self, create):
        """工具包描述为空"""
        response = Material_Management.KitTemplate().edit_ToolsKit(self.goodsId, self.toolsId, remark=None)
        assert response['msg'] == '请填写工具包描述'

    def test_12(self, create):
        """生产企业为空"""
        response = Material_Management.KitTemplate().edit_ToolsKit(self.goodsId, self.toolsId, manufacturerId=None)
        assert response['msg'] == '请选择生产企业'

    def test_13(self, create):
        """工具包类型为空"""
        response = Material_Management.KitTemplate().edit_ToolsKit(self.goodsId, self.toolsId, kitCategory=None)
        assert response['msg'] == '请选择工具包类型'

    def test_14(self, create):
        """工具包名称为空"""
        response = Material_Management.KitTemplate().edit_ToolsKit(self.goodsId, self.toolsId, kitTemplateName=None)
        assert response['msg'] == '请填写工具包名称'

    # 设置工具包租用费
    def test_15(self, create):
        """工具包ID为空"""
        response = Material_Management.KitTemplate().edit_Price(None, 10000)
        assert response['msg'] == '参数异常，请刷新后重试'

    def test_16(self, create):
        """工具包 租用费为空"""
        response = Material_Management.KitTemplate().edit_Price(self.toolsId, None)
        assert response['msg'] == '请输入工具包租用费'

    def test_17(self, create):
        """工具包ID 错误"""
        response = Material_Management.KitTemplate().edit_Price("self.toolsId", 100)
        assert response['msg'] == '请求参数异常'

    def test_18(self, create):
        response = Material_Management.KitTemplate().delete_ToolsKit(self.toolsId)
        assert response['msg'] == '请求成功'


@pytest.mark.usefixtures('res_data')
@allure.feature('物资管理')
class TestPackagingOrder:
    templateIds = None
    warehouseId = None

    @pytest.fixture(scope="module")
    def get_allMsg(self):
        warehouseId = Material_Management.PackagingOrder().get_warehouse()
        templateIds = Material_Management.PackagingOrder().get_packagingFindTools(warehouseId)
        yield templateIds, warehouseId

    @pytest.fixture(scope="module")
    def get_toolsInfo(self, get_allMsg):
        response = Material_Management.PackagingOrder().add_tools(get_allMsg[0], get_allMsg[1])
        # kitTemplateId, kitTemplateName, warehouseId, goodsList, goodsLotInfoIdList, goodsQuantityList
        yield response

    data = [
        ('正向流程', {'templateIds': 'templateIds', 'warehouseId': 'warehouseId'}, '请求成功'),
        ('仓库未选择', {'templateIds': 'templateIds', 'warehouseId': None}, '参数异常，请刷新后重试'),
        ('工具包未选择', {'templateIds': None, 'warehouseId': 'warehouseId'}, '请选择工具包',)
    ]

    # ids = ['正向流程',
    #        '仓库未选择',
    #        '工具包未选择'
    #        ]
    @allure.story('添加工具')
    @allure.title('{title}')
    @pytest.mark.parametrize('title,case,expected', data)
    def test_add_tools(self, title, case, expected, get_allMsg):
        if case['templateIds'] == 'templateIds':
            case['templateIds'] = get_allMsg[0]
        if case['warehouseId'] == 'warehouseId':
            case['warehouseId'] = get_allMsg[1]
        url = '/stockBaseData/findAvailableGoodsStockByTemplateId'
        params = {
            'templateIds': case['templateIds'],
            'warehouseId': case['warehouseId']
        }
        response = request.get_params(url, params)
        assert response['msg'] == expected

    @pytest.fixture(scope='class')
    def get_create_tools(self):
        test = Material_Management.PackagingOrder()
        warehouseId = test.get_warehouse()
        templateIds = test.get_packagingFindTools(warehouseId)
        infoList = test.add_tools(templateIds, warehouseId)
        kitTemplateId = infoList[0]
        kitTemplateName = infoList[1]
        warehouseId = infoList[2]
        goodsList = infoList[3]
        goodsLotInfoIdList = infoList[4]
        goodsQuantityList = infoList[5]
        response = test.create_tools(kitTemplateId=kitTemplateId, warehouseId=warehouseId,
                                     kitTemplateName=kitTemplateName, goodsList=goodsList,
                                     goodsLotInfoIdList=goodsLotInfoIdList, goodsQuantityList=goodsQuantityList)

    data = [

        ('商品数量错误', {'goodsDetails': [{
            "goodsId": 11,
            "goodsLotInfoId": 88,
            "goodsQuantity": 2
        }]}, '数量不一致，请确定数量'),
        ('仓库为空', {'warehouseId': None}, '请选择仓库'),
        ('仓库错误', {'warehouseId': 999999}, '当前用户不能在该仓库创建加工单'),

    ]

    @allure.story('创建加工组包')
    @pytest.mark.parametrize('title,case,expected', data)
    def test_create_tools(self, title, case, expected, get_create_tools):
        url = '/packagingOrder/create'
        body = request.body_replace(url, case)
        response = request.post_body01(url, body)
        if title == '商品数量错误':
            assert expected in response['msg']
        else:
            assert response['msg'] == expected
