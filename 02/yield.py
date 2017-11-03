#!/usr/bin/python3
# -*- coding: utf-8 -*-

def c():
    r = 1
    while True:
        n = yield r
        print("n: %s" % n)
        r=r+1

c = c()
# 首次执行，打印r的原始值
print("next %d" % next(c))
# 将1 赋给 n 然后执行后续代码，直到下次yield
print("send %d" % c.send(1))
# 从yield的下一行开始执行，并且n无值
print("next %d" % next(c))

print("send %d" % c.send(1))
print("next %d" % next(c))
print("send %d" % c.send(1))
