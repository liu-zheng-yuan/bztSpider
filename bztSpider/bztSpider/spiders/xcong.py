# -*- coding: utf-8 -*-
import scrapy


class XcongSpider(scrapy.Spider):
    name = 'xcong'
    allowed_domains = ['xcong.com']
    start_urls = ['http://xcong.com/']
    # 建两个表快讯一个 新闻一个 多一个字段表示记录来自于哪个网站
    def parse(self, response:scrapy.http.response.Response):
        pass

