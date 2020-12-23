# __author:"zonglr"
# date:2020/5/23
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

import requests, urllib3
from test_config import param_config
from common import logger

urllib3.disable_warnings()
log = logger.Log()
api_url = param_config.api_url
loginName = param_config.loginName
loginPassword = param_config.loginPassword

headers = {}


def login(loginName, loginPassword, platform='TEST'):
    global headers
    payload = {
        'loginPassword': loginPassword,
        'loginName': loginName,
        'platform': platform
    }
    r = requests.post(api_url + '/auth/login', json=payload, verify=False)
    assert r.status_code == 200
    if r.json()['msg'] == '请求成功':
        token = r.headers['X-AUTH-TOKEN']
        # headers
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-TOKEN': token
        }
        return headers
    else:
        log.info(r.json())
        return r.json()


login(loginName, loginPassword)
