# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from dbConnector import dbConnector

class NewsFlashPipeline(object):
    def __init__(self):
        self.conn = None

    def open_spider(self,spider):
        self.conn = dbConnector()
    def process_item(self, item, spider):
        self.conn.exec_sql("insert into news_flash_collection(news_flash_spider_source"
                      ", news_flash_title"
                      ", news_flash_content"
                      ", news_flash_pubtime"
                      ", news_flash_savetime"
                      ", news_flash_source"
                      ", news_flash_picture_urls"
                      ", news_flash_count) values(%s,%s,%s,%s,%s,%s,%s)",dict(item))
        return item
    def close_spider(self,spider):
        self.conn.close_conn()


