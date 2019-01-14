# -*- coding: utf-8 -*-
from scrapy import Spider, Request, http
import datetime
import json
from bztSpider.items import NewsFlashItem
import os
import sys
import settings



# 一般情况 一天的新增简讯数量是70-100条 可以设定过2分钟运行一次爬取5条，经去重后放入数据库
# 问题1.因为是一次返回多条简讯，不能正好爬到END_TIMESTAMP为止，会多出几条
class XcongFlashSpider(Spider):
    name = "XcongFlash"
    allowed_domains = ["wallstreetcn.com"]

    END_TIMESTAMP = settings.END_TIMESTAMP  # 结束爬取的时间戳
    ISINCREMENTAL = settings.ISINCREMENTAL  # 是否是增量爬取模式。如果为True，则每次只从最新的时间点爬取50条
    custom_settings = {
        'ITEM_PIPELINES': {
            'bztSpider.pipelines.NewsFlashPipeline': 300,
        }
    }

    def start_requests(self):
        url = "https://api-prod.wallstreetcn.com/apiv1/content/lives?channel={channel}&client={client}&cursor={cursor}&limit={limit}&first_page={first_page}&accept_symbols={accept_symbols}"
        params = {
            "channel": "xiaocong-channel",
            "client": "pc",
            "cursor": "",
            "first_page": "false",
            "accept_symbols": "coin",
        }
        if self.ISINCREMENTAL == False:
            params["limit"] = 50  # 非增量模式 一次爬50条
        else:
            params["limit"] = 5  # 增量模式 一次爬5条 2分钟爬一次 每次只爬最新的页面 不往后爬
        yield Request(url.format(**params), callback=self.parse)  # 传入关键字参数要加**

    def parse(self, response: http.response.Response):
        if response.status == 200:
            data_json = json.loads(response.text)
            for i in range(len(data_json["data"]["items"])):
                data = data_json["data"]["items"][i]
                item = NewsFlashItem()
                item["id"] = int(data["id"])
                item["spider_source"] = "小葱"
                item["title"] = data["title"]
                item["content"] = data["content_text"]
                item["pubtime"] = datetime.datetime.fromtimestamp(
                    data["display_time"]
                ).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )  # 转成datetime 再转成字符串
                item["savetime"] = datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                item["source"] = "小葱快讯"
                item["picture_urls"] = ",".join(data["image_uris"])
                yield item
            # 寻找下一个请求的url
            next_cursor = data_json["data"]["next_cursor"]
            next_url = "https://api-prod.wallstreetcn.com/apiv1/content/lives?channel=xiaocong-channel&client=pc&cursor={}&limit=50&first_page=false&accept_symbols=coin".format(
                next_cursor
            )
            #只有当非增量模式时 才需要往后爬
            if int(next_cursor) > self.END_TIMESTAMP and self.ISINCREMENTAL == False:
                yield Request(next_url, callback=self.parse)
