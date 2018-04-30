# _*_ coding:utf-8 _*_
import json
import requests
from datetime import datetime


"""
功能：查看当前电影票房
输出格式：
电影名称 实时票房：xxx 累计票房：xxx 上映天数：xxx
此接口默认返回 20 条数据
改进点：
异常处理，格式处理
"""
# headers 建议更全一些,里面的 cookie 每次应该会变
"""
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
{'Content-Length': '27', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding': 'gzip, deflate', 'DNT': '1', 'Connection': 'keep-alive', 'X-Requested-With': 'XMLHttpRequest',
'Accept': 'application/json, text/javascript, */*; q=0.01',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
'Cookie': 'access_log=a067f011b0fd0e08d2923ef6294420ea; channel=zhifang_index%7C%7Ct10_xa_pc; areaCode=1000010000; Hm_lvt_a028c07bf31ffce4b2d21dd85b0b8907=1524989875; Hm_lpvt_a028c07bf31ffce4b2d21dd85b0b8907=1524989875; domainUrl=xa; flag=100; gpsGot=0; channel_webapp=webapp; BAIDUID=FB6C0A702631A6240C9D9B239FD6F83F:FG=1',
'Referer': 'http://dianying.nuomi.com/movie/boxoffice', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
"""

url = 'http://dianying.nuomi.com/movie/boxrefresh'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}

def get_detail(url, data):
    r = requests.post(url, data=data, headers=headers)
    content = json.loads(r.text)
    movie_list = content['real']['data']['detail']

    for movie in movie_list:
        movie_name = movie['movieName']
        all_box_office = movie['attribute']['2']['attrValue']
        cur_box_office  = movie['attribute']['3']['attrValue']
        up_days = movie['attribute']['1']['attrValue']
        print movie_name, u"实时票房:",cur_box_office, u"累计票房:", all_box_office,
        print u"上映天数:",up_days


if __name__ == '__main__':
    dt = datetime.now()
    date = '-'.join([str(dt.year), str(dt.month), str(dt.day)])
    data = {'isAjax': 'true', 'date':date}
    get_detail(url, data)
