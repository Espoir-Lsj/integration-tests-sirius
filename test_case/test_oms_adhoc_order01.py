# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

import pytest, datetime, time
from common import params, request, logger, accept
from faker import Faker
from common import adhocOrder
from test_config import param_config

log = logger.Log()


@pytest.mark.TestAccept
class TestAccept:
    goodsId = param_config.goodsId

    @pytest.fixture(scope="module")
    def create(self):
        # 创建订单
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, goodsQuantity=1)
        try:
            assert response['msg'] == '请求成功'
        except:
            raise Exception(response['msg'], response['exMsg'])
        # 临调单id
        adhocOrderId = response['data']['id']
        log.info('生成的临调单id: %s' % adhocOrderId)
        TestAccept.adhocOrderId = adhocOrderId

    def test_01(self, create):
        """拒绝临调单时没有传原因"""

        response2 = accept.reject(self.adhocOrderId, reason=None)
        assert response2['msg'] == '请填写拒绝原因'

    def test_02(self, create):
        """接收订单 商品信息 有误"""
        response = accept.success(self.adhocOrderId, goodsId=1, quantity=1)
        assert response['msg'] == '接收的商品明细和父临调单的明细不一致'

    def test_04(self, create):
        """接收临调单 ID为空"""
        response = accept.success(None, goodsId=self.goodsId, quantity=1)
        assert response['msg'] == '请选择临调单'

    def test_05(self, create):
        """接收临调单 ID错误"""
        response = accept.success(0, goodsId=self.goodsId, quantity=1)
        assert response['msg'] == '未查询到该临调订单，请刷新重试'

    def test_06(self, create):
        """发货方式为空"""
        response = accept.success(self.adhocOrderId, deliveryMode=None)
        assert response['msg'] == '请选择收货方式'

    def test_07(self, create):
        """发货方式错误"""
        response = accept.success(self.adhocOrderId, goodsId=self.goodsId, quantity=1, deliveryMode='a')
        assert response['msg'] == '请求参数异常'

    def test_08(self, create):
        """发货仓库为空"""
        response = accept.success(self.adhocOrderId, goodsId=self.goodsId, quantity=1, warehouseId=None)
        assert response['msg'] == '请选择临调单仓库'

    def test_09(self, create):
        """发货仓库错误"""
        response = accept.success(self.adhocOrderId, goodsId=self.goodsId, quantity=1, warehouseId=0)
        assert response['msg'] == '未找到来源仓库'

    def test_21(self):
        """接收含有工具包订单 工具包信息有误"""

        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, goodsQuantity=1, kitTemplateId=21)
        try:
            assert response['msg'] == '请求成功'
        except:
            raise Exception(response['msg'], response['exMsg'])
        id = response['data']['id']
        response2 = accept.success(id, goodsId=self.goodsId, quantity=1, kitTemplateId=33)
        assert response2['msg'] == '接收的工具包明细和父临调单的明细不一致'


