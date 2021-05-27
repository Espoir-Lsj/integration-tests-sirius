# -*- coding: utf-8 -*-
# @Time : 2021/5/26 4:47 下午 
# @Author : lsj
# @File : Data_Prepare.py
import time

from test_case.common.Order_Management import AdhocOrder
from test_case.common.PostgresSql import PostgresSql


def get_prepare():
    test = PostgresSql()
    # 查一个可以用来调拨的商品ID
    sql = "SELECT id FROM  md_goods where name like '接骨%' limit 1"
    a = test.selectAll(sql)
    # idList = []
    # dataList = []
    # for i in a:
    #     j = i[0]
    #     value = (i[0], 57, 57, 13, 'put_on_shelf', 43, 'f', 59, str(time.time()))
    #     dataList.append(value)
    #     idList.append(j)
    goodsId = a[0][0]
    valueList = []
    value = (goodsId, 57, 10, 13, 'put_on_shelf', 43, 'f', 59, str(time.time()))
    value1 = (goodsId, 57, 10, 6, 'put_on_shelf', 43, 'f', 59, str(time.time()))
    valueList.append(value)
    valueList.append(value1)
    # print(goodsId)
    # print(valueList)
    #
    manufacturer_id = AdhocOrder().get_manufacturerId()
    # 给商品绑定生产商
    sql001 = "UPDATE md_goods SET manufacturer_id = {} WHERE id in ({});".format(goodsId, manufacturer_id)
    test.execute(sql001)

    # 查出 仓库1 仓库2 共有的物资id 且有库存
    sql1 = """SELECT a.id FROM  md_goods a  LEFT JOIN wms_goods_stock b on  a.id = b.goods_id
     where a.name like '锁定%' and b.quantity>0  and warehouse_id in (6,13) limit 1;"""

    test.selectAll(sql1)
    goodsId = test.selectAll(sql1)[0][0]

    # 仓库2 添加 物资以及库存
    sql2 = """INSERT INTO sirius.wms_goods_stock
                    ( goods_id, goods_lot_info_id, quantity, warehouse_id, status, version,
                    is_packaged, storage_location_id, unique_code )
                  VALUES {}""".format(*valueList)
    test.execute(sql2)

    # 把物资库存改成一样的（两个仓库就数量相同），后续不能改了，就查这个物资在两个仓库的库存分别是多少
    # sql3 = """UPDATE sirius.wms_goods_stock SET quantity = 10 where goods_id in {}""".format(tuple(idList))
    sql3 = """UPDATE sirius.wms_goods_stock SET quantity = 10 where goods_id = {}""".format(goodsId)
    test.execute(sql3)

    #
    sql4 = """SELECT sum(quantity) ,warehouse_id from wms_goods_stock where warehouse_id in (6,13) 
    and goods_id ={} GROUP BY warehouse_id""".format(goodsId)

    data = test.selectAll(sql4)
    # 仓库1 的物资库存
    warehouse1 = data[0][0]
    # 仓库2 的物资库存
    warehouse2 = data[1][0]


get_prepare()
