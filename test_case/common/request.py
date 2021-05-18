# __author:"zonglr"
# date:2020/6/10
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import requests, json
from test_config import param_config, yamlconfig
from common import login, logger

headers = login.headers
headers1 = login.headers
api_url = param_config.api_url
log = logger.Log()

request_data = yamlconfig.timeid(file_yaml='request_data.yaml')


# 替换参数
def reValue(body, data):
    for i in body.keys():
        if type(body[i]) is str:
            pass
        elif type(body[i]) is dict:
            reValue(body[i], data)
        elif type(body[i]) is list:
            for j in body[i]:
                if type(j) is dict:
                    reValue(j, data)
        if i in data.keys():
            body[i] = data[i]
    return body


def get_params(path, params):
    r = requests.get(api_url + path, headers=headers, params=params, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(params, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(params, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 传入参数：%s' % (path, json.dumps(params, ensure_ascii=False)))
    return response


def get(path):
    r = requests.get(api_url + path, headers=headers, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s ' % (path))
    return response


def post_body(path, body):
    r = requests.post(api_url + path, headers=headers, json=body, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
        if path not in request_data._get_yaml_element_info().keys():
            request_data._set_yaml_time({path: body}, 'a')
    return response


def post_body01(path, body):
    r = requests.post(api_url + path, headers=headers1, json=body, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
        if path not in request_data._get_yaml_element_info().keys():
            request_data._set_yaml_time({path: body}, 'a')
    return response


def post(path):
    r = requests.post(api_url + path, headers=headers, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    return response


def delete_body(path, body):
    r = requests.delete(api_url + path, headers=headers, data=json.dumps(body), verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    return response


def delete_params(path, params):
    r = requests.delete(api_url + path, headers=headers, params=params, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(params, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(params, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(params, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    return response


def delete(path):
    r = requests.delete(api_url + path, headers=headers, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    return response


def put_body(path, body):
    r = requests.put(api_url + path, headers=headers, data=json.dumps(body), verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
        if path not in request_data._get_yaml_element_info().keys():
            request_data._set_yaml_time({path: body}, 'a')
    return response


def put(path):
    r = requests.put(api_url + path, headers=headers, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))

    return response
