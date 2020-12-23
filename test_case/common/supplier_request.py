# __author:"zonglr"
# date:2020/6/10
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import requests, json, urllib3
from test_config import param_config
from common import logger

urllib3.disable_warnings()
log = logger.Log()

api_url = param_config.api_url
loginName = param_config.supplierLoginName
loginPassword = param_config.supplierLoginPassword


def login(loginName, loginPassword, platform='TEST'):
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


# 供应商帐号登录
headers = login(loginName, loginPassword)


def get_params(path, params):
    r = requests.get(api_url + path, headers=headers, params=params, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    return response


def get(path):
    r = requests.get(api_url + path, headers=headers, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    return response


def post_body(path, body):
    r = requests.post(api_url + path, headers=headers, json=body, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    return response


def post_params(path, params):
    r = requests.post(api_url + path, headers=headers, params=params, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    return response


def post(path):
    r = requests.post(api_url + path, headers=headers, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    return response


def delete_body(path, body):
    r = requests.delete(api_url + path, headers=headers, data=json.dumps(body), verify=False)
    response = r.json()
    assert (r.status_code == 200)
    return response


def delete_params(path, params):
    r = requests.delete(api_url + path, headers=headers, params=params, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    return response


def delete(path):
    r = requests.delete(api_url + path, headers=headers, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    return response


def put_body(path, body):
    r = requests.put(api_url + path, headers=headers, data=json.dumps(body), verify=False)
    response = r.json()
    assert (r.status_code == 200)
    return response


def put(path):
    r = requests.put(api_url + path, headers=headers, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    return response
