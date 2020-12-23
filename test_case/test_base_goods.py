# __author:"zonglr"
# date:2020/11/28
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, time
from common import logger, request
from test_config import param_config

log = logger.Log()


def create(name, commonName, skuCode, file='123', manufacturerName='11', minGoodsUnit='个', model='L',
           specification='L', price=20):
    body = {
        'commonName': commonName,
        'imageSource': [file],
        'manufacturerName': manufacturerName,
        'minGoodsUnit': minGoodsUnit,
        'model': model,
        'name': name,
        'price': price,
        'skuCode': skuCode,
        'specification': specification
    }
    response = request.post_body('/goods/createGoods', body=body)
    return response


class TestCreateGoods:
    """创建商品"""

    num = int(time.time() * 1000)
    skuCode = 'sku%d' % num
    goodsName = '测试商品%d' % num

    def test_01(self):
        response = create(name=self.goodsName, commonName=self.goodsName, skuCode=self.skuCode)
        log.info(response)


# 查询商品列表
def find_goods_list(manufacturerId, categoryCode=None, goodsIds=None, keyword=None, manufacturerName=None, pageNum=None,
                    pageSize=None, sortableColumnName=None, supplierName=None):
    params = {
        'categoryCode': categoryCode,
        'goodsIds': goodsIds,
        'keyword': keyword,
        'manufacturerId': manufacturerId,
        'manufacturerName': manufacturerName,
        'pageNum': pageNum,
        'pageSize': pageSize,
        'sortableColumnName': sortableColumnName,
        'supplierName': supplierName
    }
    response = request.get_params('/goods/findGoodsList', params=params)
    return response


class TestFindGoodsList:
    """查询商品列表"""

    # 获取品牌
    brands = request.get('/manufacturer/allBrands')
    brandId = brands['data'][0]['id']

    # 必填字段校验
    case1 = [
        ('未输入品牌', None, 0, 20, '请输入品牌'),
        ('未输入页码', brandId, None, 20, '请填写当前页码'),
        ('未输入分页大小', brandId, 0, None, '请填写分页大小')
    ]

    @pytest.mark.parametrize('casename,manufacturerId,pageNum,pageSize,msg', case1)
    def test_01(self, casename, manufacturerId, pageNum, pageSize, msg):
        """必填字段校验"""
        response = find_goods_list(manufacturerId=manufacturerId, pageNum=pageNum, pageSize=pageSize)
        log.info(response)
        assert response['msg'] == msg


# 商品列表
def find_list(commonName=None, manufacturerName=None, goodsName=None, sortableColumnName=None, pageNum=None,
              pageSize=None):
    params = {
        'pageNum': pageNum,
        'pageSize': pageSize,
        'commonName': commonName,  # 商品别名
        'manufacturerName': manufacturerName,  # 生产商名称
        'name': goodsName,
        'sortableColumnName': sortableColumnName  # array
    }
    response = request.get_params('/goods/findList', params=params)
    return response


class TestFindList:
    """商品列表"""

    # 必填字段校验
    case1 = [
        ('未输入页码', None, 20, '请填写当前页码'),
        ('未输入分页大小', 0, None, '请填写分页大小')
    ]

    @pytest.mark.parametrize('casename,pageNum,pageSize,msg', case1)
    def test_01(self, casename, pageNum, pageSize, msg):
        """必填字段校验"""
        response = find_list(pageNum=pageNum, pageSize=pageSize)
        log.info(response)
        assert response['msg'] == msg


# 查询辅耗材商品列表
def find_list_by_auxiliaryMaterial(manufacturerId, categoryCode=None, goodsIds=None, keyword=None,
                                   manufacturerName=None, pageNum=None, pageSize=None, sortableColumnName=None,
                                   supplierName=None):
    params = {
        'categoryCode': categoryCode,
        'goodsIds': goodsIds,
        'keyword': keyword,
        'manufacturerId': manufacturerId,
        'manufacturerName': manufacturerName,
        'pageNum': pageNum,
        'pageSize': pageSize,
        'sortableColumnName': sortableColumnName,
        'supplierName': supplierName
    }
    response = request.get_params('/goods/findListByAuxiliaryMaterial', params=params)
    return response