@pytest.mark.TestAppCreate
class TestAppCreate:
    """小程序创建临调单"""
    url = '/adhocOrder/appCreate'
    # 物资id
    goodsId = param_config.goodsId
    # 100位的字符串
    context = str('1').zfill(100)

    @classmethod
    def setup_class(cls):
        log.info('-------测试创建临调单异常场景------')
        # 获取今天、明天、后天、昨天的时间戳
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        twoDaysAfter = today + datetime.timedelta(days=2)
        yesterday = today - datetime.timedelta(days=1)
        cls.today_stamp = int(time.mktime(today.timetuple())) * 1000
        cls.tomorrow_stamp = int(time.mktime(tomorrow.timetuple())) * 1000
        cls.twoDaysAfter_stamp = int(time.mktime(twoDaysAfter.timetuple())) * 1000
        cls.yesterday_stamp = int(time.mktime(yesterday.timetuple())) * 1000

    def test_01(self):
        """物资id不存在"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=0)
        assert response['msg'] == '商品不存在,请刷新重试'

    def test_02(self):
        """调拨数量为0"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, goodsQuantity=0)
        assert response['msg'] == '调拨数量不能小于1'

    def test_03(self):
        """调拨数量为空"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, goodsQuantity=None)
        assert response['msg'] == '请输入商品数量'

    # def test_04(self):
    #     """经销商id为空"""
    #     response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, supplierId=None)
    #     log.info(response)
    #     assert response['msg'] == '请输入经销商'
    #
    # def test_05(self):
    #     """经销商id不存在"""
    #     response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, supplierId=0)
    #     log.info(response)
    #     assert response['msg'] == '目标仓库不存在，请选择目标仓库'

    def test_11(self):
        """医院名称为空"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, hospitalName=None)
        assert response['msg'] == '请输入医院名称'

    def test_12(self):
        """医院名称超长"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, hospitalName=self.context)
        assert response['msg'] == '医院名称长度超出限制'

    def test_13(self):
        """患者年龄段为空"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, ageGroup=None)
        assert response['msg'] == '请选择患者年龄'

    def test_14(self):
        """患者年龄段传错误的值"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, ageGroup='test')
        assert response['msg'] == '请求参数异常'

    def test_21(self):
        """手术部位为空"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, siteId=None)
        assert response['msg'] == '请选择正确的手术部位'

    def test_22(self):
        """手术部位不存在"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, siteId='1')
        assert response['msg'] == '请选择正确的手术部位'

    def test_31(self):
        """主刀医生为空"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, surgeon=None)
        assert response['msg'] == '请输入正确的主刀医生姓名'

    def test_32(self):
        """手术日期为空"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, procedureTime=None)
        assert response['msg'] == '请选择手术日期'

    def test_33(self):
        """手术日期早于当天"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, procedureTime=self.yesterday_stamp)
        assert response['msg'] == '手术日期不能早于当天'

    def test_34(self):
        """预计归还日期为空"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, expectReturnTime=None)
        assert response['msg'] == '请选择归还日期'

    def test_35(self):
        """预计归还日期早于手术日期"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, expectReturnTime=self.yesterday_stamp)
        assert response['msg'] == '预计归还日期不能早于手术日期'

    def test_36(self):
        """订单联系人为空"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, contactName=None)
        assert response['msg'] == '请输入正确的联系人姓名'

    def test_37(self):
        """订单联系电话为空"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, contactPhone=None)
        assert response['msg'] == '请输入正确的手机号码'

    def test_38(self):
        """销售人员字段超长"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, salesPerson=self.context)
        assert response['msg'] == '销售人员长度超出限制'

    def test_41(self):
        """物流方式为空"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, deliveryMode=None)
        assert response['msg'] == '请选择收货方式'

    def test_42(self):
        """收件人为空"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, receivingName=None)
        assert response['msg'] == '请输入正确的收货人姓名'

    def test_43(self):
        """收件人电话为空"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, receivingPhone=None)
        assert response['msg'] == '请输入正确的手机号码'

    def test_44(self):
        """收件人地址为空"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, receivingAddress=None)
        assert response['msg'] == '请填写收货地址'

    def test_45(self):
        """收件人身份证错误"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId, receivingIdCard='null')
        assert response['msg'] == '请输入正确的身份证号'


class TestClose:
    """关闭订单"""
    url = '/adhocOrder/close'
    # 物资id
    goodsId = param_config.goodsId

    def test_01(self):
        """关闭不存在的订单"""
        response = request.put_body(self.url, body={'id': 0})
        assert response['msg'] == '未查询到该临调订单，请刷新重试'

    def test_02(self):
        """订单id为空"""
        response = request.put_body(self.url, body={'id': None})
        assert response['msg'] == '不能为null'

    def test_03(self):
        """订单id参数错误"""
        response = request.put_body(self.url, body={'id': '%%'})
        assert response['msg'] == '请求参数异常'


