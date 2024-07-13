#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os, sys ,time ,lxml ,json
reload(sys)
sys.setdefaultencoding('utf-8')
import requests as r
from bs4 import BeautifulSoup
def pa_store(data):
    with open('parenting_url.json', 'a') as f:
        f.write(data)

with open('urls', 'r') as f:
    for url in f:
        try:
            res = r.get(url)
            soup = BeautifulSoup(res.text, "lxml")
            name = soup.select_one('h1').text
            subtitle = soup.select_one('h2').text

            time1 = soup.find('meta', {'itemprop':"datePublished"})
            time =time1["content"][0:10]
            tags = soup.select_one('.tagWrap').text.replace('\n', '').replace('、',",").replace(" ",",")
            p = soup.select_one('.pagination').text.split('下一頁')[0][-1]
            #判斷內文頁數，文章相加
            content=""
            address=""
            phone=""
            area=""
            for x in range(1,int(p)):
                addurl = (url.replace('\n', ''))+"?page={}".format(x)
                res = r.get(addurl)
                soup = BeautifulSoup(res.text, "lxml")
                c1 = soup.select_one('.articleContent').text.replace('\n', '').replace('\t', '')
                content = content + c1
            content1 = content
            address_a = ["地點：", "地址："]
            phone_a= "電話："
            area_a=["台北","桃園","新竹","苗栗","台中","嘉義","台南","雲林","高雄","屏東","台東","花蓮","宜蘭"]
            for x in range(0,len(address_a)):
                if content1.__contains__(address_a[x]):
                    address = content1.split(address_a[x])[1].split(" ")[0]
            for x in range(0,len(area_a)):
                if content1.__contains__(area_a[x]):
                    area = area_a[x]
            if content1.__contains__(phone_a) :
                phone=content1.split(phone_a)[1].replace(" ","")[0:12]
            parenting = {
                '01_url': url,
                '02_name': name,
                '03_address': address,
                '04_phone': phone,
                '05_date': time,
                '06_content': content,
                '07_tags': tags,
                "08_area":area,
            }
            json_data = json.dumps(parenting, open('parenting_url.json', 'a'), ensure_ascii=False, indent=4,sort_keys=True) + ','
            pa_store(json_data)
            time.sleep(1)
        except Exception as e:
            print e