#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os, sys ,time ,lxml ,json
reload(sys)
sys.setdefaultencoding('utf-8')
import requests as r
from bs4 import BeautifulSoup
## 1.讀取https://yukiblog.tw/category/special-topic/family-restaurant/page/1~11親子餐廳頁面，擷取blog內文的urls
yukiblog_urls = []
yukiblog_list = []
for x in range(1,12):
    url="https://yukiblog.tw/category/special-topic/family-restaurant/page/{}".format(x)
    res = r.get (url)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "lxml")
    for p in range(1,10):
        urls = soup.select("article.blog-post")[p].select_one('h1').select_one('a')['href']
        yukiblog_urls.append(urls)
# print yukiblog_urls
# print len(yukiblog_urls)
# print yukiblog_urls[0]
## 2.擷取urls裡面的內文
for y in range(0,len(yukiblog_urls)-1):
    try:
        url_a = yukiblog_urls[y]
        print url_a
        res_a = r.get(url_a)
        soup_a = BeautifulSoup(res_a.text, "lxml")
        yukiblog = {}
        yukiblog['url'] = url_a
        yukiblog['name'] = soup_a.select_one('h1').text
        yukiblog['date ']= soup_a.select_one('time').text
        yukiblog['tags ']= soup_a.select_one(".category").text.split('：')[1].replace(' ','')
        yukiblog['content ']= soup_a.select_one('article').text
        content_all =soup_a.select_one('article').text
        yukiblog['address']= content_all.split('地址：')[1].split(' ')[0]
        yukiblog['phone ']= content_all.split('電話：')[1].split(' ')[0]
        area = ""
        area_a=["台北","桃園","新竹","苗栗","台中","嘉義","台南","雲林","高雄","屏東","台東","花蓮","宜蘭","韓國","日本"]
        for x in range(0, len(area_a)):
            if content_all.__contains__(area_a[x]):
                yukiblog['area ']= area_a[x]
        yukiblog_list.append(yukiblog)
    except Exception as e:
        print e
yukiblog_f = json.dumps(yukiblog_list, ensure_ascii=False)
with open('yukiblog.json', 'w') as a:
    a.write(yukiblog_f.encode('utf-8'))
