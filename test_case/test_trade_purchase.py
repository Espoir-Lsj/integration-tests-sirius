# __author:"zonglr"
# date:2020/12/11
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, datetime, time, jsonpath, random
from common import supplier_request, tradePurchase, logger

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
categoryId = ids[random.randint(0, len(ids))]


# 新增一个供应商A的求购信息，fixture生效范围为每个class仅执行一次
@pytest.fixture(scope="class")
def addPurchase():
    response = tradePurchase.addPurchase()
    assert response['msg'] == '请求成功'
    # 获取求购信息的id,并返回
    id = response['data']
    return id


# 新增一个供应商B的求购信息，fixture生效范围为每个class仅执行一次
@pytest.fixture(scope="class")
def addPurchase_02():
    response = tradePurchase.addPurchase_02()
    assert response['msg'] == '请求成功'
    # 获取求购信息的id,并返回
    id = response['data']
    return id


class TestAdd:
    """新增求购信息"""
    context = str('1').zfill(200)

    def test_01(self):
        """商品名称为空"""
        response = tradePurchase.addPurchase(goodsName=None)
        assert response['msg'] == '请输入物资名称'

    def test_01_1(self):
        """商品名称超长"""
        response = tradePurchase.addPurchase(goodsName=self.context)
        assert response['msg'] == '物资名称长度超出限制'

    def test_02(self):
        """规格型号为空"""
        response = tradePurchase.addPurchase(specification=None)
        assert response['msg'] == '请输入规格/型号'

    def test_02_1(self):
        """规格超长"""
        response = tradePurchase.addPurchase(specification=self.context)
        assert response['msg'] == '规格长度超出限制'

    def test_02_2(self):
        """型号超长"""
        response = tradePurchase.addPurchase(specification=None, model=self.context)
        assert response['msg'] == '型号长度超出限制'

    def test_03(self):
        """求购数量为空"""
        response = tradePurchase.addPurchase(quantity=None)
        assert response['msg'] == '请输入物资数量'

    def test_03_1(self):
        """求购数量超出3位数字"""
        response = tradePurchase.addPurchase(quantity=1000)
        assert response['msg'] == '最大不能超过999'

    def test_03_2(self):
        """求购数量非数字"""
        response = tradePurchase.addPurchase(quantity='%%')
        assert response['msg'] == '请求参数异常'

    def test_03_3(self):
        """求购数量为0"""
        response = tradePurchase.addPurchase(quantity=0)
        assert response['msg'] == '最小不能小于1'

    def test_04(self):
        """单价为空"""
        response = tradePurchase.addPurchase(price=None)
        assert response['msg'] == '请输入售价'

    def test_04_1(self):
        """单价超长"""
        response = tradePurchase.addPurchase(price=10000000000000000000.11)
        assert response['msg'] == '请求参数异常'

    def test_05(self):
        """求购公司为空"""
        response = tradePurchase.addPurchase(supplierName=None)
        assert response['msg'] == '请输入求购公司'

    def test_05_1(self):
        """求购公司超长"""
        response = tradePurchase.addPurchase(supplierName=self.context)
        assert response['msg'] == '求购公司长度超出限制'

    def test_05_2(self):
        """求购公司不存在"""
        response = tradePurchase.addPurchase(supplierName=0)
        assert response['msg'] == '所属公司不属于当前用户，请刷新重试'

    def test_06(self):
        """联系人为空"""
        response = tradePurchase.addPurchase(contact=None)
        assert response['msg'] == '请输入联系人'

    def test_06_1(self):
        """联系人字段超长"""
        response = tradePurchase.addPurchase(contact=self.context)
        assert response['msg'] == '联系人长度超出限制'

    def test_07(self):
        """联系电话为空"""
        response = tradePurchase.addPurchase(contactPhone=None)
        assert response['msg'] == '请输入正确的手机号码'

    def test_07_1(self):
        """联系电话非数字"""
        response = tradePurchase.addPurchase(contactPhone='%%%%')
        assert response['msg'] == '请输入正确的手机号码'

    def test_08(self):
        """收货地址为空"""
        response = tradePurchase.addPurchase(receiverArea=None)
        assert response['msg'] == '请选择收货地'

    def test_08_1(self):
        """收货地址值错误"""
        response = tradePurchase.addPurchase(receiverArea='test')
        assert response['msg'] == '请求参数异常'

    def test_09(self):
        """不存在的耗材类型"""
        response = tradePurchase.addPurchase(category=0)
        assert response['msg'] == '该类型不存在'

    def test_10(self):
        """需求关闭日期等于当天"""
        response = tradePurchase.addPurchase(closingDate=today_stamp)
        assert response['msg'] == '关闭日期不能早于或等于当天'


