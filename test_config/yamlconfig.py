# coding=gbk
import collections
import os
import yaml, time, pprint


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


body_data = timeid().body_data()

# elements=ElementdataYamlUtils().get_yaml_element_info(yaml_path)

if __name__ == '__main__':
    # pprint.pprint(timeid().id())
    # timeid(file_yaml='request_data.yaml')._set_yaml_time({1:2},'a')
    # url = '/api/admin/goodsTypes/1.0/add'
    # pprint.pprint(timeid(file_yaml='request_data.yaml')._get_yaml_element_info()[url])
    timeid(file_yaml='request_data.yaml')._set_yaml_time({'url': 'body'}, 'w')