class TestCreate:
    """创建临调单"""
    url = '/adhocOrder/create'

    # 物资id
    goodsId = param_config.goodsId
    # 100位的字符串
    context = str('1').zfill(100)

    @classmethod
    def setup_class(cls):
        log.info('-------测试创建临调单异常场景------')
        # 获取今天、明天、后天、昨天的时间戳
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        twoDaysAfter = today + datetime.timedelta(days=2)
        yesterday = today - datetime.timedelta(days=1)
        cls.today_stamp = int(time.mktime(today.timetuple())) * 1000
        cls.tomorrow_stamp = int(time.mktime(tomorrow.timetuple())) * 1000
        cls.twoDaysAfter_stamp = int(time.mktime(twoDaysAfter.timetuple())) * 1000
        cls.yesterday_stamp = int(time.mktime(yesterday.timetuple())) * 1000

    def test_01(self):
        """物资id不存在"""
        response = adhocOrder.createAdhocOrder(goodsId=0)
        assert response['msg'] == '商品不存在,请刷新重试'

    def test_02(self):
        """调拨数量为0"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, goodsQuantity=0)
        assert response['msg'] == '调拨数量不能小于1'

    def test_03(self):
        """调拨数量为空"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, goodsQuantity=None)
        assert response['msg'] == '请输入商品数量'

    def test_04(self):
        """经销商id为空"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, supplierId=None)
        assert response['msg'] == '请输入经销商'

    def test_05(self):
        """经销商id不存在"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, supplierId=0)
        assert response['msg'] == '目标仓库不存在，请选择目标仓库'

    # 删除了物资库存校验
    # def test_06(self):
    #     """调拨数量大于库存数量"""
    #     response = adhocOrder.createTransferOrder(goodsId=self.goodsId, goodsQuantity=99999999)
    #     log.info(response)
    #     assert response['exMsg'] == '库存不足'

    def test_06(self):
        """医院名称为空"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, hospitalName=None)
        assert response['msg'] == '请输入医院名称'

    def test_07(self):
        """医院名称超长"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, hospitalName=self.context)
        assert response['msg'] == '医院名称长度超出限制'

    def test_08(self):
        """患者年龄段为空"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, ageGroup=None)
        assert response['msg'] == '请选择患者年龄'

    def test_09(self):
        """患者年龄段传错误的值"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, ageGroup='test')
        assert response['msg'] == '请求参数异常'

    def test_10(self):
        """手术部位为空"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, siteId=None)
        assert response['msg'] == '请选择正确的手术部位'

    def test_11(self):
        """手术部位不存在"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, siteId='1')
        assert response['msg'] == '请选择正确的手术部位'

    def test_12(self):
        """主刀医生为空"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, surgeon=None)
        assert response['msg'] == '请输入正确的主刀医生姓名'

    def test_13(self):
        """手术日期为空"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, procedureTime=None)
        assert response['msg'] == '请选择手术日期'

    def test_14(self):
        """手术日期早于当天"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, procedureTime=self.yesterday_stamp)
        assert response['msg'] == '手术日期不能早于当天'

    def test_15(self):
        """预计归还日期为空"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, expectReturnTime=None)
        assert response['msg'] == '请选择归还日期'

    def test_16(self):
        """预计归还日期早于手术日期"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, expectReturnTime=self.yesterday_stamp)
        assert response['msg'] == '预计归还日期不能早于手术日期'

    def test_17(self):
        """订单联系人为空"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, contactName=None)
        assert response['msg'] == '请输入正确的联系人姓名'

    def test_18(self):
        """订单联系电话为空"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, contactPhone=None)
        assert response['msg'] == '请输入正确的手机号码'

    def test_19(self):
        """销售人员字段超长"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, salesPerson=self.context)
        assert response['msg'] == '销售人员长度超出限制'

    def test_20(self):
        """物流方式为空"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, deliveryMode=None)
        assert response['msg'] == '请选择收货方式'

    def test_21(self):
        """收件人为空"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, receivingName=None)
        assert response['msg'] == '请输入正确的收货人姓名'

    def test_22(self):
        """收件人电话为空"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, receivingPhone=None)
        assert response['msg'] == '请输入正确的手机号码'

    def test_23(self):
        """收件人地址为空"""
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId, receivingAddress=None)
        assert response['msg'] == '请填写收货地址'

    # 删除了邮编的必填校验
    # def test_45(self):
    #     """收件人邮编为空"""
    #     response = adhocOrder.createTransferOrder(goodsId=self.goodsId, postcode=None)
    #     log.info(response)
    #     assert response['msg'] == '请填写邮编'


class TestAppEdit:
    """小程序编辑订单"""
    url = '/adhocOrder/appEdit'
    # 物资id
    goodsId = param_config.goodsId
    # 临调单id
    orderId = None

    @pytest.fixture(scope="module")
    def create(self):
        """创建临调单"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId)
        try:
            assert response['msg'] == '请求成功'
        except:
            raise Exception(response['msg'], response['exMsg'])
        # 临调单id
        TestAppEdit.orderId = response['data']['id']

        # 小程序编辑订单优先判断物资，所以暂时不需要把订单退回 编辑
        # yield
        # # 退回临调单
        # response2 = accept.reject(self.orderId, "小程序退回修改")
        # assert response2['msg'] == '请求成功'

    def test_01(self, create):
        """商品明细、工具包明细为空"""
        response = adhocOrder.app_edit_order(self.orderId, None, None)
        assert response['msg'] == '请选择物资'

    def test_02(self, create):
        """商品明细、工具包array的内容为空"""
        response = adhocOrder.app_edit_order(self.orderId, [None], [None])
        assert response['msg'] == '参数异常'

    def test_03(self, create):
        """修改商品数量为0"""
        goodsDetail = [{
            'goodsId': self.goodsId,
            'quantity': 0,
            'supplierId': 0
        }]
        response = adhocOrder.app_edit_order(self.orderId, goodsDetail, None)
        assert response['msg'] == '调拨数量不能小于1'

    def test_04(self, create):
        """订单状态不是待修改"""
        goodsDetail = [{
            'goodsId': self.goodsId,
            'quantity': 1,
            'supplierId': 0
        }]
        response = adhocOrder.app_edit_order(self.orderId, goodsDetail, None)
        assert response['msg'] == '只能修改待修改的订单'


