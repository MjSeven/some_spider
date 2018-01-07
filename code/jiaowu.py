    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-07 19:36:42
# @Author  : mz (yuchenmj@163.com)
# @Link    : ${link}
# @Version : $Id$

import requests
from PIL import Image
from bs4 import BeautifulSoup as bs

s = requests.session()
url = 'http://222.24.62.120/default2.aspx'

user_agent = "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/57.0"
headers = {"User_Agent": user_agent}


def get_index_html(stu_number, passwd):
    response = s.get(url)
    index = bs(response.content, 'lxml')
    __VIEWSTATE = index.find("input").get("value")

    # 获取验证码，将验证码 down 下来然后手工输入
    img_url = "http://222.24.62.120/CheckCode.aspx"
    img_response = s.get(img_url, stream=True)

    img = img_response.content
    with open("ver.png", "wb") as f:
        f.write(img)
    im = Image.open("ver.png")
    im.show()

    code = raw_input("验证码是：")
    # 构建 post 数据，登入网站
    data = {
        "__VIEWSTATE": __VIEWSTATE,
        "txtUsername": stu_number,
        "TextBox2": passwd,
        "txtSecretCode": code,
        "Button1": "",
    }

    index_html = s.post(url, data=data, headers=headers)

    content = index_html.content.decode("gb2312")

    info_html = bs(content, "lxml")

    name = info_html.find("span", id="xhxm")
    print "欢迎您:", name.get_text()


def get_score(stu_number):
    post_data = {
        "btn_xq": "%D1%A7%C6%DA%B3%C9%BC%A8",
        "ddlXN": "2017-2018",
        "ddlXQ": "1",
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "",
        "hidLanguage": "",
        "ddl_kcxz": "",
    }
    global headers
    headers["Referer"] = "http://222.24.62.120/xscjcx.aspx?xh="\
        + str(stu_number) + "&xm=%C2%ED%D5%F0&gnmkdm=N121605"

    score_url = "http://222.24.62.120/xscjcx.aspx?xh="\
        + str(stu_number) + "&xm=%C2%ED%D5%F0&gnmkdm=N121605"

    get_score = s.get(score_url, headers=headers).content
    get_score = get_score.decode("gb2312")
    # 将获取到的框架源代码保存下来，方便提取__EVENTARGUMENT和__VIEWSTATE值后作为post内容进行下一步
    # with open("socre.html", "wb") as score_file:
    #     score_file.write(get_scorce)
    post_info = bs(get_score, "lxml")
    infos = post_info.find_all("input")[:3]
    post_data["__EVENTTARGET"] = infos[0].get("value")
    post_data["__EVENTARGUMENT"] = infos[1].get("value")
    post_data["__VIEWSTATE"] = infos[2].get("value")

    real_score = s.post(score_url, data=post_data, headers=headers).content

    # 得到真正的包含成绩的页面，之后就可以提取成绩了
    # with open("real_score.html", "wb") as real:
    #     real.write(real_score)
    real_score = real_score.decode("gb2312")

    real = bs(real_score, "lxml")
    # 查找成绩并显示
    one = real.find_all("table", class_="datelist")
    # print one[-1].get_text()
    tab = one[0]
    trs = tab.find_all("tr")
    for tr in trs:
        for td in tr.find_all("td"):
            print td.get_text().strip(), "  ",
        print


if __name__ == '__main__':
    stu_number = raw_input("请输入学号:")
    passwd = raw_input("请输入密码:")
    get_index_html(stu_number, passwd)
    get_score(stu_number)
