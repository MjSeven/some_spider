#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-19 19:36:17
# @Author  : mz (https://github.com/MjSeven)
# @Link    : ${link}
# @Version : $Id$

import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

text = open('lmy.txt').read()
# 分词并且去重
final_word_list = []
wordlist = list(jieba.cut(text, cut_all=True))
for word in wordlist:
    final_word_list.append(word)
final_word_list = set(final_word_list)
final_word = ''
for word in final_word_list:
    final_word = final_word + ' ' + word
# 设置词云形状的图片 
test_color = np.array(Image.open('3.jpg'))

# 分词后的内容 构造词云
my_wordcloud = WordCloud(
    background_color='black', font_path='msyh.ttf',
    mask=test_color, max_font_size=100).generate(final_word)
plt.imshow(my_wordcloud)
# 不显示 x y 轴
plt.axis("off")
plt.savefig('huba1.jpg', dpi=1000)
plt.show()