class TestFindListByAuxiliaryMaterial:
    """查询辅耗材商品列表"""

    # 获取品牌
    brands = request.get('/manufacturer/allBrands')
    brandId = brands['data'][0]['id']

    # 必填字段校验
    case1 = [
        ('未输入品牌', None, 0, 20, '请输入品牌'),
        ('未输入页码', brandId, None, 20, '请填写当前页码'),
        ('未输入分页大小', brandId, 0, None, '请填写分页大小')
    ]

    @pytest.mark.parametrize('casename,manufacturerId,pageNum,pageSize,msg', case1)
    def test_01(self, casename, manufacturerId, pageNum, pageSize, msg):
        """必填字段校验"""
        response = find_goods_list(manufacturerId=manufacturerId, pageNum=pageNum, pageSize=pageSize)
        log.info(response)
        assert response['msg'] == msg


# 查询主耗材商品列表
def find_list_by_mainMaterial(manufacturerId, categoryCode=None, goodsIds=None, keyword=None,
                              manufacturerName=None, pageNum=None, pageSize=None, sortableColumnName=None,
                              supplierName=None):
    params = {
        'categoryCode': categoryCode,
        'goodsIds': goodsIds,
        'keyword': keyword,
        'manufacturerId': manufacturerId,
        'manufacturerName': manufacturerName,
        'pageNum': pageNum,
        'pageSize': pageSize,
        'sortableColumnName': sortableColumnName,
        'supplierName': supplierName
    }
    response = request.get_params('/goods/findListByMainMaterial', params=params)
    return response


class TestFindListByMainMaterial:
    """查询主耗材商品列表"""

    # 获取品牌
    brands = request.get('/manufacturer/allBrands')
    brandId = brands['data'][0]['id']

    # 必填字段校验
    case1 = [
        ('未输入品牌', None, 0, 20, '请输入品牌'),
        ('未输入页码', brandId, None, 20, '请填写当前页码'),
        ('未输入分页大小', brandId, 0, None, '请填写分页大小')
    ]

    @pytest.mark.parametrize('casename,manufacturerId,pageNum,pageSize,msg', case1)
    def test_01(self, casename, manufacturerId, pageNum, pageSize, msg):
        """必填字段校验"""
        response = find_goods_list(manufacturerId=manufacturerId, pageNum=pageNum, pageSize=pageSize)
        log.info(response)
        assert response['msg'] == msg


# 查询主耗材下的辅耗材
def get_main_fit_relation(manufacturerId, categoryCode=None, goodsIds=None, keyword=None,
                          manufacturerName=None, pageNum=None, pageSize=None, sortableColumnName=None,
                          supplierName=None):
    params = {
        'categoryCode': categoryCode,
        'goodsIds': goodsIds,
        'keyword': keyword,
        'manufacturerId': manufacturerId,
        'manufacturerName': manufacturerName,
        'pageNum': pageNum,
        'pageSize': pageSize,
        'sortableColumnName': sortableColumnName,
        'supplierName': supplierName
    }
    response = request.get_params('/goods/getMainFitRelation', params=params)
    return response


class TestGetMainFitRelation:
    """查询主耗材下的辅耗材"""

    # 获取品牌
    brands = request.get('/manufacturer/allBrands')
    brandId = brands['data'][0]['id']

    # 必填字段校验
    case1 = [
        ('未输入品牌', None, 0, 20, '请输入品牌'),
        ('未输入页码', brandId, None, 20, '请填写当前页码'),
        ('未输入分页大小', brandId, 0, None, '请填写分页大小')
    ]

    @pytest.mark.parametrize('casename,manufacturerId,pageNum,pageSize,msg', case1)
    def test_01(self, casename, manufacturerId, pageNum, pageSize, msg):
        """必填字段校验"""
        response = find_goods_list(manufacturerId=manufacturerId, pageNum=pageNum, pageSize=pageSize)
        log.info(response)
        assert response['msg'] == msg


class TestGS1Decode:
    """GS1解析"""
    url = '/goods/gs1Decode'

    def test_01(self):
        params = {
            'code': 0
        }
        response = request.get_params(self.url, params=params)
        log.info(response)
        assert response['msg'] == '请求成功'


class TestSetEnable:
    """启用-禁用商品"""
    url = '/goods/setEnable'

    # 字段值校验
    case1 = [
        ('商品id为空', None, True, '请选择商品'),
        ('未选择启用禁用', 0, None, '请选择启用或者禁用商品')
    ]

    @pytest.mark.parametrize('casename,id,isEnabled,msg', case1)
    @pytest.mark.skip("提示语错误")
    def test_01(self, casename, id, isEnabled, msg):
        body = {
            'id': id,
            'isEnabled': isEnabled
        }
        response = request.put_body(self.url, body=body)
        log.info(response)
        assert response['msg'] == msg

