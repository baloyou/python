#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
import sys



argv = sys.argv

url = 'http://www.douban.com'

if (len(argv)>1):
    url = argv[1]

request = urllib.request.Request(url)

response = urllib.request.urlopen(request)

data = response.read()

print(data)
