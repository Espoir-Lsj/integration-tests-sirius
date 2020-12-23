# __author:"zonglr"
# date:2020/12/11
#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import random
import math


def generate_random_gps(base_log=None, base_lat=None, radius=None):
    radius_in_degrees = radius / 111300
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)
    longitude = y + base_log
    latitude = x + base_lat
    # 这里是想保留6位小数点
    lat = '%.6f' % latitude
    lng = '%.6f' % longitude
    return lat, lng


lat, lng = generate_random_gps(base_log=120.7, base_lat=30, radius=1000000)