# -*- coding: utf-8 -*-
# @Time : 2021/7/2 10:26 上午 
# @Author : lsj
# @File : QRs.py
import qrcode, os


def make_qr(name):
    path = os.path.join(os.path.dirname(__file__))

    for x in name:
        img = qrcode.make(x)
        with open('%s/%s.png' % (path, x), 'wb') as f:
            img.save(f)


make_qr(['a', 'b', 'c'])
