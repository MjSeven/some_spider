#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-19 14:26:42
# @Author  : mz (https://github.com/MjSeven)
# @Link    : ${link}
# @Version : $Id$

import time
import requests
from bs4 import BeautifulSoup as bs

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
cookie = '自己的 cookie'
headers = {
    'User-Agent': user_agent,
    'Cookie': cookie
}
f = open('lmy.txt', 'ab')
page = 1
while page < 8:
    url = 'https://weibo.cn/u/' + '微博 id' + '?page=' + str(page)
    html = requests.get(url=url, headers=headers).content
    x = bs(html, 'lxml')
    print x.title
    contents = x.find_all(class_='ctt')

    for content in contents:
        word = content.get_text()
        f.write(word.encode('utf-8'))
    page += 1
    time.sleep(1)
f.close()
