# __author:"zonglr"
# date:2020/12/9
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, datetime, time
from common import params, request, logger, accept
from faker import Faker
from common import adhocOrder, outboundOrder, pick
from test_config import param_config

log = logger.Log()

today = datetime.date.today()
today_stamp = int(time.mktime(today.timetuple())) * 1000


# 创建一个待审核的快递出库单
@pytest.fixture(scope="module")
def createOutboundOrder():
    # 创建临调单
    response = adhocOrder.appCreateAdhocOrder(param_config.goodsId)
    # assert response['msg'] == '请求成功'
    try:
        assert response['msg'] == '请求成功'
    except:
        raise Exception(response['msg'], response['exMsg'])
    # 保存临调单id，code
    adhocOrderId = response['data']['id']
    log.info('生成的临调单id: %s' % adhocOrderId)
    adhocOrderCode = response['data']['code']
    log.info('生成的临调单code: %s' % adhocOrderCode)
    # 接收临调单
    response1 = accept.check(adhocOrderId)
    try:
        assert response1['msg'] == '请求成功'
    except:
        raise Exception(response1['msg'], response1['exMsg'])
    log.info('临调单接收成功 %s' % response1)
    # 根据临调单code查询拣货单id
    getList = request.get(
        '/allocateOutboundOrder/list?pageNum=0&pageSize=20&keyword=%s' % adhocOrderCode)
    assert getList['msg'] == '请求成功'
    # 保存拣货单id
    pickOrderId = getList['data']['rows'][0]['pickOrderId']
    log.info('生成的拣货单id: %s' % pickOrderId)
    # 拣货
    pick_response = pick.finishPick(pickOrderId)
    assert pick_response['msg'] == '请求成功'
    # 根据keyword查询列表详情
    getList = request.get(
        '/allocateOutboundOrder/list?pageNum=0&pageSize=50&status=delivery_pending&status=pick_pending&keyword=%s' % adhocOrderCode)
    # 出库单id
    outboundOrderId = getList['data']['rows'][0]['id']
    # # 提货方式
    # deliveryMode = getList['data']['rows'][0]['deliveryMode']
    return outboundOrderId


# 发货
def delivery(id, logisticsCompany='京东', expressNo='JD881991899', deliveryDate=today_stamp, deliveryMode='SELF_PIKE_UP'):
    body = {
        'logisticsCompany': logisticsCompany,
        'expressNo': expressNo,
        'deliveryDate': deliveryDate,
        'id': id,
        'deliveryMode': deliveryMode
    }
    response = request.put_body('/allocateOutboundOrder/delivery', body=body)
    return response


# 发货审核
def approval(id, logisticsCompany='京东', expressNo='JD881991899', deliveryDate=today_stamp):
    body = {
        'logisticsCompany': logisticsCompany,
        'expressNo': expressNo,
        'deliveryDate': deliveryDate,
        'id': id,
    }
    response = request.put_body('/allocateOutboundOrder/approval', body=body)
    return response


class TestDeliveryAndApproval:
    """设置调拨出库单已发货"""
    url = '/allocateOutboundOrder/delivery'
    approval_url = '/allocateOutboundOrder/approval'

    # 发货成功，class内仅执行一次
    @pytest.fixture(scope="class")
    def setDelivery(self, createOutboundOrder):
        # 发货方式设置为快递
        response = delivery(id=createOutboundOrder, deliveryMode='DELIVERY')
        return response

    def test_01(self, createOutboundOrder):
        """收货地址未填写"""
        response = delivery(id=createOutboundOrder)
        assert response['msg'] == '收货信息不完整,请联系客服/商务,补全收货信息'

    def test_02(self):
        """出库单id不存在"""
        response = delivery(id=0)
        assert response['msg'] == '调拨出库单不存在'

    def test_03(self):
        """审核不存在的出库单"""
        response = approval(id=0)
        assert response['msg'] == '调拨出库单不存在'

    def test_04(self, createOutboundOrder):
        """审核未发货的出库单"""
        response = approval(id=createOutboundOrder)
        assert response['msg'] == '该订单状态不正确'

    def test_05(self, createOutboundOrder, setDelivery):
        """审核时日期为空"""
        response = approval(id=createOutboundOrder, deliveryDate=None)
        assert response['msg'] == '请输入发货日期'


class TestDeliveryInfo:
    """调拨出库单发货信息"""
    url = '/allocateOutboundOrder/deliveryInfo/{orderId}'

    def test_01(self):
        """调拨出库单id不存在"""
        response = request.get(self.url.format(orderId=0))
        assert response['msg'] == '调拨出库单不存在'

    def test_02(self, createOutboundOrder):
        """正确的调拨出库单id"""
        response = request.get(self.url.format(orderId=createOutboundOrder))
        assert response['msg'] == '请求成功'


class TestDetail:
    """调拨出库单明细"""
    url = '/allocateOutboundOrder/detail/{orderId}'

    def test_01(self):
        """出库单id不存在"""
        response = request.get(self.url.format(orderId=0))
        assert response['msg'] == '调拨出库单不存在'

    def test_02(self, createOutboundOrder):
        """正确的出库单id"""
        response = request.get(self.url.format(orderId=createOutboundOrder))
        assert response['msg'] == '请求成功'


class TestGetAddress:
    """查询调拨出库单收货信息"""
    url = '/allocateOutboundOrder/getAddress'

    def test_01(self):
        """出库单id不存在"""
        params = {
            'outboundOrderId': 0
        }
        response = request.get_params(self.url, params=params)
        assert response['msg'] == '调拨出库单不存在'

    def test_02(self, createOutboundOrder):
        """正确的出库单id"""
        params = {
            'outboundOrderId': createOutboundOrder
        }
        response = request.get_params(self.url, params=params)
        assert response['msg'] == '请求成功'


class TestList:
    """调拨单出库单列表"""
    url = '/allocateOutboundOrder/list'

    # 列举需要测试的查询条件和值，组合查询
    # 状态（每个状态都需要查询一次，组合状态查询一次）
    statusList = ['pick_pending', 'delivery_pending', 'approval_pending', 'finish']
    # 关键字
    keyword = ['123', '%%%', 'TEST']

    @pytest.mark.parametrize('statusList', statusList)
    @pytest.mark.parametrize('keyword', keyword)
    def test_01(self, statusList, keyword):
        """组合查询"""
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'status': statusList,
            'keyword': keyword
        }
        r = request.get_params(self.url, params=params)
        assert r['msg'] == '请求成功'


class TestPrint:
    """调拨出库单打印"""
    url = '/allocateOutboundOrder/print/{orderId}'

    def test_01(self):
        """出库单id不存在"""
        response = request.get(self.url.format(orderId=0))
        assert response['msg'] == '调拨出库单不存在'

    def test_02(self, createOutboundOrder):
        """正确的出库单id"""
        response = request.get(self.url.format(orderId=createOutboundOrder))
        assert response['msg'] == '请求成功'