class TestCancel:
    """取消求购信息"""

    def test_01(self):
        """信息id不存在"""
        response = tradePurchase.cancelPurchase(id=0)
        assert response['msg'] == '求购物资不存在'

    def test_02(self):
        """信息id为空值"""
        response = tradePurchase.cancelPurchase(id=None)
        assert response['msg'] == '求购商品id不能为空'

    # 调用作用范围为class的fixture-addPurchase
    def test_03(self, addPurchase):
        """重复取消"""
        # 第一次取消
        response = tradePurchase.cancelPurchase(id=addPurchase)
        assert response['msg'] == '请求成功'
        # 第二次取消
        response2 = tradePurchase.cancelPurchase(id=addPurchase)
        log.info(response2)
        assert response2['msg'] == '非待交易状态下不能取消'

    # 调用作用范围为class的fixture, 供应商B新增一个求购信息，然后供应商A取消
    def test_04(self, addPurchase_02):
        """取消其他供应商的求购信息"""
        response = tradePurchase.cancelPurchase(id=addPurchase_02)
        assert response['msg'] == '求购信息不存在'


class TestDelete:
    """删除求购信息"""

    def test_01(self):
        """信息id不存在"""
        response = tradePurchase.deletePurchase(id=0)
        assert response['msg'] == '求购物资不存在'

    def test_02(self):
        """信息id为空"""
        response = tradePurchase.deletePurchase(id=None)
        assert response['msg'] == '求购商品id不能为空'

    # 先调用作用范围为class的fixture-addPurchase
    def test_03(self, addPurchase):
        """重复删除"""
        # 第一次删除
        response = tradePurchase.deletePurchase(id=addPurchase)
        assert response['msg'] == '请求成功'
        # 第二次删除
        response2 = tradePurchase.deletePurchase(id=addPurchase)
        log.info(response2)
        assert response2['msg'] == '求购物资不存在'

    # 调用作用范围为class的fixture, 供应商B新增一个求购信息，然后供应商A删除
    def test_04(self, addPurchase_02):
        """删除其他供应商的求购信息"""
        response = tradePurchase.deletePurchase(id=addPurchase_02)
        assert response['msg'] == '求购信息不存在'


class TestDetail:
    """求购信息详情"""

    def test_01(self):
        """查询不存在的求购信息"""
        response = tradePurchase.detail(0)
        assert response['msg'] == '求购物资不存在'