class TestEdit:
    """web 编辑临调单"""
    goodsId = param_config.goodsId
    orderId = None
    context = str('1').zfill(100)

    def setup_class(cls):
        log.info('-------测试创建临调单异常场景------')
        # 获取今天、明天、后天、昨天的时间戳
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        twoDaysAfter = today + datetime.timedelta(days=2)
        yesterday = today - datetime.timedelta(days=1)
        cls.today_stamp = int(time.mktime(today.timetuple())) * 1000
        cls.tomorrow_stamp = int(time.mktime(tomorrow.timetuple())) * 1000
        cls.twoDaysAfter_stamp = int(time.mktime(twoDaysAfter.timetuple())) * 1000
        cls.yesterday_stamp = int(time.mktime(yesterday.timetuple())) * 1000

    @pytest.fixture(scope="module")
    def create(self):
        response = adhocOrder.createAdhocOrder(goodsId=self.goodsId)
        try:
            assert response['msg'] == '请求成功'
        except:
            raise Exception(response['msg'], response['exMsg'])
        TestEdit.orderId = response['data']['id']
        # yield
        #
        # response2 = accept.reject(self.orderId, "web退回编辑")

    def test_01(self, create):
        """商品ID为空"""
        response = adhocOrder.edit_order(self.orderId, goodsId=None)
        assert response['msg'] == '商品不存在,请刷新重试'

    def test_02(self, create):
        """商品ID错误"""
        response = adhocOrder.edit_order(self.orderId, goodsId=0)
        assert response['msg'] == '商品不存在,请刷新重试'

    def test_03(self, create):
        """调拨数量为0"""
        response = adhocOrder.edit_order(self.orderId, goodsQuantity=0)
        assert response['msg'] == '调拨数量不能小于1'

    def test_04(self, create):
        """调拨数量为空"""
        response = adhocOrder.edit_order(self.orderId, goodsQuantity=None)
        assert response['msg'] == '请输入商品数量'

    def test_05(self, create):
        """经销商id为空"""
        response = adhocOrder.edit_order(self.orderId, supplierId=None)
        assert response['msg'] == '请输入经销商'

    def test_06(self, create):
        """经销商id不存在"""
        response = adhocOrder.edit_order(self.orderId, supplierId=0)
        assert response['msg'] == '目标仓库不存在，请选择目标仓库'

    # 删除了物资库存校验
    # def test_06(self, create):
    #     """调拨数量大于库存数量"""
    #     response = adhocOrder.edit_order(gself.orderId, goodsQuantity=99999999)
    #     log.info(response)
    #     assert response['exMsg'] == '库存不足'

    def test_07(self, create):
        """医院名称为空"""
        response = adhocOrder.edit_order(self.orderId, hospitalName=None)
        assert response['msg'] == '请输入医院名称'

    def test_08(self, create):
        """医院名称超长"""
        response = adhocOrder.edit_order(self.orderId, hospitalName=self.context)
        assert response['msg'] == '医院名称长度超出限制'

    def test_09(self, create):
        """患者年龄段为空"""
        response = adhocOrder.edit_order(self.orderId, ageGroup=None)
        assert response['msg'] == '请选择患者年龄'

    def test_10(self, create):
        """患者年龄段传错误的值"""
        response = adhocOrder.edit_order(self.orderId, ageGroup='test')
        assert response['msg'] == '请求参数异常'

    def test_11(self, create):
        """手术部位为空"""
        response = adhocOrder.edit_order(self.orderId, siteId=None)
        assert response['msg'] == '请选择正确的手术部位'

    def test_12(self, create):
        """手术部位不存在"""
        response = adhocOrder.edit_order(self.orderId, siteId='1')
        assert response['msg'] == '请选择正确的手术部位'

    def test_13(self, create):
        """主刀医生为空"""
        response = adhocOrder.edit_order(self.orderId, surgeon=None)
        assert response['msg'] == '请输入正确的主刀医生姓名'

    def test_14(self, create):
        """手术日期为空"""
        response = adhocOrder.edit_order(self.orderId, procedureTime=None)
        assert response['msg'] == '请选择手术日期'

    def test_15(self, create):
        """手术日期早于当天"""
        response = adhocOrder.edit_order(self.orderId, procedureTime=self.yesterday_stamp)
        assert response['msg'] == '手术日期不能早于当天'

    def test_16(self, create):
        """预计归还日期为空"""
        response = adhocOrder.edit_order(self.orderId, expectReturnTime=None)
        assert response['msg'] == '请选择归还日期'

    def test_17(self, create):
        """预计归还日期早于手术日期"""
        response = adhocOrder.edit_order(self.orderId, expectReturnTime=self.yesterday_stamp)
        assert response['msg'] == '预计归还日期不能早于手术日期'

    def test_18(self, create):
        """订单联系人为空"""
        response = adhocOrder.edit_order(self.orderId, contactName=None)
        assert response['msg'] == '请输入正确的联系人姓名'

    def test_19(self, create):
        """订单联系电话为空"""
        response = adhocOrder.edit_order(self.orderId, contactPhone=None)
        assert response['msg'] == '请输入正确的手机号码'

    # def test_19_1(self, create):
    #     """订单联系电话过长"""
    #     response = adhocOrder.edit_order(self.orderId, contactPhone=135123456789)
    #     assert response['msg'] == '请输入正确的手机号码'

    def test_20(self, create):
        """销售人员字段超长"""
        response = adhocOrder.edit_order(self.orderId, salesPerson=self.context)
        assert response['msg'] == '销售人员长度超出限制'

    def test_21(self, create):
        """物流方式为空"""
        response = adhocOrder.edit_order(self.orderId, deliveryMode=None)
        assert response['msg'] == '请选择收货方式'

    def test_22(self, create):
        """收件人为空"""
        response = adhocOrder.edit_order(self.orderId, receivingName=None)
        assert response['msg'] == '请输入正确的收货人姓名'

    def test_23(self, create):
        """收件人电话为空"""
        response = adhocOrder.edit_order(self.orderId, receivingPhone=None)
        assert response['msg'] == '请输入正确的手机号码'

    def test_24(self, create):
        """收件人地址为空"""
        response = adhocOrder.edit_order(self.orderId, receivingAddress=None)
        assert response['msg'] == '请填写收货地址'


