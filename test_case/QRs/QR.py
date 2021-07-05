# -*- coding: utf-8 -*-
# @Time : 2021/7/2 10:26 上午 
# @Author : lsj
# @File : QRs.py
import qrcode, os


def make_qr(name):
    path = os.path.join(os.path.dirname(__file__))
    num = name

    for x, y in zip(name, num):
        img = qrcode.make(x)
        with open('%s/%s.png' % (path, y), 'wb') as f:
            img.save(f)


make_qr(['a', 'b', 'c'])