class TestEdit:
    """编辑求购信息"""
    context = str('1').zfill(200)

    def test_01(self):
        """求购信息id不存在"""
        response = tradePurchase.editPurchase(id=0)
        assert response['msg'] == '求购物资不存在'

    def test_02(self):
        """求购信息id为空值"""
        response = tradePurchase.editPurchase(id=None)
        assert response['msg'] == '求购id不能为空'

    def test_03(self, addPurchase):
        """物资名称为空"""
        response = tradePurchase.editPurchase(id=addPurchase, goodsName=None)
        assert response['msg'] == '请输入物资名称'

    def test_03_1(self, addPurchase):
        """商品名称超长"""
        response = tradePurchase.editPurchase(id=addPurchase, goodsName=self.context)
        assert response['msg'] == '物资名称长度超出限制'

    def test_04(self, addPurchase):
        """规格型号为空"""
        response = tradePurchase.editPurchase(id=addPurchase, specification=None)
        assert response['msg'] == '请输入规格/型号'

    def test_04_1(self, addPurchase):
        """规格超长"""
        response = tradePurchase.editPurchase(id=addPurchase, specification=self.context)
        assert response['msg'] == '规格长度超出限制'

    def test_04_2(self, addPurchase):
        """型号超长"""
        response = tradePurchase.editPurchase(id=addPurchase, specification=None, model=self.context)
        assert response['msg'] == '型号长度超出限制'

    def test_05(self, addPurchase):
        """求购数量为空"""
        response = tradePurchase.editPurchase(id=addPurchase, quantity=None)
        assert response['msg'] == '请输入物资数量'

    def test_05_1(self, addPurchase):
        """求购数量超出3位数字"""
        response = tradePurchase.editPurchase(id=addPurchase, quantity=1000)
        assert response['msg'] == '最大不能超过999'

    def test_05_2(self, addPurchase):
        """求购数量非数字"""
        response = tradePurchase.editPurchase(id=addPurchase, quantity='%%')
        assert response['msg'] == '请求参数异常'

    def test_05_3(self, addPurchase):
        """求购数量为0"""
        response = tradePurchase.editPurchase(id=addPurchase, quantity=0)
        assert response['msg'] == '最小不能小于1'

    def test_06(self, addPurchase):
        """单价为空"""
        response = tradePurchase.editPurchase(id=addPurchase, price=None)
        assert response['msg'] == '请输入售价'

    def test_06_1(self, addPurchase):
        """单价超长"""
        response = tradePurchase.editPurchase(id=addPurchase, price=10000000000000000000.11)
        assert response['msg'] == '请求参数异常'

    def test_07(self, addPurchase):
        """求购公司为空"""
        response = tradePurchase.editPurchase(id=addPurchase, supplierName=None)
        assert response['msg'] == '请输入求购公司'

    def test_07_1(self, addPurchase):
        """求购公司超长"""
        response = tradePurchase.editPurchase(id=addPurchase, supplierName=self.context)
        assert response['msg'] == '求购公司长度超出限制'

    def test_07_2(self, addPurchase):
        """求购公司不存在"""
        response = tradePurchase.editPurchase(id=addPurchase, supplierName=0)
        assert response['msg'] == '所属公司不属于当前用户，请刷新重试'

    def test_08(self, addPurchase):
        """联系人为空"""
        response = tradePurchase.editPurchase(id=addPurchase, contact=None)
        assert response['msg'] == '请输入联系人'

    def test_08_1(self, addPurchase):
        """联系人字段超长"""
        response = tradePurchase.editPurchase(id=addPurchase, contact=self.context)
        assert response['msg'] == '联系人长度超出限制'

    def test_09(self, addPurchase):
        """联系电话为空"""
        response = tradePurchase.editPurchase(id=addPurchase, contactPhone=None)
        assert response['msg'] == '请输入正确的手机号码'

    def test_09_1(self, addPurchase):
        """联系电话非数字"""
        response = tradePurchase.editPurchase(id=addPurchase, contactPhone='%%%%')
        assert response['msg'] == '请输入正确的手机号码'

    def test_10(self, addPurchase):
        """收货地址为空"""
        response = tradePurchase.editPurchase(id=addPurchase, receiverArea=None)
        assert response['msg'] == '请选择收货地'

    def test_10_1(self, addPurchase):
        """收货地址值错误"""
        response = tradePurchase.editPurchase(id=addPurchase, receiverArea='test')
        assert response['msg'] == '请求参数异常'

    def test_11(self, addPurchase):
        """不存在的耗材类型"""
        response = tradePurchase.editPurchase(id=addPurchase, category=0)
        assert response['msg'] == '该类型不存在'

    def test_12(self, addPurchase):
        """需求关闭日期等于当天"""
        response = tradePurchase.editPurchase(id=addPurchase, closingDate=today_stamp)
        assert response['msg'] == '关闭日期不能早于或等于当天'

    def test_13(self, addPurchase_02):
        """修改其他供应商的求购信息"""
        response = tradePurchase.editPurchase(id=addPurchase_02, closingDate=today_stamp)
        assert response['msg'] == '求购信息不存在'


class TestList:
    """查询求购列表"""

    def test_01(self):
        """页码为空"""
        response = tradePurchase.listPurchase(pageNum=None)
        assert response['msg'] == '请填写当前页码'

    def test_02(self):
        """分页大小为空"""
        response = tradePurchase.listPurchase(pageSize=None)
        assert response['msg'] == '请填写分页大小'

    def test_03(self):
        """组合查询"""
        # 传参分类id和关键字查询
        response = tradePurchase.listPurchase(categoryId=categoryId, keyword='test')
        assert response['msg'] == '请求成功'


class TestMyPurchaseList:
    """查询我的求购信息"""

    def test_01(self):
        """页码为空"""
        response = tradePurchase.myPurchaseList(pageNum=None)
        assert response['msg'] == '请填写当前页码'

    def test_02(self):
        """分页大小为空"""
        response = tradePurchase.myPurchaseList(pageSize=None)
        assert response['msg'] == '请填写分页大小'

    def test_03(self):
        """组合查询"""
        # 传参分类id和关键字查询
        response = tradePurchase.listPurchase(categoryId=categoryId, keyword='test')
        assert response['msg'] == '请求成功'
