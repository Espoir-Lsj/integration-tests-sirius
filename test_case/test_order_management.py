# -*- coding: utf-8 -*-
# @Time : 2021/5/18 1:21 下午 
# @Author : lsj
# @File : test_order_management.py

import allure, pytest, time, datetime
from common import Order_Management, logger, request

from test_config.yamlconfig import timeid

timeStamp = int(time.time() * 1000)
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday_stamp = int(time.mktime(yesterday.timetuple())) * 1000
fiveDaysAfter = today + datetime.timedelta(days=5)
fiveDaysAfter_stamp = int(time.mktime(fiveDaysAfter.timetuple())) * 1000
context = str('1').zfill(5000)
log = logger.Log()
longName = '主治医师主治医师主治医师主治医师主治医师主治医师主治医师主治医师主治医师主治医师主治医师主治医师主治医师'


# 订单管理：临调订单
@allure.feature('订单管理')
@allure.story('临调订单')
@pytest.mark.usefixtures('res_data')
class TestAdhocOrder:
    data = [
        ('物资id为空', {'goodsId': None}, '请输入商品id'),
        ('物资ID错误', {'goodsId': 1111111}, '商品不存在,请刷新重试'),
        ('套包ID为空', {'kitTemplateId': None}, '请输入套包id'),
        ('套包ID错误', {'kitTemplateId': 1111111}, '工具包不存在，请刷新重试'),
        ('物资、套包为空', {'goodsDetailUiBeans': [], 'toolsDetailUiBeans': []}, '请选择物资'),
        ('医院为空', {'hospitalName': None}, '请输入医院名称'),
        ('医院名字超长', {'hospitalName': context}, '医院名称长度超出限制'),
        ('手术部位为空', {'procedureSite': None}, '请选择手术部位'),
        ('手术部位错误', {'procedureSite': [9999999]}, '请选择正确的手术部位'),
        ('主刀医生为空', {'surgeon': None}, '请输入正确的主刀医生姓名'),
        ('主刀医生超长', {'surgeon': longName}, '主刀医生名称长度超出限制'),
        ('订单联系人为空', {'contactName': None}, '请输入正确的联系人姓名'),
        ('联系人电话为空', {'contactPhone': None}, '请输入正确的手机号码'),
        ('品牌为空', {'manufacturerId': None}, '品牌不能为空'),
        ('收货方式为空', {'deliveryMode': None}, '请选择收货方式'),
        ('性别为空', {'gender': None}, '请选择患者性别'),
        ('年龄段为空', {'ageGroup': None}, '请选择患者年龄'),
        ('年龄段错误', {'ageGroup': 'None'}, '请求参数异常'),
        # ('收件人为空', {'receivingName': None}, ''),
        ('默认地址为空', {'addressId': None}, '请输入收货地址id'),
        ('默认地址错误', {'addressId': 9999999}, '所选地址不存在，请刷新重试'),
        # ('经销商为空', {'supplierId': None}, ''),
        ('手术时间为空', {'procedureTime': None}, '请选择手术日期'),
        ('归还时间为空', {'expectReturnTime': None}, '请选择归还日期'),
        ('手术日期小于当天', {'procedureTime': yesterday_stamp}, '手术日期不能早于当天'),
        ('归还时间小于手术开始时间', {'expectReturnTime': yesterday_stamp}, '预计归还日期不能早于手术日期'),
    ]

    @pytest.mark.parametrize('title,case,expected', data)
    @allure.title('{title}')
    def test_create(self, title, case, expected, AdhocOrder_get_id):
        url = '/adhocOrder/create'
        body = timeid(file_yaml='request_data.yaml')._get_yaml_element_info()[url]
        body = request.reValue(body, case)
        response = request.post_body01(url, body)
        assert response['msg'] == expected
