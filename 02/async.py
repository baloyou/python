#!/usr/bin/python3
# -*- coding: utf-8 -*-

import asyncio
import time

@asyncio.coroutine
def hello():
    print('hello world')
    #使用了基于异步IO实现的 sleep，协程能够并行处理
    r = yield from asyncio.sleep(2)
    #使用同步IO的 sleep，会导致协程失效
    #time.sleep(2)
    print('hello again')

loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
