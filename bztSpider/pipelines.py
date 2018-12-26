# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from dbConnector import dbConnector
from items import NewsFlashItem


class NewsFlashPipeline(object):
    def __init__(self):
        self.conn = None

    def open_spider(self, spider):
        self.conn = dbConnector()

    def process_item(self, item: NewsFlashItem, spider):
        existed_count = self.conn.exec_sql_feach(
            "select count(*) count from news_flash_collection where news_flash_id = {}".format(
                item["news_flash_id"]
            )
        )[0]["count"]
        if existed_count != 0:  # id已存在则不重复加入
            print("以下为重复记录，news_flash_id为" + str(item["news_flash_id"]))
            return item
        # 要插入的数据
        row = (
            item["news_flash_id"],
            item["news_flash_spider_source"],
            item["news_flash_title"],
            item["news_flash_content"],
            item["news_flash_pubtime"],
            item["news_flash_savetime"],
            item["news_flash_source"],
            item["news_flash_picture_urls"],
        )

        self.conn.exec_sql(
            "insert into news_flash_collection(news_flash_id"
            ", news_flash_spider_source"
            ", news_flash_title"
            ", news_flash_content"
            ", news_flash_pubtime"
            ", news_flash_savetime"
            ", news_flash_source"
            ", news_flash_picture_urls"
            ") values(%s,%s,%s,%s,%s,%s,%s,%s)",
            row,
        )
        # 获取当前最大的count
        data = self.conn.exec_sql_feach(
            "select IFNULL(max(news_flash_count),0) maxCount from news_flash_collection"
        )
        maxCount = data[0]["maxCount"]
        # 更新所有记录的count字段为最大值
        self.conn.exec_sql(
            "update news_flash_collection set news_flash_count = {}".format(
                maxCount + 1
            )
        )
        return item

    def close_spider(self, spider):
        self.conn.close_conn()
