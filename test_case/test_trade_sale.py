# __author:"zonglr"
# date:2020/12/11
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import datetime, time, jsonpath, random, pytest
from common import supplier_request, supplier_request_02, tradeSale
from common import logger

log = logger.Log()
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
# categoryId = ids[random.randint(0, len(ids))]
categoryId = 10


# 新增一个供应商A的售卖信息，fixture生效范围为每个class仅执行一次
@pytest.fixture(scope="class")
def addSale():
    response = tradeSale.addSale()
    assert response['msg'] == '请求成功'
    # 获取求购信息的id,并返回
    id = response['data']
    return id


# 新增一个供应商B的售卖信息，fixture生效范围为每个class仅执行一次
# @pytest.fixture(scope="class")
# def addSale_02():
#     response = tradeSale.addSale_02()
#     assert response['msg'] == '请求成功'
#     # 获取求购信息的id,并返回
#     id = response['data']
#     return id


class TestAdd:
    """新增售卖信息"""
    context = str('1').zfill(200)

    def test_01(self):
        """商品名称为空"""
        response = tradeSale.addSale(goodsName=None)
        assert response['msg'] == '请输入物资名称'

    def test_01_1(self):
        """商品名称超长"""
        response = tradeSale.addSale(goodsName=self.context)
        assert response['msg'] == '物资名称长度超出限制'

    def test_02(self):
        """规格型号为空"""
        # 型号默认为空，所以将规格设置为空即可
        response = tradeSale.addSale(specification=None)
        assert response['msg'] == '请输入规格/型号'

    def test_02_1(self):
        """规格超长"""
        response = tradeSale.addSale(specification=self.context)
        assert response['msg'] == '规格长度超出限制'

    def test_02_2(self):
        """型号超长"""
        response = tradeSale.addSale(model=self.context)
        assert response['msg'] == '型号长度超出限制'

    def test_03(self):
        """销售数量为空"""
        response = tradeSale.addSale(quantity=None)
        assert response['msg'] == '请输入物资数量'

    def test_03_1(self):
        """销售数量长度超过3位"""
        response = tradeSale.addSale(quantity=1000)
        assert response['msg'] == '最大不能超过999'

    def test_03_2(self):
        """销售数量为非数字"""
        response = tradeSale.addSale(quantity='%%')
        assert response['msg'] == '请求参数异常'

    def test_03_3(self):
        """销售数量为0"""
        response = tradeSale.addSale(quantity=0)
        assert response['msg'] == '最小不能小于1'

    def test_04(self):
        """单价为空"""
        response = tradeSale.addSale(price=None)
        assert response['msg'] == '请输入售价'

    def test_04_2(self):
        """单价超长"""
        response = tradeSale.addSale(price=10000000000000000000.11)
        assert response['msg'] == '请求参数异常'

    def test_05(self):
        """所属公司为空"""
        response = tradeSale.addSale(supplierName=None)
        assert response['msg'] == '请输入所属公司'

    def test_05_1(self):
        """求购公司超长"""
        response = tradeSale.addSale(supplierName=self.context)
        assert response['msg'] == '所属公司长度超出限制'

    def test_05_2(self):
        """求购公司不存在"""
        response = tradeSale.addSale(supplierName=0)
        assert response['msg'] == '所属公司不属于当前用户，请刷新重试'

    def test_06(self):
        """联系人为空"""
        response = tradeSale.addSale(contact=None)
        assert response['msg'] == '请输入联系人'

    def test_06_1(self):
        """联系人字段超长"""
        response = tradeSale.addSale(contact=self.context)
        assert response['msg'] == '联系人长度超出限制'

    def test_07(self):
        """联系电话为空"""
        response = tradeSale.addSale(contactPhone=None)
        assert response['msg'] == '请输入正确的手机号码'

    def test_07_1(self):
        """联系电话非数字"""
        response = tradeSale.addSale(contactPhone='%%%%')
        assert response['msg'] == '请输入正确的手机号码'

    def test_08(self):
        """发货地址为空"""
        response = tradeSale.addSale(deliveryArea=None)
        assert response['msg'] == '请选择发货地'

    def test_08_1(self):
        """收货地址值错误"""
        response = tradeSale.addSale(deliveryArea='test')
        assert response['msg'] == '请求参数异常'

    def test_09(self):
        """不存在的耗材类型"""
        response = tradeSale.addSale(category=0)
        assert response['msg'] == '该类型不存在'

    def test_10(self):
        """失效日期为空"""
        response = tradeSale.addSale(expirationDate=None)
        assert response['msg'] == '请输入失效日期'

    def test_10_1(self):
        """失效日期早于今天"""
        response = tradeSale.addSale(expirationDate=yesterday_stamp)
        assert response['msg'] == '失效日期不能早于或等于当天'

    def test_10_2(self):
        """失效日期等于今天"""
        response = tradeSale.addSale(expirationDate=today_stamp)
        assert response['msg'] == '失效日期不能早于或等于当天'

    def test_11(self):
        """物资照片为空"""
        response = tradeSale.addSale(imageResource=None)
        assert response['msg'] == '非法的参数值'

    def test_12(self):
        """新旧程度的值不存在"""
        response = tradeSale.addSale(newAndOldStandard='test')
        assert response['msg'] == '请求参数异常'

    def test_13(self):
        """是否有磨损的值不存在"""
        response = tradeSale.addSale(abrasionStandard='test')
        assert response['msg'] == '请求参数异常'

    def test_14(self):
        """包装完整的值不存在"""
        response = tradeSale.addSale(packingIntactStandard='test')
        assert response['msg'] == '请求参数异常'

    def test_15(self):
        """批次号为空"""
        response = tradeSale.addSale(lotNum=None)
        assert response['msg'] == '请输入批次/序列号'


