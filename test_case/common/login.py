# __author:"zonglr"
# date:2020/5/23
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

import requests, urllib3
from test_config import param_config
from test_case.common import logger

urllib3.disable_warnings()
log = logger.Log()
api_url = param_config.api_url
loginName = param_config.supplierLoginName
loginPassword = param_config.supplierLoginPassword

loginName1 = param_config.supplierLoginName02
loginPassword1 = param_config.supplierLoginPassword02

headers = {}
supplierId = None
dealerId = None
headers1 = {}


def login(loginName, loginPassword, platform='TEST'):
    global headers, dealerId
    payload = {
        'loginPassword': loginPassword,
        'loginName': loginName,
        'platform': platform
    }
    r = requests.post(api_url + '/auth/login', json=payload, verify=False)
    assert r.status_code == 200
    dealerId = r.json()['data']['companyId']
    if r.json()['msg'] == '请求成功':
        token = r.headers['X-AUTH-TOKEN']
        # headers
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-TOKEN': token
        }
        return dealerId, headers
    else:
        log.info(r.json())
        return r.json()


# 获取自身ID 经销商/供应商 ID    供应商id 供应商token
def get_supplierId(loginName, loginPassword, platform='TEST'):
    global supplierId, headers1
    payload = {
        'loginPassword': loginPassword,
        'loginName': loginName,
        'platform': platform
    }

    response = requests.post(api_url + '/auth/login', json=payload, verify=False)
    assert response.status_code == 200
    supplierId = response.json()['data']['companyId']

    if response.json()['msg'] == '请求成功':
        token = response.headers['X-AUTH-TOKEN']
        # headers
        headers1 = {
            'Content-Type': 'application/json',
            'X-AUTH-TOKEN': token
        }
        return supplierId, headers1


login(loginName, loginPassword)
# print(dealerId)
get_supplierId(loginName1, loginPassword1)
# print(supplierId)
