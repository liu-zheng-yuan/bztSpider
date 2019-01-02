import requests
import datetime
import time
from dbConnector import dbConnector
from bs4 import BeautifulSoup
from enum import Enum

# ?channel=xiaocong-channel&client=pc&cursor=1544592877&limit=50&first_page=false&accept_symbols=coin
# API分析 https://api-prod.wallstreetcn.com/apiv1/content/lives
# channel 怀疑是频道 必须有 保持
# client 登录端 保持？
# cursor 快讯的时间戳 可改 下次request要修改时间戳
# limit 一次返回的快讯数量
# first_page 是否首页
#
# conn = dbConnector.get_instance()
# url = "https://api-prod.wallstreetcn.com/apiv1/content/lives"
# params = {'channel': "xiaocong-channel", "client": "pc", 'cursor': 1545633094, 'limit': 50, 'first_page': 'false',
#           'accept_symbols': 'coin'}
# r = requests.get(url, params)
#
# rows = []
# patch_number = 50  # 一批插入的数量
# for i in range(50):
#     data = r.json()['data']['items'][i]
#     spider_source = "小葱"
#     title = data["title"]
#     content = data["content_text"]
#     pubtime = datetime.datetime.fromtimestamp(data['display_time']).strftime('%Y-%m-%d %H:%M:%S')  # 转成datetime 再转成字符串
#     savetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     source = "小葱快讯"
#     picture_urls = ",".join(data["image_uris"])
#     row = (spider_source, title, content, pubtime, savetime, source, picture_urls)
#     rows.append(row)
# rows = tuple(rows)
# sql = "insert into _collection(id,spidersource,title,content," \
#       "pubtime,savetime,source,picture_urls) values(UUID(),%s,%s,%s,%s,%s,%s,%s)"
# conn.exec_sql_many(sql, rows)
# conn.exec_sql("UPDATE collection SET count = IFNULL(count,0) + %d", patch_number)
# conn.close_conn()
#
# print(r.json())
#
# r = requests.get("https://wallstreetcn.com/articles/3460178")
# bs = BeautifulSoup(r.text,"lxml")
# print(type(bs.find('div',class_="rich-text")))
# print(bs.find('div',class_="rich-text"))
# uri = "https://xcong.com/articles/3460863"
# response = requests.get(uri)
# soup = BeautifulSoup(response.text)
# content = soup.find('div', id="js_content").text
# html_content = response.text
# print(html_content)
Type = Enum("Type", ("龙虎榜", "早晚报", "行情分析", "好文精选"))
print(Type.早晚报.name)