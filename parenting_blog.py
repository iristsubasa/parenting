#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import lxml
import requests as r
from bs4 import BeautifulSoup
def pa_store(data):
    with open('parenting_blog.json', 'a') as f:
        f.write(data)
#部落格內文文章
for x in range(58, 5000):
    try:
        URL = "http://best.parenting.com.tw/blogger_article.php?w={}".format(x)
        res = r.get(URL)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "lxml")

        classall = soup.select_one('div.breadCrumb').text  # 親子天下類別
        class1 = classall.split('>')[2]
        #判斷類別為"玩●生活"
        str_class1="玩●生活"
        if class1.__contains__(str_class1) :
            class2 = classall.split('>')[3]
            str_class2=["旅遊","親子餐廳","時事／生活"]
            for x in range(0, len(str_class2)):
                # 判斷類別為"旅遊","親子餐廳","時事／生活"
                if class2.__contains__(str_class2[x]):
                    name = soup.select_one('h3').text  # 餐廳名稱
                    content = soup.select_one('div.editor').text
                    content = content.replace('\n', '').replace('\t', '')
                    address = content.split('：')[2].split('電話')[0]  # 餐廳地址
                    phone = content.split('：')[3]  # 餐廳電話
                    phone = phone[0:12]
                    phone_num ="0"
                    if phone.__contains__(phone_num):
                        phone=phone
                    else:
                        phone=""
                    date = soup.select_one('div.views').text
                    date1 = date[-11:-1]  # po文日期
                    date1 = date1.replace('/', '-')
                    tags = soup.select_one('p.tag').text.replace('\n', '').replace(' ', ',')
                    resp = soup.select_one('div.views').text.split('：')[1].split('/')[0]
                    resp1 = resp[0:(len(resp) - 4)]
                    area_a = ["台北", "桃園", "新竹", "苗栗", "台中", "嘉義", "台南", "雲林", "高雄", "屏東", "台東", "花蓮", "宜蘭","彰化"]
                    for x in range(0, len(area_a)):
                        if content.__contains__(area_a[x]):
                            area = area_a[x]
                    parenting = {
                        '01_url': URL,
                        '02_name': name,
                        '03_address': address,
                        '04_phone': phone,
                        '05_date': date1,
                        '06_content': content,
                        '07_tags': tags,
                        '08_resp': resp1,
                        "11_area": area,
                        '9_class1': class1,
                        '10_class2': class2,
                    }
                    json_data = json.dumps(parenting, open('parenting_blog.json', 'a'), ensure_ascii=False, indent=4,sort_keys=True) + ','
                    pa_store(json_data)
                else:
                    continue
    except Exception as e:
        print e