class TestEdit:
    """编辑售卖信息"""
    context = str('1').zfill(200)

    def test_01(self, addSale):
        """商品名称为空"""
        response = tradeSale.editSale(id=addSale, goodsName=None)
        assert response['msg'] == '请输入物资名称'

    def test_01_1(self, addSale):
        """商品名称超长"""
        response = tradeSale.editSale(id=addSale, goodsName=self.context)
        assert response['msg'] == '物资名称长度超出限制'

    def test_02(self, addSale):
        """规格型号为空"""
        # 型号默认为空，所以将规格设置为空即可
        response = tradeSale.editSale(id=addSale, specification=None)
        assert response['msg'] == '请输入规格/型号'

    def test_02_1(self, addSale):
        """规格超长"""
        response = tradeSale.editSale(id=addSale, specification=self.context)
        assert response['msg'] == '规格长度超出限制'

    def test_02_2(self, addSale):
        """型号超长"""
        response = tradeSale.editSale(id=addSale, model=self.context)
        assert response['msg'] == '型号长度超出限制'

    def test_03(self, addSale):
        """销售数量为空"""
        response = tradeSale.editSale(id=addSale, quantity=None)
        assert response['msg'] == '请输入物资数量'

    def test_03_1(self, addSale):
        """销售数量长度超过3位"""
        response = tradeSale.editSale(id=addSale, quantity=1000)
        assert response['msg'] == '最大不能超过999'

    def test_03_2(self, addSale):
        """销售数量为非数字"""
        response = tradeSale.editSale(id=addSale, quantity='%%')
        assert response['msg'] == '请求参数异常'

    def test_03_3(self, addSale):
        """销售数量为0"""
        response = tradeSale.editSale(id=addSale, quantity=0)
        assert response['msg'] == '最小不能小于1'

    def test_04(self, addSale):
        """单价为空"""
        response = tradeSale.editSale(id=addSale, price=None)
        assert response['msg'] == '请输入售价'

    def test_04_2(self, addSale):
        """单价超长"""
        response = tradeSale.editSale(id=addSale, price=10000000000000000000.11)
        assert response['msg'] == '请求参数异常'

    def test_05(self, addSale):
        """所属公司为空"""
        response = tradeSale.editSale(id=addSale, supplierName=None)
        assert response['msg'] == '请输入所属公司'

    def test_05_1(self, addSale):
        """求购公司超长"""
        response = tradeSale.editSale(id=addSale, supplierName=self.context)
        assert response['msg'] == '所属公司长度超出限制'

    def test_05_2(self, addSale):
        """求购公司不存在"""
        response = tradeSale.editSale(id=addSale, supplierName=0)
        assert response['msg'] == '所属公司不属于当前用户，请刷新重试'

    def test_06(self, addSale):
        """联系人为空"""
        response = tradeSale.editSale(id=addSale, contact=None)
        assert response['msg'] == '请输入联系人'

    def test_06_1(self, addSale):
        """联系人字段超长"""
        response = tradeSale.editSale(id=addSale, contact=self.context)
        assert response['msg'] == '联系人长度超出限制'

    def test_07(self, addSale):
        """联系电话为空"""
        response = tradeSale.editSale(id=addSale, contactPhone=None)
        assert response['msg'] == '请输入正确的手机号码'

    def test_07_1(self, addSale):
        """联系电话非数字"""
        response = tradeSale.editSale(id=addSale, contactPhone='%%%%')
        assert response['msg'] == '请输入正确的手机号码'

    def test_08(self, addSale):
        """发货地址为空"""
        response = tradeSale.editSale(id=addSale, deliveryArea=None)
        assert response['msg'] == '请选择发货地'

    def test_08_1(self, addSale):
        """收货地址值错误"""
        response = tradeSale.editSale(id=addSale, deliveryArea='test')
        assert response['msg'] == '请求参数异常'

    def test_09(self, addSale):
        """不存在的耗材类型"""
        response = tradeSale.editSale(id=addSale, category=0)
        assert response['msg'] == '该类型不存在'

    def test_10(self, addSale):
        """失效日期为空"""
        response = tradeSale.editSale(id=addSale, expirationDate=None)
        assert response['msg'] == '请输入失效日期'

    def test_10_1(self, addSale):
        """失效日期早于今天"""
        response = tradeSale.editSale(id=addSale, expirationDate=yesterday_stamp)
        assert response['msg'] == '失效日期不能早于或等于当天'

    def test_10_2(self, addSale):
        """失效日期等于今天"""
        response = tradeSale.editSale(id=addSale, expirationDate=today_stamp)
        assert response['msg'] == '失效日期不能早于或等于当天'

    def test_11(self, addSale):
        """物资照片为空"""
        response = tradeSale.editSale(id=addSale, imageResource=None)
        assert response['msg'] == '非法的参数值'

    def test_12(self, addSale):
        """新旧程度的值不存在"""
        response = tradeSale.editSale(id=addSale, newAndOldStandard='test')
        assert response['msg'] == '请求参数异常'

    def test_13(self, addSale):
        """是否有磨损的值不存在"""
        response = tradeSale.editSale(id=addSale, abrasionStandard='test')
        assert response['msg'] == '请求参数异常'

    def test_14(self, addSale):
        """包装完整的值不存在"""
        response = tradeSale.editSale(id=addSale, packingIntactStandard='test')
        assert response['msg'] == '请求参数异常'

    def test_15(self):
        """售卖信息id不存在"""
        response = tradeSale.editSale(id=0, packingIntactStandard='test')
        assert response['msg'] == '请求参数异常'

    def test_16(self, addSale):
        """批次号为空"""
        response = tradeSale.editSale(id=addSale, lotNum=None)
        assert response['msg'] == '请输入批次/序列号'


