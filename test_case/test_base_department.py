# __author:"zonglr"
# date:2020/11/28
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pytest, time
from common import logger, request
from test_config import param_config

log = logger.Log()


# 创建部门
def createUser(departmentName, departmentTypeId, director, isEnabled, parentId, phone, sort):
    body = {
        'departmentName': departmentName,  # 部门名称
        'departmentTypeId': departmentTypeId,  # 分类
        'director': director,  # 负责人
        'isEnabled': isEnabled,  # 部门状态
        'parentId': parentId,  # 上级部门
        'phone': phone,  # 手机号
        'remark': "测试",  # 备注
        'sort': sort  # 排序
    }
    response = request.post_body('/api/1.0/department/create', body=body)
    return response