class TestFindList:
    """查询临调单列表"""
    url = '/adhocOrder/findList'

    # 列举需要测试的查询条件和值，组合查询
    # 状态（每个状态都需要查询一次，组合状态查询一次）
    statusList = ['accept_pending', 'delivery_pending', 'delivering', 'backing', 'generate_sales_order_pending',
                  'adjusting', 'finished', 'closed', 'accept_pending,delivery_pending']
    # 关键字
    keyword = ['123', '%%%', 'TEST']
    # 物流方式
    deliveryMode = ['SELF_PIKE_UP', 'DELIVERY']

    @pytest.mark.parametrize('statusList', statusList)
    @pytest.mark.parametrize('keyword', keyword)
    @pytest.mark.parametrize('deliveryMode', deliveryMode)
    def test_01(self, statusList, keyword, deliveryMode):
        """组合查询"""
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'status': statusList,
            'keyword': keyword,
            'deliveryMode': deliveryMode
        }
        r = request.get_params(self.url, params=params)
        assert r['msg'] == '请求成功'


class TestGetAddress:
    """查询订单地址"""
    url = '/adhocOrder/getAddress'

    def test_01(self):
        """临调单id不存在"""
        response = request.get_params(self.url, params={'id': 0})
        assert response['msg'] == '临调订单不存在'

    def test_02(self):
        """临调单id参数值错误"""
        response = request.get_params(self.url, params={'id': '%%'})
        assert 'System busy' not in response['msg']

    def test_03(self):
        """临调单id为空"""
        response = request.get_params(self.url, params={'id': None})
        assert 'System busy' not in response['msg']


