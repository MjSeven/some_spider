#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-16 20:17:35
# @Author  : mz (https://github.com/MjSeven)
# @Link    : ${link}
# @Version : $Id$

import os
import sys
import time
import json
import requests
from PIL import Image
from bs4 import BeautifulSoup as bs

reload(sys)
sys.setdefaultencoding('utf-8')

ISTIMEFORMAT = '%Y-%m-%d'

ti = time.strftime(ISTIMEFORMAT, time.localtime())

pic_folder = "F:/Python Code/biying"
video_folder = "F:/Python Code/biying"
img_urls = "F:/Python Code/biying/img_urls.txt"


def get_pic_info():
    # 获取图片介绍
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


def get_pic():
    bing_url = "http://bing.com/HPImageArchive.aspx?\
format=js&idx=0&n=1&nc=1439260838289&pid=hp&video=1"
    content = requests.get(bing_url)
    result = json.loads(content.text)

    wallpaper_url = result['images'][0]['url']
    pic_name = wallpaper_url.split('/')[-1]
    if wallpaper_url.find('http') < 0:
        # 存在图片网址，并将网址以及图片介绍写入 txt
        wallpaper_url = "http://www.bing.com/" + wallpaper_url
        # print wallpaper_url
        info_text = get_pic_info()
        with open(img_urls, "a") as img_urls_file:
            img_urls_file.write('\n' + wallpaper_url + '\n')
            img_urls_file.write(info_text + ti)
    img_src = requests.get(wallpaper_url, stream=True)

    img_file = pic_folder + "/" + ti + pic_name

    # 判断图片存在并保存
    if os.path.isfile(img_file):
        print "The picture is already exists!"
    else:
        with open(img_file, 'wb') as f:
            f.write(img_src.content)
        print 'The picture is Ok'
    # 显示图片
    img = Image.open(img_file)
    img.show()
    return result


def tryDownloadVideo(result):
    # 下载视频
    vid = result['images'][0]
    if 'vid' in vid.keys():
        src = vid['vid']['sources'][1]
        video_url = src[2]
        if not video_url:
            return False

        video_url = video_url.replace('\\', '')
        video_name = video_url.split('/')[-1]

        if video_url.find('http') > 0:
            video_src = requests.get(video_url).content()
        else:
            video_src = requests.get('http:' + video_url).content()

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


if __name__ == '__main__':
    result = get_pic()
    tryDownloadVideo(result)
