# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BztspiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    news_title = Field()  # 新闻标题
    news_pageview = Field()  # 浏览量
    # news_id = Field()
    # newsid_hash = Field()
    news_url = Field()  # 新闻链接
    news_content = Field()  # 新闻文字内容
    news_content_body = Field()  # 新闻带P标签
    news_pubtime = Field()  # 新闻发布时间
    news_savetime = Field()  # 新闻爬取时间
    news_source = Field()  # 新闻来源（例如小葱、巴比特、金色财经）
    news_editor = Field()  # 编辑
    news_summary = Field()  # 摘要
    news_type = Field()  # 类型（快讯、要闻）
    news_lable = Field()  # 要闻中的类型（行业、公告、深度解读）
    news_picture_url = Field()  # 文章中图片列表
    spider = Field()  # 爬虫名称
    # news_comments = Field()
    # news_comment_count = Field()
    # enterprises_name = Field()
    # enterprises_id = Field()
    # news_keywords = Field()
    # news_main_type = Field()
