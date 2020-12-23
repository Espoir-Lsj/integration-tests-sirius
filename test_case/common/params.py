# __author:"zonglr"
# date:2020/6/23
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import itertools


def params(json):
    params = json
    alllist = []
    n = 0
    while n < len(params):
        n = n + 1
        lists = list(itertools.combinations(params, n))
        for i in lists:
            dic = {}
            for j in i:
                value = params[j]
                dic.setdefault(j, value)
            alllist.append(dic)
    print(alllist)
    return alllist
