# -*- coding: utf-8 -*-
# @Date    : 2018-01-16 20:17:35
# @Author  : mz (https://github.com/MjSeven)
# @Link    : ${}
# @Version : $Id$

import os
import sys
import time

import requests
from bs4 import BeautifulSoup as bs
from PIL import Image

reload(sys)
sys.setdefaultencoding('utf-8')

pic_folder = "xxx/Python Code/biying"
video_folder = "xxx/Python Code/biying"
info_loc = "xxx/Python Code/biying/img_urls.txt"

bing_url = ("http://bing.com/HPImageArchive.aspx?"
"format=js&idx=0&n=1&nc=1439260838289&pid=hp&video=1")

ISTIMEFORMAT = '%Y-%m-%d'
ti = time.strftime(ISTIMEFORMAT, time.localtime())

def get_request(url, stream=None):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    if stream:
        result = requests.get(url,headers=headers, stream=True)
        return result
    result = requests.get(url,headers=headers)
    print (result.text)
    return result.json()

def build_url(base_url, url):
    return base_url + url

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

def info_in_file(url):
    info_text = get_pic_info()
    with open(info_loc, 'a') as info_file:
        info_file.write('\n' + url + '\n')
        info_file.write(info_text + ti)
    print ('The info is OK!')

def is_have_file(img_file):
    if os.path.isfile(img_file):
        return True
    return False

def show_image(img_file):
    img = Image.open(img_file)
    img.show()

def get_pic():
    content = get_request(bing_url)
    if 'images' in content:
        pic_short_url = content['images'][0]['url']
        pic_name = pic_short_url.split('/')[-1]
        pic_full_url = 'https://www.bing.com{}'.format(pic_short_url)
        print (pic_full_url)
        # video_url = content['images'][0]['vid']['sources']
        # if video_url[0]:
        #     #print video_url[0][2]
        #     video_url = 'http:'+ video_url[0][2]
        #     #print video_url
        #     video_file = pic_folder + '' + ti + video_url.split('/')[-1]
        #     if is_have_file(video_file):
        #         print 'The {} is already exists!'.format(video_file)
        #     else:
        #         r = requests.get(video_url)
        #         with open(video_file, 'wb') as f:
        #             f.write(r.content)
        #    print 'The video is Ok!'
        pic_file = pic_folder + '/' + ti + pic_name
        print (pic_file)
        if is_have_file(pic_file):
            print ('The {} is already exists!'.format(pic_name))
        else:
            img_src = get_request(pic_full_url, True)
            with open(pic_file, 'wb') as f:
                f.write(img_src.content)
            print ('The {} is OK!'.format(pic_name))
            info_in_file(pic_full_url)
        show_image(pic_file)
        time.sleep(2)

if __name__ == '__main__':
    get_pic()
