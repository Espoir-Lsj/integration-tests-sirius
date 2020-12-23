# __author:"zonglr"
# date:2020/12/9
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, datetime, time
from common import params, request, logger
from faker import Faker
from common import adhocOrder, outboundOrder, pick
from test_config import param_config

log = logger.Log()

today = datetime.date.today()
today_stamp = int(time.mktime(today.timetuple())) * 1000


# 创建一个待审核的快递出库单
@pytest.fixture(scope="module")
def prepare():
    # 创建临调单
    response = adhocOrder.appCreateAdhocOrder(param_config.goodsId)
    assert response['msg'] == '请求成功'
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
    body = {
        'id': adhocOrderId,
        'accept': True
    }
    accept = request.put_body('/adhocOrder/accept', body=body)
    try:
        assert accept['msg'] == '请求成功'
    except:
        raise Exception(accept['msg'], accept['exMsg'])
    log.info('临调单接收成功 %s' % accept)
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
    # 提货方式
    deliveryMode = getList['data']['rows'][0]['deliveryMode']
    return outboundOrderId, deliveryMode


class TestOutbound:
    """设置调拨出库单已发货"""
    url = '/allocateOutboundOrder/delivery'
    approval_url = '/allocateOutboundOrder/approval'

    def test_01(self, prepare):
        """收货地址未填写"""
        body = {
            'logisticsCompany': '京东',
            'expressNo': 'JD881991899',
            'deliveryDate': today_stamp,
            'id': prepare[0],
            'deliveryMode': 'SELF_PIKE_UP'
        }
        response = request.put_body(self.url, body=body)
        log.info(response)
        assert response['msg'] == '收货信息不完整,请联系客服/商务,补全收货信息'
        # 设置出库单为已发货
        body['deliveryMode'] = 'DELIVERY'
        response2 = request.put_body(self.url, body=body)
        log.info(response2)
        assert response2['msg'] == '请求成功'

    def test_02(self):
        """出库单id不存在"""
        body = {
            'logisticsCompany': '京东',
            'expressNo': 'JD881991899',
            'deliveryDate': today_stamp,
            'id': 0,
            'deliveryMode': 'SELF_PIKE_UP'
        }
        response = request.put_body(self.url, body=body)
        log.info(response)
        assert response['msg'] == '调拨出库单不存在'

    def test_03(self):
        """审核不存在的出库单"""
        body = {
            'logisticsCompany': '京东',
            'expressNo': 'JD881991899',
            'deliveryDate': today_stamp,
            'id': 0,
        }
        response = request.put_body(self.approval_url, body=body)
        log.info(response)
        assert response['msg'] == '调拨出库单不存在'

    def test_03_1(self, prepare):
        """审核出库单发货日期为空"""
        body = {
            'logisticsCompany': '京东',
            'expressNo': 'JD881991899',
            'deliveryDate': None,
            'id': prepare[0],
        }
        response = request.put_body(self.approval_url, body=body)
        log.info(response)
        assert response['msg'] == '请输入发货日期'

    def test_04(self, prepare):
        """查询调拨出库单发货信息"""
        # 出库单id不存在
        response = request.get('/allocateOutboundOrder/deliveryInfo/0')
        log.info(response)
        assert response['msg'] == '调拨出库单不存在'
        # 正确的出库单id
        response2 = request.get('/allocateOutboundOrder/deliveryInfo/%s' % prepare[0])
        assert response2['msg'] == '请求成功'

    def test_05(self, prepare):
        """查询调拨出库单明细"""
        # 出库单id不存在
        response = request.get('/allocateOutboundOrder/detail/0')
        log.info(response)
        assert response['msg'] == '调拨出库单不存在'
        # 正确的出库单id
        response2 = request.get('/allocateOutboundOrder/detail/%s' % prepare[0])
        assert response2['msg'] == '请求成功'

    def test_06(self, prepare):
        """调拨出库单打印"""
        # 出库单id不存在
        response = request.get('/allocateOutboundOrder/print/0')
        log.info(response)
        assert response['msg'] == '调拨出库单不存在'
        # 正确的出库单id
        response2 = request.get('/allocateOutboundOrder/print/%s' % prepare[0])
        assert response2['msg'] == '请求成功'


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
