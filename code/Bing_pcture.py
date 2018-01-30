# /usr/bin/env python
# coding:--utf-8--

import urllib
import urllib2
from bs4 import BeautifulSoup as bs
from datetime import datetime


page = 57
pic_folder = r"C:/Users/Mj/Desktop"
id = 1
num = 1
start = datetime.now()
print "start at:  ", start
while page > 0:
    #   打开包含所有图片的网址
    root_url = root_url = "http://bing.plmeizi.com/?page=" + str(page)
    response = urllib2.Request(root_url)
    content = urllib2.urlopen(response)
    content = content.read()

    # 第一次解析，获得图片详情页
    origin = bs(content, 'lxml')
    pic_urls = origin.find_all("a", attrs={"class": "item"})

    for pic_url in pic_urls:
        img_url = pic_url.get("href")

        # 打开图片详情页
        img_view = urllib2.Request(img_url)
        img_view = urllib2.urlopen(img_view)
        img_view = img_view.read()

        # 解析详情页，获得图片真实网址
        data = bs(img_view, 'lxml')

        urls = data.select("#picurl")  # 通过id查找包含图片网址的内容

        for url in urls:
            real_url = url["href"]

        name = real_url.split("/")[-1]  # 获得网址中关于图片的描述

        img_name = pic_folder + "/" + name

        # 打开只包含图片的网址
        img_data = urllib.urlopen(real_url)
        img = img_data.read()

        # 保存图片
        try:
            file = open(img_name, "wb")
        except IOError as e:
            print "第 %d 张图片无法保存.\n" % id
            id = id + 1
            continue

        file.write(img)
        print "第 %d 张图片保存完毕.\n" % num
        num = num + 1
        file.close()

    page = page - 1

end = datetime.now()

print "保存了 %d 张图片, %d 张图片无法保存。\n" % (num, id)
print "总共耗时:", end - start
