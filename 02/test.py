#!/usr/bin/python3
# -*- coding: utf-8 *-*

import asyncio
import time
from aiohttp import web

async def index(request):
    #await asyncio.sleep(1)
    return web.Response(
            body=b'<h1>Index</h1>',
            status=200,
            content_type='text/html',
            charset='utf-8'
            )

async def hello(request):
    #await asyncio.sleep(5)
    text = '<h1>hello , %s!</h1>' % request.match_info['name']
    return web.Response(
            body=text.encode('utf-8'),
            status=200,
            content_type='text/html',
            charset='utf-8'
            )

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    srv = await loop.create_server(app.make_handler(), '0.0.0.0', 81)
    print('server start')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
