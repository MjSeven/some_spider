#! /usr/bin/env python
# coding=utf-8

import urllib
import json
import os
import time
import requests
from bs4 import BeautifulSoup as bs
from PIL import Image
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

ISOTIMEFORMAT = '%Y-%m-%d'

ti = time.strftime(ISOTIMEFORMAT, time.localtime())
# print ti

# print time.time()
# print time.ctime()

pic_folder = "F:/Python Code/biying"
video_folder = "F:/Python Code/biying"
img_urls = "F:/Python Code/biying/img_urls.txt"
bing_url = "http://bing.com/HPImageArchive.aspx?\
format=js&idx=0&n=1&nc=1439260838289&pid=hp&video=1"


def tryDownloadVideo(result):
    vid = result['images'][0]
    if 'vid' in vid.keys():
        src = vid['vid']['sources'][1]
        video_url = src[2]
        if not video_url:
            return False

        video_url = video_url.replace('\\', '')
        video_name = video_url.split('/')[-1]

        if video_url.find('http') > 0:
            video_src = urllib.urlopen(video_url).read()
        else:
            video_src = urllib.urlopen('http:' + video_url).read()

        video_file = video_folder + '/' + ti + video_name

        if os.path.isfile(video_file):
            return "The video is already exists!"
        else:
            print "The video is downloading now..."
            with open(video_file, 'wb') as f:
                f.write(video_src)
            with open(img_urls, "a") as img_urls_file:
                img_urls_file.write("\n")
                img_urls_file.write(video_url)
                img_urls_file.write("\n")
            return 'The video is ok!'
    return "There is no video to download!"


def get_pic_info():
    '''获取图片的详细信息'''
    req = requests.get('http://cn.bing.com/')
    ig = req.text.split('IG:"')[1].split('"')[0]
    # print ig
    data = {
        'ensearch': '0', 'IID': 'SERP.5044', 'IG': ig
    }
    zeq = requests.get('http://cn.bing.com/cnhp/life', data)
    # with open("biying2.html", "wb") as f:
    #     f.write(z.text)

    html = bs(zeq.text, "lxml")
    info = html.find("div", id="hplaSnippet")
    return info.string.strip()


# 未联网的情况下等待
times = 10
waitSeconds = 15
i = 0
if_connected = False
try:
    urllib.urlopen("http://www.baidu.com")
    if_connected = True
except KeyboardInterrupt:
    if_connected = False
while not if_connected:
    i = i + 1
    print "You seems don't connect the Internet,\
     now is the " + str(i) + " time "
    time.sleep(waitSeconds)
    try:
        urllib.urlopen("http://www.baidu.com")
        if_connected = True
    except KeyboardInterrupt:
        if_connected = False
    if i == times:
        print "Long time can not connect the Internet, it's over!"
        exit()


content = urllib.urlopen(bing_url).read().decode('utf-8')
result = json.loads(content)

wallpaper_url = result['images'][0]['url']
# print wallpaper_url
pic_name = wallpaper_url.split('/')[-1]
# print pic_name
if wallpaper_url.find('http') < 0:
    wallpaper_url = "http://www.bing.com/" + wallpaper_url
    # print wallpaper_url
    info_text = get_pic_info()
    with open(img_urls, "a") as img_urls_file:
        img_urls_file.write("\n")
        img_urls_file.write(wallpaper_url)
        img_urls_file.write("\n")
        img_urls_file.write(info_text)
        img_urls_file.write(ti)
img_src = urllib.urlopen(wallpaper_url).read()

img_file = pic_folder + "/" + ti + pic_name

if os.path.isfile(img_file):
    print "The picture is already exists!"
else:
    with open(img_file, 'wb') as f:
        f.write(img_src)
    print 'The picture is Ok'

# 显示图片
img = Image.open(img_file)
img.show()

print tryDownloadVideo(result)

print "Ok,all work has done!"
