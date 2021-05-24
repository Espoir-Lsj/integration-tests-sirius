
import requests, json
from test_config import param_config, yamlconfig
from test_case.common import login, logger

headers = login.headers
headers1 = login.headers1
api_url = param_config.api_url
log = logger.Log()


# 替换参数
def body_replace(url, data=None):
    body = yamlconfig.timeid()

    if data is None:
        return body._get_body(url)
    return body._body_replace(body._get_body(url), data)


def reValue_01(body, data):
    if type(data) is not dict:
        data = eval(data)
    for i in body.keys():
        if type(body[i]) is str:
            pass
        elif type(body[i]) is dict:
            reValue_01(body[i], data)
        elif type(body[i]) is list:
            for j in body[i]:
                if type(j) is dict:
                    reValue_01(j, data)
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
        log.info('----------请求成功---------- \n 请求地址：%s ' % path)
    return response


def get01(path):
    r = requests.get(api_url + path, headers=headers1, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s ' % path)
    return response


# 供应商
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
        yamlconfig.body_data.setdefault(path, body)
    return response


# 经销商
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
        yamlconfig.body_data.setdefault(path, body)
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
        yamlconfig.body_data.setdefault(path, body)
    return response


def put_body01(path, body):
    r = requests.put(api_url + path, headers=headers1, data=json.dumps(body), verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
        # yamlconfig.body_data.setdefault(path, body)
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
        yamlconfig.body_data.setdefault(path, body)
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
