# __author:"zonglr"
# date:2020/12/9
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import time, datetime
from common import logger, request
from faker import Faker

log = logger.Log()
faker = Faker(locale='zh_CN')

today = datetime.date.today()
today_stamp = int(time.mktime(today.timetuple())) * 1000


def approval(keyword):
    # 根据keyword查询列表详情
    getList = request.get(
        '/allocateOutboundOrder/list?pageNum=0&pageSize=50&status=delivery_pending&status=pick_pending&keyword=%s' % keyword)
    # 出库单id
    outboundOrderId = getList['data']['rows'][0]['id']
    # 提货方式
    deliveryMode = getList['data']['rows'][0]['deliveryMode']

    # 当提货方式为快递时
    if deliveryMode == 'DELIVERY':
        # 发货
        body = {
            'logisticsCompany': '京东',
            'expressNo': 'JD881991899',
            'deliveryDate': today_stamp,
            'id': outboundOrderId,
            'deliveryMode': 'DELIVERY'
        }
        response = request.put_body('/allocateOutboundOrder/delivery', body=body)
        assert response['msg'] == '请求成功'
        log.info('发货单发货成功')
        # 审核
        approval = request.put_body('/allocateOutboundOrder/approval', body=body)
        log.info('发货单审核成功')
        return approval
    # 当提货方式为自提时
    if deliveryMode == 'SELF_PIKE_UP':
        # 发货
        body = {
            'id': outboundOrderId,
            "deliveryMode": "SELF_PIKE_UP"
        }
        response = request.put_body('/allocateOutboundOrder/delivery', body=body)
        assert response['msg'] == '请求成功'
        log.info('发货单发货成功')
        # 审核
        body2 = {
            'logisticsCompany': '京东',
            'deliveryDate': today_stamp,
            'id': outboundOrderId
        }
        approval = request.put_body('/allocateOutboundOrder/approval', body=body2)
        log.info('发货单审核成功')
        return approval
