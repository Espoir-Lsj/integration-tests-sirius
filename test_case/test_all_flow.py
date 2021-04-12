import time, datetime, pytest, jsonpath, re
from common import logger, request, adhocOrder, inboundOrder, outboundOrder, salesOrder, pick, putOnShelf, accept
from faker import Faker

from common.adhocOrder import supplierId, siteId, brandId
from test_config import param_config
import func_timeout

log = logger.Log()
faker = Faker(locale='zh_CN')


@func_timeout.func_set_timeout(6)
def askChoice(text):
    return input('%s:\n' % text)


# # 去除括号
# def test_num():
#     UDI = input('\n输入UDI：')
#     num = re.sub(r'\D', "", UDI)
#     print('\n去除括号后的值：%s' % num)


class TestAll:
    # 调拨数量
    transferQuantity = 4
    # 消耗数量
    consumeQuantity = 1  # 待验收数量=调拨数量-消耗数量
    # 实际验收数量
    receiveQuantity = 1  # 实际消耗数量=调拨数量-实际验收数量
    # 临调单id
    adhocOrderId = ''
    # 临调单号
    adhocOrderCode = ''
    # 拣货单id
    pickOrderId = ''
    # 入库单id
    allocateInboundOrderId = ''
    # 物资id
    goodsId = param_config.goodsId

    @classmethod
    def setup_class(cls):
        # 获取今天、明天、后天的时间戳
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        twoDaysAfter = today + datetime.timedelta(days=2)
        yesterday = today - datetime.timedelta(days=1)
        cls.today_stamp = int(time.mktime(today.timetuple())) * 1000
        cls.tomorrow_stamp = int(time.mktime(tomorrow.timetuple())) * 1000
        cls.twoDaysAfter_stamp = int(time.mktime(twoDaysAfter.timetuple())) * 1000
        cls.yesterday_stamp = int(time.mktime(yesterday.timetuple())) * 1000

    def test_01_list(self):
        """临调单列表"""
        list = request.get('/adhocOrder/findList?pageNum=0&pageSize=50')
        assert list['msg'] == '请求成功'

    @pytest.mark.待拣货
    @pytest.mark.待出库
    @pytest.mark.待回库
    @pytest.mark.待验收
    @pytest.mark.待上架
    @pytest.mark.待生成销售单
    @pytest.mark.主流程
    @pytest.mark.dependency(name='create')
    def test_02_create(self):
        """创建临调单"""
        log.info('------开始创建临调单------')
        # 获取供应商列表
        list = request.get('/supplier/dropDownSupplierList')
        # 获取供应商id
        supplierId = list['data'][0]['id']
        # 获取手术部位
        site = request.get('/dictionary/getByType/procedure_site')
        siteId = site['data'][0]['id']
        # 获取品牌
        brands = request.get('/manufacturer/allBrands')
        brandId = brands['data'][0]['id']
        # 查询商品主耗材列表
        goods = request.get('/goods/findListByMainMaterial?pageNum=0&pageSize=50&manufacturerId=%d' % brandId)
        goodsId = goods['data']['rows'][0]['id']
        stockQuantity = goods['data']['rows'][0]['stockQuantity']

        # 创建临调单的参数
        body = {
            'toolsDetailUiBeans': [],
            'goodsDetailUiBeans': [],
            'orderUiBean': {
                'ageGroup': 'adult',
                'gender': 'male',
                'supplierId': supplierId,
                'hospitalName': '测试',
                'procedureSite': [siteId],
                'surgeon': faker.name(),
                'procedureTime': self.tomorrow_stamp,
                'expectReturnTime': self.twoDaysAfter_stamp,
                'postcode': faker.postcode(),
                'contactName': '本单勿动谢谢',
                'contactPhone': faker.phone_number(),
                'manufacturerId': brandId,
                'deliveryMode': 'SELF_PIKE_UP',  # 快递DELIVERY  自提SELF_PIKE_UP
                'receivingName': faker.name(),
                'receivingIdCard': faker.ssn(),
                'receivingPhone': faker.phone_number(),
                'districtCode': 110101000000,
                'receivingAddress': faker.address(),
                'powerOfAttorney': '123',
                'consignorName': faker.name(),
                'consignorPhone': faker.phone_number()
            }
        }
        # 通过控制台输入是否需要工具包，如果6秒内未输入则不调拨工具包
        try:
            type = askChoice('请选择调拨类型：1-仅调拨物资，2-调拨物资+工具包，3-仅调拨工具包')
        except func_timeout.exceptions.FunctionTimedOut as e:
            type = '1'  # 默认仅调拨物资

        # 物资信息
        goods = {
            'goodsId': self.goodsId,
            'quantity': self.transferQuantity,
            'supplierId': supplierId
        }
        # 工具包信息
        tools = {
            "kitTemplateId": param_config.kitTemplateId,
            "quantity": 1,
            "supplierId": supplierId
        }
        if type == '2':
            # body中追加物资信息
            body['goodsDetailUiBeans'] = [goods]
            # body中追加工具包
            body['toolsDetailUiBeans'] = [tools]
        elif type == '3':
            body['toolsDetailUiBeans'] = [tools]
        else:
            body['goodsDetailUiBeans'] = [goods]

        log.info('传入的参数 %s' % body)

        # 创建临调单
        create = request.post_body('/adhocOrder/appCreate', body=body)
        try:
            assert create['msg'] == '请求成功'
        except:
            raise Exception(create['msg'], create['exMsg'])
        # 保存临调单id，code
        TestAll.adhocOrderId = create['data']['id']
        log.info('生成的临调单id: %s' % TestAll.adhocOrderId)
        TestAll.adhocOrderCode = create['data']['code']
        log.info('生成的临调单code: %s' % TestAll.adhocOrderCode)

    @pytest.mark.skip
    def test_03_get(self):
        """查询接口"""
        # 查询订单地址
        response = request.get('/adhocOrder/getAddress?id=%s' % self.adhocOrderId)
        log.info(response)
        # 查询订单明细
        response2 = request.get('/adhocOrder/getDetail?orderId=%s' % self.adhocOrderId)
        log.info(response2)

    @pytest.mark.主流程
    @pytest.mark.dependency(depends=["create"])
    # @pytest.mark.skip
    # 跳过
    def test_04_refuse(self):
        """退回临调单"""
        # 拒绝临调单
        if self.adhocOrderId == '':
            id = input("\n输入临调单id:")
        else:
            id = self.adhocOrderId
        response = request.put_body('/adhocOrder/reject',
                                    body={'id': id, 'reason': 'refuse'})
        log.info(response)
        assert response['msg'] == '请求成功'

    @pytest.mark.主流程
    @pytest.mark.dependency(depends=["create"])
    # @pytest.mark.skip
    def test_05_edit(self):
        """修改临调单"""
        # 查看临调单详情
        # detail = request.get('/adhocOrder/getDetailByOrderId?orderId=%s' % 705)
        detail = request.get('/adhocOrder/getDetailByOrderId?orderId=%s' % self.adhocOrderId)
        orderUiBean = {
            'ageGroup': 'adult',
            'gender': 'male',
            'supplierId': supplierId,
            'hospitalName': '测试',
            'procedureSite': [siteId],
            'surgeon': faker.name(),
            'procedureTime': self.tomorrow_stamp,
            'expectReturnTime': self.twoDaysAfter_stamp,
            'postcode': faker.postcode(),
            'contactName': '本单勿动谢谢',
            'contactPhone': faker.phone_number(),
            'manufacturerId': brandId,
            'deliveryMode': 'SELF_PIKE_UP',  # 快递DELIVERY  自提SELF_PIKE_UP
            'receivingName': faker.name(),
            'receivingIdCard': faker.ssn(),
            'receivingPhone': faker.phone_number(),
            'districtCode': 110101000000,
            'receivingAddress': faker.address(),
            'powerOfAttorney': '123',
            'consignorName': faker.name(),
            'consignorPhone': faker.phone_number(),
            'id': self.adhocOrderId
        }
        goodsDetail = detail['data']['childUiList'][0]['detailBeanUiList']
        toolsDetails = detail['data']['childUiList'][0]['toolsKitUiBeans']
        # 根据详情数据重新生成新的ARRAY
        new_goodssDetails = []
        for i in goodsDetail:
            Tdetail = {
                'goodsId': i['goodsId'],
                'quantity': i['quantity'],
            }
            new_goodssDetails.append(Tdetail)

        new_toolsDetails = []
        for i in toolsDetails:
            Tdetail = {
                'kitTemplateId': i['id'],
                'quantity': i['templateQuantity'],
                # 'supplierId': i['supplierId']
            }
            new_toolsDetails.append(Tdetail)  # T数组添加数据

        response = adhocOrder.edit_order1(orderUiBean, new_goodssDetails, new_toolsDetails)
        log.info(response)
        assert response['msg'] == '请求成功'

    @pytest.mark.待拣货
    @pytest.mark.待出库
    @pytest.mark.待回库
    @pytest.mark.待验收
    @pytest.mark.待上架
    @pytest.mark.待生成销售单
    @pytest.mark.主流程
    @pytest.mark.dependency(name='accept', depends=["create"])
    def test_06_accept(self):
        """接收临调单"""
        log.info('------接收临调单------')
        # 如果临调单号为空则输入临调单
        if self.adhocOrderId == '':
            id = input("\n输入临调单id:")
        else:
            id = self.adhocOrderId
        # body = {
        #     "detail": [
        #         {
        #             "deliveryMode": "DELIVERY",
        #             "goodsDetailUiBeans": [
        #                 {
        #                     "goodsId": self.goodsId,
        #                     "quantity": self.transferQuantity
        #                 }
        #             ],
        #             "toolsDetailUiBeans": [
        #                 {
        #                     "kitTemplateId": param_config.kitTemplateId,
        #                     "quantity": 1
        #                 }
        #             ],
        #             "warehouseId": 6
        #         }
        #     ],
        #     "id": id
        # }
        # response = request.put_body('/adhocOrder/accept', body=body)
        response = accept.check(self.adhocOrderId)
        try:
            assert response['msg'] == '请求成功'
        except:
            raise Exception(response['msg'], response['exMsg'])
        log.info('临调单接收成功 %s' % accept)
        # 根据临调单id查询临调单code
        getDetail = request.get(
            '/adhocOrder/getDetailByOrderId?orderId=%s' % id)
        # 临调单code
        adhocOrderCode = getDetail['data']['adhocOrderUiBean']['code']
        # 根据临调单code查询拣货单id
        getList = request.get(
            '/allocateOutboundOrder/list?pageNum=0&pageSize=20&keyword=%s' % adhocOrderCode)
        assert getList['msg'] == '请求成功'
        # 保存拣货单id
        TestAll.pickOrderId = getList['data']['rows'][0]['pickOrderId']
        log.info('生成的拣货单id: %s' % TestAll.pickOrderId)

    @pytest.mark.待出库
    @pytest.mark.待回库
    @pytest.mark.待验收
    @pytest.mark.待上架
    @pytest.mark.待生成销售单
    @pytest.mark.主流程
    @pytest.mark.dependency(name='pick', depends=["accept"])
    def test_07_pick(self):
        """拣货"""
        log.info('------拣货------')
        # 根据临调单code查询拣货单id, 如果临调单code为空则手工输入拣货单id
        if self.pickOrderId == '':
            pickOrderId = input("\n输入拣货单id:")
        else:
            pickOrderId = self.pickOrderId
        # 拣货
        finish_response = pick.finishPick(pickOrderId)
        assert finish_response['msg'] == '请求成功'

    @pytest.mark.待回库
    @pytest.mark.待验收
    @pytest.mark.待上架
    @pytest.mark.待生成销售单
    @pytest.mark.主流程
    @pytest.mark.dependency(name='outbound', depends=["pick"])
    def test_08_outbound(self):
        """发货审核"""
        log.info('------出库，发货审核------')
        # 根据临调单code查询出库单id, 临调单code为空时需手工输入出库单号
        if self.adhocOrderCode == '':
            keyword = input("\n输入出库单号:")
        else:
            keyword = self.adhocOrderCode
        # 出库审核
        approval_response = outboundOrder.approval(keyword)
        assert approval_response['msg'] == '请求成功'

    @pytest.mark.待验收
    @pytest.mark.待上架
    @pytest.mark.待生成销售单
    @pytest.mark.主流程
    @pytest.mark.dependency(name='inbound', depends=["outbound"])
    def test_09_inbound(self):
        """回库--提交销用信息"""
        log.info('------回库，提交入库单------')
        # 根据临调单id查询待入库的入库单，临调单id为空时需手工输入
        if self.adhocOrderId == '':
            adhocOrderId = input("\n输入临调单id:")
        else:
            adhocOrderId = self.adhocOrderId
        # 提交入库单
        submit_response = inboundOrder.submit(adhocOrderId, self.consumeQuantity)
        assert submit_response['msg'] == '请求成功'

    @pytest.mark.待上架
    @pytest.mark.待生成销售单
    @pytest.mark.主流程
    @pytest.mark.dependency(name='inbound_check', depends=["inbound"])
    def test_10_inbound_check(self):
        """入库单验收"""
        log.info('------入库单开始验收------')
        """入库单验收"""
        # 根据临调单号查询入库单id，临调单号为空时，输入入库单id
        if self.adhocOrderCode == '':
            allocateInboundOrderId = input("\n输入入库单id:")
        else:
            # 根据临调单号查询入库单id
            getList = request.get(
                # '/allocateInboundOrder/getDetailByCode?pageNum=0&pageSize=50&keyword=%s' % self.adhocOrderCode)
                '/allocateInboundOrder/getDetailByOrderId?orderId=%s' % self.adhocOrderId)
            assert getList['msg'] == '请求成功'
            allocateInboundOrderId = getList['data']['allocateInboundOrderId']
        # 入库单验收, 实际验收数量比待验收数量少1
        check_response = inboundOrder.check(allocateInboundOrderId, subNum=1)
        #
        # # 入库单验收, 实际验收数量和待验收数量相等
        # check_response = inboundOrder.check(allocateInboundOrderId, subNum=1)
        assert check_response['msg'] == '请求成功'

    # @pytest.mark.待生成销售单
    # @pytest.mark.主流程
    # @pytest.mark.dependency(name='put_on_shelf', depends=["inbound_check"])
    # def test_11_put_on_shelf(self):
    #     """"上架商品"""
    #     log.info('------开始上架商品------')
    #     if self.adhocOrderCode == '':
    #         allocateInboundOrderCode = input("\n输入入库单id:")
    #     else:
    #         # 根据临调单号查询入库单id
    #         getList = request.get(
    #             # '/allocateInboundOrder/getDetailByCode?pageNum=0&pageSize=50&keyword=%s' % self.adhocOrderCode)
    #             '/allocateInboundOrder/getDetailByOrderId?orderId=%s' % self.adhocOrderId)
    #         assert getList['msg'] == '请求成功'
    #         allocateInboundOrderCode = getList['data']['allocateInboundOrderCode']
    #     putOn_response = putOnShelf.put_all(allocateInboundOrderCode)
    #     assert putOn_response['msg'] == '请求成功'

    @pytest.mark.主流程
    @pytest.mark.dependency(name='check_sales_order', depends=["put_on_shelf"])
    def test_13_check_sales_order(self):
        """生成销售单"""
        log.info('------开始生成销售单------')
        # 根据临调单id查询待生成销售单的入库单，临调单id为空时需手工输入
        if self.adhocOrderId == '':
            adhocOrderId = input("\n输入临调单id: ")
        else:
            adhocOrderId = self.adhocOrderId
        # 生成销售单
        check_response = salesOrder.check(adhocOrderId, subNum=0)
        # 生成销售单   subNum协商数量 跟 实际验收的差值  不为0 的话，说明消耗数量 和生成销售数量不匹配 无法生成销售单
        # check_response = salesOrder.check(adhocOrderId, subNum=0)

        # assert check_response['msg'] == '请求成功'#data 返回的是[] 加断言 会报类型错误

    def test_14_get_detail(self):
        """查询临调订单明细"""
        adhocOrder.getDetail(self.adhocOrderId)

    @pytest.mark.dependency(name='inbound_check', depends=["check_sales_order"])
    def test_15_inbound_check(self):
        """销售单生成的入库单验收"""
        log.info('------销售单生成的入库单开始验收------')
        # 根据临调单号查询入库单id，临调单号为空时，输入入库单id
        if self.adhocOrderCode == '':
            allocateInboundOrderId = input("\n输入入库单id:")
        else:
            # 根据临调单号查询待验收入库单id
            params = {
                'pageNum': 0,
                'pageSize': 50,
                'status[0]': 'receiving_pending',
                'keyword': self.adhocOrderCode
            }
            getList = request.get_params('/allocateInboundOrder/findList', params=params)
            # 判断查询出的结果数量是否为1
            assert getList['data']['totalCount'] == 1
            allocateInboundOrderId = getList['data']['rows'][0]['allocateInboundOrderId']
        # 入库单验收, 实际验收数量比待验收数量少1
        check_response = inboundOrder.check(allocateInboundOrderId, subNum=1)
        assert check_response['msg'] == '销售订单下生成的入库单，验收数量应和待入库数量一致'
        # 入库单验收，实际验收数量等于待验收数量
        check_response2 = inboundOrder.check(allocateInboundOrderId, subNum=0)
        assert check_response2['msg'] == '请求成功'

    @pytest.mark.dependency(depends=["inbound_check"])
    def test_16_get_detail_by_app(self):
        """查询消耗详情"""
        # 根据临调单号查询销售单id
        response = request.get('/salesOrder/list?pageNum=0&pageSize=50&adhocOrderCode=%s' % self.adhocOrderCode)
        assert response['msg'] == '请求成功'
        salesOrderId = response['data']['rows'][0]['id']
        # 根据销售单id查询销售订单详情
        response3 = request.get('/salesOrder/getDetailById?id=%s' % salesOrderId)
        assert response3['msg'] == '请求成功'

    @pytest.mark.dependency(depends=["inbound_check"])
    def test_17_get_detail(self):
        """查询临调订单明细"""
        adhocOrder.getDetail(self.adhocOrderId)


if __name__ == '__main__':
    pytest.main(["-s", "test_all_flow.py"])