class TestGetDetail:
    """查询临调单明细"""
    url = '/adhocOrder/getDetail'
    # 物资id
    goodsId = param_config.goodsId
    kitTemplateId = param_config.kitTemplateId
    # 临调单id
    orderId = None

    @pytest.fixture(scope="module")
    def create(self):
        """创建临调单"""
        response = adhocOrder.appCreateAdhocOrder(goodsId=self.goodsId)
        try:
            assert response['msg'] == '请求成功'
        except:
            raise Exception(response['msg'], response['exMsg'])
        # 临调单id
        TestGetDetail.orderId = response['data']['id']

        yield
        # 关闭临调单
        response2 = request.put_body('/adhocOrder/close', body={'id': TestGetDetail.orderId})
        assert response2['msg'] == '请求成功'

    def test_01(self):
        """临调单id不存在"""
        response = request.get_params(self.url, params={'orderId': 0})
        assert response['msg'] == '未查询到该临调订单，请刷新重试'

    def test_02(self):
        """临调单id参数值错误"""
        response = request.get_params(self.url, params={'orderId': '%%'})
        assert response['msg'] == '请求参数异常'

    def test_03(self):
        """临调单id为空"""
        response = request.get_params(self.url, params={'orderId': None})
        assert response['msg'] == '请求参数异常'

    def test_04(self, create):
        """临调单id正确"""
        response = request.get_params(self.url, params={'orderId': self.orderId})
        assert response['msg'] == '请求成功'


