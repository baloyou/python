#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'wl'

import asyncio, logging
import aiomysql

def log(sql, args=()):
    logging.info('SQL: %s' % sql)


async def create_pool(loop, **kw):
    """
    创建数据库连接池
    """
    logging.info('create database connection pool...')
    global __pool
    """ 
    __pool = await aiomysql.create_pool(
        host = kw.get('host', 'localhost'),
        port = kw.get('port', 3306),
        user = kw.get('user', 'root'),
        password = kw.get('password', 'test1123456'),
        db = kw.get('db', 'python'),
        charset = kw.get('charset', 'utf-8'),
        autocommit = kw.get('autocommit', True),
        maxsize = kw.get('maxsize', 10),
        minsize = kw.get('minsize', 1),
        loop=loop
    )
    """
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )
    

async def select(sql, args, size=None):
    """
    执行 SELECT 查询
    """
    log(sql, args)
    global __pool
    with (await __pool) as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?', '%s'), args or ())
        # rs 应该是一个字典的数据类型
        if size:
            rs = await cur.fecthmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        logging.info('rows returned: %s' % len(rs))
        return rs

async def execute(sql, args):
    log(sql)
    global __pool
    with (await __pool) as conn:
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount
            await cur.close()
        except BaseException as e:
            raise
        return affected

async def init(loop):
    global __pool
    await create_pool(loop=loop,user='root', password='test123456',db='python')
    rows = await select('select * from test',[])
    print(rows)
    with (await __pool) as conn:
        conn.close()
    logging.info('test ...')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    #loop.run_forever()


