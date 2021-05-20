# -*- coding: utf-8 -*-
# @Time : 2021/5/19 5:05 下午 
# @Author : lsj
# @File : abb.py
data = [{'url': 'ww.saa', 'request_type': 'post', 'title': '测试1', 'case': "{'id':3}", 'expected': '准确'},
        {'url': 'ww.saa', 'request_type': 'post', 'title': '测试2', 'case': "{'id':4}", 'expected': '准确'},
        {'url': 'aa', 'request_type': 'get', 'title': '测试3', 'case': "{'name':'hello'}", 'expected': '错误'}]

caseList = []
#
for dict in data:
    if 'ww.saa' in dict.values():
        a = (dict['url'] + ',' + str(dict['title']) + ',' + dict['case'] + ',' + dict['expected'])
        # print(a)
        b = a.split(",")
        c = tuple(b)
        # print(c)
        caseList.append(c)
# print(caseList)
#
# vaList = []
# for dict1 in data:
#     value = dict1['url']
#     if value not in vaList:
#         vaList.append(value)
# print(vaList)

# vaList = ['ww.saa', 'aa']
# for dict in data:
#     for j in vaList:
#         if j in dict.values():
#             a = (dict['url'] + ',' + str(dict['title']) + ',' + dict['case'] + ',' + dict['expected'])
#             # print(a)
#             b = a.split(",")
#             c = tuple(b)
#             # print(c)
#             caseList.append(c)
#     print(caseList)

a = "{'goodsId': None}"
# b = eval(a[2])
a.replace("\"", "")
# print(type(b))
print(a)