class TestGetDetailByOrderId:
    """查询订单详情"""
    url = '/adhocOrder/getDetailByOrderId'

    def test_01(self):
        """临调单id不存在"""
        response = request.get_params(self.url, params={'orderId': 0})
        assert response['msg'] == '未查询到该临调订单，请刷新重试'

    def test_02(self):
        """临调单id参数值错误"""
        response = request.get_params(self.url, params={'orderId': '%%'})
        assert response['msg'] == '请求参数异常'

    def test_03(self):
        """临调单id为空"""
        response = request.get_params(self.url, params={'orderId': None})
        assert response['msg'] == '请求参数异常'


class TestUpdateAddress:
    """修改订单地址"""
    url = '/adhocOrder/updateAddress'

    # 物资id
    goodsId = param_config.goodsId
    # 100位的字符串
    context = str('1').zfill(100)

    @classmethod
    def setup_class(cls):
        """创建并接收一个临调单"""
        create = adhocOrder.createAdhocOrder(goodsId=cls.goodsId)
        try:
            assert create['msg'] == '请求成功'
        except:
            raise Exception(create['msg'], create['exMsg'])
        # 获取临调单id
        adhocOrderId = create['data']['id']
        log.info('生成的临调单id: %s' % adhocOrderId)
        # 接收临调单
        accept = request.put_body('/adhocOrder/accept', body={'id': adhocOrderId, 'accept': True})
        try:
            assert accept['msg'] == '请求成功'
        except:
            raise Exception(accept['msg'], accept['exMsg'])
        # 保存临调单id
        cls.adhocOrderId = adhocOrderId

    def test_01(self):
        """临调单id不存在"""
        response = adhocOrder.updateAddress(orderId=0)
        assert response['msg'] == '未查询到该临调订单，请刷新重试'

    def test_02(self):
        """临调单id为空"""
        response = adhocOrder.updateAddress(orderId=None)
        assert response['msg'] == '不能为null'

    def test_03(self):
        """临调单id错误"""
        response = adhocOrder.updateAddress(orderId='%%')
        assert response['msg'] == '请求参数异常'

    def test_04(self):
        """收件人为空"""
        response = adhocOrder.updateAddress(orderId=self.adhocOrderId, receivingName=None)
        assert response['msg'] == '请输入正确的收件人'

    def test_05(self):
        """联系电话为空"""
        response = adhocOrder.updateAddress(orderId=self.adhocOrderId, receivingPhone=None)
        assert response['msg'] == '请输入正确的手机号码'

    def test_06(self):
        """收件地址为空"""
        response = adhocOrder.updateAddress(orderId=self.adhocOrderId, receivingAddress=None)
        assert response['msg'] == '请输入收货地址'

    def test_11(self):
        """物流方式为自提时，提货人为空"""
        response = adhocOrder.updateAddress(orderId=self.adhocOrderId, deliveryMode='SELF_PIKE_UP', consignorName=None)
        assert response['msg'] == '请输入提货人'

    def test_12(self):
        """物流方式为自提时，提货人电话为空"""
        response = adhocOrder.updateAddress(orderId=self.adhocOrderId, deliveryMode='SELF_PIKE_UP', consignorPhone=None)
        assert response['msg'] == '请输入提货人电话'

    def test_13(self):
        """物流方式为自提时，提货人身份证为空"""
        response = adhocOrder.updateAddress(orderId=self.adhocOrderId, deliveryMode='SELF_PIKE_UP',
                                            receivingIdCard=None)
        assert response['msg'] == '请输入身份证号码'

    def test_14(self):
        """物流方式为自提时，委托书为空"""
        response = adhocOrder.updateAddress(orderId=self.adhocOrderId, deliveryMode='SELF_PIKE_UP', file=None)
        assert response['msg'] == '请上传提货委托书'

    def test_15(self):
        """物流方式为快递时，收件地址为空"""
        response = adhocOrder.updateAddress(orderId=self.adhocOrderId, deliveryMode='DELIVERY', receivingAddress=None)
        assert response['msg'] == '请输入收货地址'

    def test_16(self):
        """不修改任何信息"""
        response = adhocOrder.updateAddress(orderId=self.adhocOrderId)
        assert response['msg'] == '请求成功'


if __name__ == '__main__':
    pytest.main(['-v', '-s'])
