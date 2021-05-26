# coding=gbk
import collections
import os
import yaml, time, pprint


# from common import request


class timeid():
    def __init__(self, file_yaml='config.yaml'):
        current_path = os.path.dirname(__file__)
        self.yaml_path = os.path.join(current_path, file_yaml)
        time_now = time.time()
        self.my_time = int(time_now * 1000)
        timeArray = time.localtime(time_now)
        self.otherStyleTime = time.strftime("%m%d", timeArray)

    # 读取
    def _get_yaml_element_info(self):
        file = open(self.yaml_path, 'r', encoding="utf-8")
        file_data = file.read()
        file.close()
        # 指定Loader
        data = yaml.load(file_data, Loader=yaml.FullLoader)
        return data

    # 写入
    def _set_yaml_time(self, data, type='w'):
        file = open(self.yaml_path, type, encoding='utf-8')
        yaml.dump(data, file, allow_unicode=True)
        file.close()

    # 获取之间id
    def id(self):
        time_data = self._get_yaml_element_info()
        time_data['goods']['id'] += 1
        if self.otherStyleTime == time_data['time']:
            time_data['id'] += 1
            self._set_yaml_time(time_data)
        else:
            time_data['id'] = 0
            time_data['time'] = self.otherStyleTime
            self._set_yaml_time(time_data)

        department_name = []
        code = []
        for i in time_data['department_list']:
            department_name.append(time_data['testname'] + time_data['time'] + str(time_data['id']) + str(i))
            code.append(time_data['time'] + str(time_data['id']) + str(i))
        return {
            # 中心库唯一id
            'core_code': time_data['time'] + str(time_data['id']),
            # 一级科室名字
            'departmentname': time_data['testname'] + time_data['time'] + '-' + str(time_data['id']),
            # 二级科室名字
            'department_name': department_name,
            'code': code,
            'goodsname': {
                'low': time_data['goods']['name']['low'] + time_data['time'] + str(time_data['id']),
                'low1': time_data['goods']['name']['low1'] + time_data['time'] + str(time_data['id']),
                'high': time_data['goods']['name']['high'] + time_data['time'] + str(time_data['id']),
                'lowbag': time_data['goods']['name']['lowbag'] + time_data['time'] + str(time_data['id']),
                'pkg': time_data['goods']['name']['pkg'] + time_data['time'] + str(time_data['id']),
            }
        }

    def body_data(self):
        return collections.defaultdict()

    def _get_body(self, path):
        body = eval(str(body_data[path].copy()))
        return body

    def _body_replace(self, body, data):
        # 如果想要参数化变量，在用到方法的时候 加eval（data）
        if type(data) is not dict:
            data = eval(data)
        for i in body.keys():
            if type(body[i]) is str:
                pass
            elif type(body[i]) is dict:
                self._body_replace(body[i], data)
            elif type(body[i]) is list:
                for j in body[i]:
                    if type(j) is dict:
                        self._body_replace(j, data)

            if i in data.keys():
                body[i] = data[i]
        return body


body_data = timeid().body_data()

# elements=ElementdataYamlUtils().get_yaml_element_info(yaml_path)

if __name__ == '__main__':
    body = {
        "toolsDetailUiBeans": [{
            "kitTemplateId": 23,
            "quantity": 1,
            "supplierId": 3
        }],
        "goodsDetailUiBeans": [{
            "goodsId": 294,
            "quantity": 1,
            "supplierId": 8
        }],
        "orderUiBean": {
            "hospitalName": "\u6d4b\u8bd5\u533b\u9662",
            "procedureSite": [95],
            "surgeon": "\u4e3b\u5200\u533b\u751f",
            "procedureTime": 1621423780357,
            "expectReturnTime": 1621785600000,
            "contactName": "\u8ba2\u5355\u8054\u7cfb\u4eba",
            "contactPhone": "13333333333",
            "manufacturerId": 1,
            "salesPerson": "\u9500\u552e\u4eba\u5458",
            "gender": "FEMALE",
            "ageGroup": "TEENAGERS",
            "deliveryMode": "SELF_PIKE_UP",
            "payOnDelivery": True,
            "receivingName": "\u6536\u4ef6\u4eba",
            "consignorName": "\u63d0\u8d27\u4eba",
            "consignorPhone": "13212345567",
            "receivingIdCard": "421322199811044619",
            "powerOfAttorney": "http://192.168.10.254:9191/server/file/2021/05/17/5b15b54d-de1f-4aab-ab5b-ffe6bc5a6998/base64Test.jpg",
            "addressId": 305,
            "supplierId": 1
        }
    }
    case = {'goodsId': None}
    a = timeid()._body_replace(body, case)
    print(a)
