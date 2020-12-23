# __author:"zonglr"
# date:2020/11/20
#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import func_timeout

@func_timeout.func_set_timeout(10)
def askChoice():
    return input('y/n:')

try:
    s = askChoice()
except func_timeout.exceptions.FunctionTimedOut as e:
    s = 'test'
