#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os, sys ,time ,lxml
reload(sys)
sys.setdefaultencoding('utf-8')
import requests as r
from bs4 import BeautifulSoup
def url_store(data):
    with open('urls', 'a') as f:
        f.write(data)
URL="https://www.parenting.com.tw/subcategory/35-%E8%A6%AA%E5%AD%90%E9%81%8A/"
res = r.get (URL)
soup = BeautifulSoup(res.text, "lxml")
a = soup.select_one('.pagination').text.split('下一頁')[0][17:19]
for x in range(1,int(a)):
    URL="https://www.parenting.com.tw/subcategory/35-%E8%A6%AA%E5%AD%90%E9%81%8A/?page={}".format(x)
    res = r.get (URL)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "lxml")
    for y in soup.find_all('a',{"class":"txtLink"}):
        url = y['href']
        print url
        s = "https://www.parenting.com.tw/article/"
        if url.__contains__(s):
            url_store(url+'\n')
        else:
            print "not ariticle"
    time.sleep(1)