class TestDelete:
    """删除售卖信息"""

    def test_01(self):
        """售卖信息id不存在"""
        response = tradeSale.deleteSale(id=0)
        assert response['msg'] == '售卖物资不存在'

    def test_02(self):
        """售卖信息id为空"""
        response = tradeSale.deleteSale(id=None)
        assert response['msg'] == '售卖商品id不能为空'

    # 调用作用范围为class的fixture-addPurchase
    def test_03(self, addSale):
        """重复删除"""
        # 第一次删除
        response = tradeSale.deleteSale(id=addSale)
        assert response['msg'] == '请求成功'
        # 第二次删除
        response2 = tradeSale.deleteSale(id=addSale)
        log.info(response2)
        assert response2['msg'] == '售卖物资不存在'


class TestList:
    """查询求购列表"""

    def test_01(self):
        """页码为空"""
        response = tradeSale.listSale(pageNum=None)
        assert response['msg'] == '请填写当前页码'

    def test_02(self):
        """分页大小为空"""
        response = tradeSale.listSale(pageSize=None)
        assert response['msg'] == '请填写分页大小'

    def test_03(self):
        """组合查询"""
        # 传参分类id和关键字查询
        response = tradeSale.listSale(categoryId=categoryId, keyword='test')
        assert response['msg'] == '请求成功'


class TestMyPurchaseList:
    """查询我的求购信息"""

    def test_01(self):
        """页码为空"""
        response = tradeSale.mySaleList(pageNum=None)
        assert response['msg'] == '请填写当前页码'

    def test_02(self):
        """分页大小为空"""
        response = tradeSale.mySaleList(pageSize=None)
        assert response['msg'] == '请填写分页大小'

    def test_03(self):
        """组合查询"""
        # 传参分类id和关键字查询
        response = tradeSale.mySaleList(categoryId=categoryId, keyword='test')
        assert response['msg'] == '请求成功'


class TestSold:
    """已经售卖"""

    def test_01(self):
        """售卖信息id不存在"""
        response = tradeSale.sold(id=None)
        assert response['msg'] == '售卖商品id不能为空'

    # 调用作用范围为class的fixture-addPurchase
    def test_02(self, addSale):
        """重复售卖"""
        # 第一次售卖
        response = tradeSale.sold(id=addSale)
        assert response['msg'] == '请求成功'
        # 第二次售卖
        response2 = tradeSale.sold(id=addSale)
        log.info(response2)
        assert response2['msg'] == '只可操作待交易的商品'

    # 调用作用范围为class的fixture, 供应商B新增一个求购信息，然后供应商A设为已售卖
    def test_03(self, addSale_02):
        """将其他供应商的售卖信息设置为已售卖"""
        response = tradeSale.sold(id=addSale_02)
        assert response['msg'] == '售卖信息不存在'
