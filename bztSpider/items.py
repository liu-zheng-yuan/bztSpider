# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class NewsFlashItem(Item):
    id = Field()  # 唯一主键
    spider_source = Field()  # 爬取网站名称
    title = Field()  # 新闻标题
    content = Field()  # 新闻内容
    pubtime = Field()  # 新闻发布时间
    savetime = Field()  # 新闻抓取日期
    source = Field()  # 新闻出处
    picture_urls = Field()  # 图片url
    count = Field()  # 总快讯数量


class NewsItem(Item):
    id = Field()  # 唯一主键
    spider_source = Field()  # 爬取网站名称
    title = Field()  # 新闻标题
    content = Field()  # 新闻内容
    abstract = Field()  # 新闻摘要
    pubtime = Field()  # 新闻发布时间
    savetime = Field()  # 新闻抓取日期
    source = Field()  # 新闻出处
    editor = Field()  # 新闻责任编辑
    url = Field()  # 新闻网址
    type = Field()  # 新闻类型
    picture_url = Field()  # 新闻中的图片网址，逗号隔开
    html_content = Field()  # 新闻原来的html内容
    count = Field()  # 总数量

# class BztspiderItem(Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     news_title = Field()  # 新闻标题
#     news_pageview = Field()  # 浏览量
#     # news_id = Field()
#     # newsid_hash = Field()
#     news_url = Field()  # 新闻链接
#     news_content = Field()  # 新闻文字内容
#     news_content_body = Field()  # 新闻带P标签
#     news_pubtime = Field()  # 新闻发布时间
#     news_savetime = Field()  # 新闻爬取时间
#     news_source = Field()  # 新闻来源（例如小葱、巴比特、金色财经）
#     news_editor = Field()  # 编辑
#     news_summary = Field()  # 摘要
#     news_type = Field()  # 类型（快讯、要闻）
#     news_lable = Field()  # 要闻中的类型（行业、公告、深度解读）
#     news_picture_url = Field()  # 文章中图片列表
#     spider = Field()  # 爬虫名称
#     # news_comments = Field()
#     # news_comment_count = Field()
#     # enterprises_name = Field()
#     # enterprises_id = Field()
#     # news_keywords = Field()
#     # news_main_type = Field()
