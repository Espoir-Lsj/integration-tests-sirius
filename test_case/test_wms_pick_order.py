# __author:"zonglr"
# date:2020/12/8
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, datetime, time
from common import params, request, logger
from faker import Faker
from common import adhocOrder, pick
from test_config import param_config

log = logger.Log()


# 创建一个待拣货的拣货单
@pytest.fixture(scope="module")
def prepare_pick_order():
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
    return pickOrderId


class TestApproval:
    """拣货单审核"""

    def test_01(self):
        """拣货单id不存在"""
        response = request.put('/pickOrder/approval/0')
        log.info(response)
        assert response['msg'] == '拣货单不存在'


class TestDetail:
    """获取拣货单详情"""

    def test_01(self):
        """拣货单id不存在"""
        response = request.get('/pickOrder/detail/0')
        log.info(response)
        assert response['msg'] == '拣货单不存在'


class TestDetailPda:
    """在PDA上获取拣货单详情"""

    def test_01(self):
        """拣货单id不存在"""
        response = request.get('/pickOrder/detailByPda/0')
        log.info(response)
        assert response['msg'] == '拣货单不存在'

    def test_02(self, prepare_pick_order):
        """拣货单存在"""
        response = request.get('/pickOrder/detailByPda/%s' % prepare_pick_order)
        assert response['msg'] == '请求成功'


class TestList:
    """查询拣货单列表"""
    url = '/pickOrder/list'

    # 列举需要测试的查询条件和值，组合查询
    # 状态（每个状态都需要查询一次，组合状态查询一次）
    statusList = ['pick_pending', 'picking', 'finish']
    # 关键字
    keyword = ['123', '%%%', 'TEST']
    # 类型
    type = ['allocate', 'packaging']

    @pytest.mark.parametrize('statusList', statusList)
    @pytest.mark.parametrize('keyword', keyword)
    @pytest.mark.parametrize('type', type)
    def test_01(self, statusList, keyword, type):
        """组合查询"""
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'status': statusList,
            'keyword': keyword,
            'type': type
        }
        r = request.get_params(self.url, params=params)
        assert r['msg'] == '请求成功'


class TestPickFinished:
    """拣货完成"""
    url = '/pickOrder/pickFinished'

    def test_01(self):
        """拣货单id不存在"""
        body = {
            'imagePath': ['123'],
            "pickOrderId": 0
        }
        response = request.put_body(self.url, body=body)
        log.info(response)
        assert response['msg'] == '拣货单不存在'

    def test_02(self, prepare_pick_order):
        """拣货未完成，提交拣货单"""
        body = {
            'imagePath': ['123'],
            "pickOrderId": prepare_pick_order
        }
        response = request.put_body(self.url, body=body)
        log.info(response)
        assert response['msg'] == '存在未拣货完成的商品不能结束拣货'


class TestPicking:
    """拣货"""
    url = '/pickOrder/picking'

    @pytest.fixture(scope="class")
    def detail(self, prepare_pick_order):
        """根据拣货单id查询详情"""
        detail = request.get('/pickOrder/detail/%s' % prepare_pick_order)
        assert detail['msg'] == '请求成功'
        # 获取待拣货商品的详情
        goodsId = detail['data']['goodsDetail'][0]['goodsId']
        lotNum = detail['data']['goodsDetail'][0]['lotNum']
        serialNumber = detail['data']['goodsDetail'][0]['serialNumber']
        storageLocationId = detail['data']['goodsDetail'][0]['storageLocationId']
        return goodsId, lotNum, serialNumber, storageLocationId

    def test_01(self, detail, prepare_pick_order):
        """批号为空"""
        response = pick.pickOne(detail[0], None, detail[2], detail[3], prepare_pick_order)
        log.info(response)
        assert response['msg'] == '该批次商品不存在'

    def test_02(self, detail, prepare_pick_order):
        """物资id为空"""
        response = pick.pickOne(None, detail[1], detail[2], detail[3], prepare_pick_order)
        log.info(response)
        assert response['msg'] == '请选择需要拣的物资'

    def test_03(self, detail, prepare_pick_order):
        """货位号为空"""
        response = pick.pickOne(detail[0], detail[1], detail[2], None, prepare_pick_order)
        log.info(response)
        assert response['msg'] == '拣货的商品或该批次的商品在拣货单中不存在'

    def test_04(self,detail,prepare_pick_order):
        """货位号不存在"""
        response = pick.pickOne(detail[0], detail[1], detail[2], 'test', prepare_pick_order)
        log.info(response)
        assert response['msg'] == '请求参数异常'

    def test_05(self,detail,prepare_pick_order):
        """拣货单id为空"""
        response = pick.pickOne(detail[0], detail[1], detail[2], detail[3], None)
        log.info(response)
        assert response['msg'] == '请选择拣货单'

    def test_06(self,detail,prepare_pick_order):
        """拣货单id不存在"""
        response = pick.pickOne(detail[0], detail[1], detail[2], detail[3], 0)
        log.info(response)
        assert response['msg'] == '拣货单不存在'

    def test_07(self,detail,prepare_pick_order):
        """重复拣货"""
        response = pick.pickOne(detail[0], detail[1], detail[2], detail[3], prepare_pick_order)
        log.info(response)
        response2 = pick.pickOne(detail[0], detail[1], detail[2], detail[3], prepare_pick_order)
        log.info(response2)
        assert response2['msg'] == '该商品已拣货完成请勿重复操作'