# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
from bztSpider.items import NewsFlashItem
from scrapy import Request,Spider

class XcongFlashSpider(Spider):
    name = 'xcong'
    allowed_domains = ['wallstreetcn.com']
    api_url = "https://api-prod.wallstreetcn.com/apiv1/content/lives"
    start_urls = ['https://api-prod.wallstreetcn.com/apiv1/content/lives?channel=xiaocong-channel&client=pc&cursor=&limit=50&first_page=false&accept_symbols=coin']
    # 建两个表快讯一个 新闻一个 多一个字段表示记录来自于哪个网站
    # def start_requests(self):
    #     channel = "xiaocong-channel"
    #     client ="pc"
    #     cursor=""
    #     limit = "50"
    #     first_page ="false"
    #     accept_symbols = "coin"
    #     yield Request(self.api_url.format(channel = channel,client=client,cursor=cursor,limit=limit,first_page=first_page,accept_symbols=accept_symbols),callback=self.parse)

    def parse(self, response:scrapy.http.response.Response):
        if response.status == 200:
            patch_number = 50  # 一批插入的数量
            self.logger.debug(response.text)
            data_json = json.loads(response.text)
            for i in range(patch_number):
                data = data_json['data']['items'][i]
                item = NewsFlashItem()
                item["news_flash_spider_source"] = "小葱"
                item["news_flash_title"] = data["title"]
                item["news_flash_content"] = data["content_text"]
                item["news_flash_pubtime"] = datetime.datetime.fromtimestamp(data['display_time']).strftime(
                    '%Y-%m-%d %H:%M:%S')  # 转成datetime 再转成字符串
                item["news_flash_savetime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item["news_flash_source"] = "小葱快讯"
                item["news_flash_picture_urls"] = ",".join(data["image_uris"])
                yield item

