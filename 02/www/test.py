#!/usr/bin/python3
# -*- coding: utf-8 *-*

import asyncio
import time
from datetime import datetime
from aiohttp import web
import orm
async def index(request):
    #await asyncio.sleep(1)
    rows = await orm.select('select * from test', [])
    html = '<h1>Index</h1><table border=1><Tr><td>id</td><td>name</td></tr>'
    for row in rows:
        html = html + '<tr>'
        html = html + '<td>%s</td><td>%s</td>' % (row['id'], row['name'])

    return web.Response(
            body=html.encode('utf-8'),
            status=200,
            content_type='text/html',
            charset='utf-8'
            )

async def hello(request):
    #await asyncio.sleep(5)
    name = request.match_info['name']
    await orm.execute('insert into test (`name`) values (%s)', [name])
    text = '<h1>hello , %s!</h1>' % request.match_info['name']
    return web.Response(
            body=text.encode('utf-8'),
            status=200,
            content_type='text/html',
            charset='utf-8'
            )

async def init(loop):
    await orm.create_pool(loop=loop,user='root', password='test123456',db='python')
    #必须关闭数据库链接，否则会报 event loop is closed
    with (await orm.__pool ) as conn:
        conn.close()
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    srv = await loop.create_server(app.make_handler(), '0.0.0.0', 81)
    print('server start')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
