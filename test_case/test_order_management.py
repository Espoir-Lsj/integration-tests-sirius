# -*- coding: utf-8 -*-
# @Time : 2021/5/18 1:21 下午 
# @Author : lsj
# @File : test_order_management.py


import allure, pytest, time, datetime
from test_case.common import Order_Management, logger, request, Data_driven, login

timeStamp = int(time.time() * 1000)
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday_stamp = int(time.mktime(yesterday.timetuple())) * 1000
fiveDaysAfter = today + datetime.timedelta(days=5)
fiveDaysAfter_stamp = int(time.mktime(fiveDaysAfter.timetuple())) * 1000
context = str('1').zfill(5000)
log = logger.Log()
longName = '主治医师' * 30

sheetname = "Sheet1"
# url = '/adhocOrder/create'
get_data = Data_driven.ExcelData(sheetname)
get_datas = Data_driven.CsvData()
supplierId = login.supplierId


# 订单管理：临调订单
@allure.feature('订单管理')
# @pytest.mark.usefixtures('res_data')
class TestAdhocOrder:
    data = [('物资id为空', {'goodsId': None}, '请输入商品id'),
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
    @allure.story('临调订单——创建临调单')
    @allure.title('{title}')
    def test_create(self, title, case, expected, AdhocOrder_get_id):
        url = '/adhocOrder/create'
        body = request.body_replace(url, case)
        response = request.post_body(url, body)
        assert response['msg'] == expected

    data = get_datas.get_csv('/adhocOrder/reject')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('临调订单——拒绝临调单')
    @allure.title('{title}')
    def test_reject(self, url, title, case, expected, AdhocOrder_get_id02):
        body = {
            "reason": '拒绝',
            "accept": False,
            "id": AdhocOrder_get_id02
        }
        body = request.reValue_01(body, case)
        response = request.put_body01(url, body)
        assert response['msg'] == expected

    data = get_datas.get_csv('/adhocOrder/edit')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('临调订单——编辑临调单')
    @allure.title('{title}')
    def test_edit(self, url, title, case, expected, AdhocOrder_edit, AdhocOrder_reject01):

        body = request.body_replace(url, case)
        body['orderUiBean']['id'] = AdhocOrder_reject01
        response = request.put_body(url, body)
        if title == '商品/套包数量为空':
            assert expected in response['msg']
        else:
            assert response['msg'] == expected

    data = get_datas.get_csv('/adhocOrder/edit1')

    @pytest.mark.parametrize('url1,title,case,expected', data)
    @allure.story('临调订单——编辑临调单')
    @allure.title('{title}')
    def test_edit02(self, url1, title, case, expected, AdhocOrder_edit, AdhocOrder_reject):
        url = '/adhocOrder/edit'
        body = request.body_replace(url, case)
        response = request.put_body(url, body)
        assert response['msg'] == expected

    data = get_datas.get_csv('/adhocOrder/accept')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('临调订单——接收临调单')
    @allure.title('{title}')
    def test_accept(self, url, title, case, expected, AdhocOrder_accept):
        body = request.body_replace(url, case)
        response = request.put_body01(url, body)
        if title == '商品数量为空' or title == '套包数量为空':
            assert '请输入' in response['msg']
        else:
            assert response['msg'] == expected

    data = get_datas.get_csv('/adhocOrder/accept1')

    @pytest.mark.parametrize('url1,title,case,expected', data)
    @allure.story('临调订单——接收临调单')
    @allure.title('{title}')
    def test_accept01(self, url1, title, case, expected, AdhocOrder_get_id01,AdhocOrder_accept):
        url = '/adhocOrder/accept'
        body = request.body_replace(url, case)
        body['id'] = AdhocOrder_get_id01
        print(body)
        body['detail'][0]['toolsDetailUiBeans'][0]['quantity'] = 99999
        response = request.put_body01(url, body)
        assert response['msg'] == expected



    data = get_datas.get_csv('/adhocOrder/close')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('临调订单——关闭临调单')
    @allure.title('{title}')
    def test_close(self, url, title, case, expected, AdhocOrder_close):
        if title == '重复关闭订单':
            case = None
        body = request.body_replace(url, case)
        response = request.put_body01(url, body)
        assert response['msg'] == expected

    data = get_datas.get_csv('/supplier/addReceivingAddress')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('临调订单——创建默认地址')
    @allure.title('{title}')
    def test_addReceivingAddress(self, url, title, case, expected, AdhocOrder_add_address):
        body = request.body_replace(url, case)
        response = request.post_body(url, body)
        assert response['msg'] == expected

    data = get_datas.get_csv('/supplier/updateReceivingAddress')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('临调订单——修改默认地址')
    @allure.title('{title}')
    def test_updateReceivingAddress(self, url, title, case, expected, AdhocOrder_update_address):
        body = request.body_replace(url, case)
        response = request.put_body(url, body)
        assert response['msg'] == expected

    # @allure.story('临调订单——修改默认地址')
    # @allure.title('经销商修改供应商地址')
    # def test_updateReceivingAddress01(self):
    #     addressId = request.get('/supplier/getReceivingAddress?dealerId=%s' % supplierId)['data'][0]['id']
    #     response = Order_Management.AdhocOrder().update_default_address(id=addressId)
    #     assert response['msg'] == '不可操作其他经销商数据'

    data = [('id为空', {'id': None}, 'id不能为空'),
            ('id为空', {'id': 99990099}, '地址不存在')]

    @pytest.mark.parametrize('title,case,expected', data)
    @allure.story('临调订单——设置默认地址')
    @allure.title('{title}')
    def test_setDefaultAddress(self, title, case, expected):
        url = '/supplier/setDefaultReceivingAddress'
        body = {
            'id': None
        }
        body = request.reValue_01(body, case)
        response = request.put_body(url, body)
        assert response['msg'] == expected

    data = get_datas.get_csv('/adhocOrder/updateAddress')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('临调订单——修改收货地址')
    @allure.title('{title}')
    def test_updateAddress(self, url, title, case, expected, AdhocOrder_updateAddress):
        body = request.body_replace(url, case)
        response = request.post_body(url, body)
        assert response['msg'] == expected

    data = get_datas.get_csv('/adhocOrder/adhocReturn')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('临调订单——提交销用')
    @allure.title('{title}')
    def test_return(self, url, title, case, expected, Prepare_adhocOrder):

        body = request.body_replace(url, case)
        if title == '重复提交':
            body['parentAdhocOrderId'] = Prepare_adhocOrder[2]
            body['detail'][0]['childAdhocOrderId'] = Prepare_adhocOrder[2]
        if title in ('商品错误', '批次信息错误'):
            body['parentAdhocOrderId'] = Prepare_adhocOrder[0]
            body['detail'][0]['childAdhocOrderId'] = Prepare_adhocOrder[0]
        response = request.post_body(url, body)
        assert response['msg'] == expected

    @allure.title('用户无权限')
    def test_return01(self, Prepare_adhocOrder):
        url = '/adhocOrder/adhocReturn'
        case = {"quantity": 1}
        body = request.body_replace(url, case)
        response = request.post_body01(url, body)
        assert response['msg'] == '权限不足'

    data = get_datas.get_csv('/salesOrder/createSalesOrder')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('临调订单——创建销售单')
    @allure.title('{title}')
    def test_create(self, url, title, case, expected, Prepare_adhocOrder):
        body = request.body_replace(url, case)

        if title == '子订单ID错误':
            body['parentId'] = Prepare_adhocOrder[1]
        if title in ('商品ID错误', '批次信息错误', '商品数量为空', '商品数量错误'):
            body['parentId'] = Prepare_adhocOrder[1]
            body['createUiBeans'][0]['adhocOrderId'] = Prepare_adhocOrder[1]
        response = request.post_body01(url, body)
        assert response['msg'] == expected

    data = get_datas.get_csv('/salesOrder/checkSalesOrder')

    @pytest.mark.parametrize('url,title,case,expected', data)
    @allure.story('临调订单——检查销售单')
    @allure.title('{title}')
    def test_check(self, url, title, case, expected, Prepare_adhocOrder):
        body = request.body_replace(url, case)
        if title == '子订单ID错误':
            body['parentId'] = Prepare_adhocOrder[1]
        if title in ('商品ID错误', '批次信息错误', '商品数量为空', '商品数量错误'):
            body['parentId'] = Prepare_adhocOrder[1]
            body['createUiBeans'][0]['adhocOrderId'] = Prepare_adhocOrder[1]
        response = request.post_body01(url, body)
        assert response['msg'] == expected

    def test1(self, Prepare_adhocOrder):
        pass
# 568
