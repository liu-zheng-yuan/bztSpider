# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from dbConnector import dbConnector
from items import NewsFlashItem, NewsItem
import emoji
import redis
import settings

class NewsFlashPipeline(object):
    def __init__(self):
        self.conn = None
        # redis的数据库连接池
        self.rpool =None
        self.rconn = None

    def open_spider(self, spider):
        self.conn = dbConnector()
        self.rpool = redis.ConnectionPool(host=settings.REDIS_host, port=settings.REDIS_port, decode_responses=True)
        self.rconn = redis.Redis(connection_pool=self.rpool)

    def process_item(self, item: NewsFlashItem, spider):
        existed_count = self.conn.exec_sql_feach(
            "select count(*) count from news_flash_collection where id = {}".format(
                item["id"]
            )
        )[0]["count"]
        if existed_count != 0:  # id已存在则不重复加入
            print("以下为重复记录，id为" + str(item["id"]))
            return item
        # 要插入的数据
        row = (
            item["id"],
            item["spider_source"],
            item["title"],
            item["content"],
            item["pubtime"],
            item["savetime"],
            item["source"],
            item["picture_urls"],
        )

        self.conn.exec_sql(
            "insert into news_flash_collection(id"
            ", spider_source"
            ", title"
            ", content"
            ", pubtime"
            ", savetime"
            ", source"
            ", picture_urls"
            ") values(%s,%s,%s,%s,%s,%s,%s,%s)",
            row,
        )
        # 获取当前最大的count
        data = self.conn.exec_sql_feach(
            "select IFNULL(max(count),0) maxCount from news_flash_collection"
        )
        maxCount = data[0]["maxCount"]
        # 更新所有记录的count字段为最大值
        self.conn.exec_sql(
            "update news_flash_collection set count = {}".format(
                maxCount + 1
            )
        )
        #更新redis中的count值
        #每插入一条自增1,如果数据库中没有News_Flash_Count,会从1开始.
        self.rconn.incr("News_Flash_Count")
        return item

    def close_spider(self, spider):
        self.conn.close_conn()
        self.rpool.disconnect()


class NewsPipeline(object):
    def __init__(self):
        self.conn = None
        # redis的数据库连接池
        self.rpool =None
        self.rconn = None

    def open_spider(self, spider):
        self.conn = dbConnector()
        self.rpool = redis.ConnectionPool(host=settings.REDIS_host, port=settings.REDIS_port, decode_responses=True)
        self.rconn = redis.Redis(connection_pool=self.rpool)


    def process_item(self, item: NewsItem, spider):
        TYPE_NUMBER = {
            "好文精选": 1,
            "行情分析": 2,
            "早晚报": 3,
            "龙虎榜": 4
        }
        existed_count = self.conn.exec_sql_feach(
            "select count(*) count from news_collection where id = {}".format(
                item["id"]
            )
        )[0]["count"]
        if existed_count != 0:  # id已存在则不重复加入
            print("以下为重复记录，news_id为" + str(item["id"]))
            return item
        row = (
            item["id"],
            item["spider_source"],
            item["title"],
            item["abstract"],
            emoji.demojize(item["content"]),  # 去除文章中4字节的emoji表情
            item["pubtime"],
            item["savetime"],
            item["source"],
            item["editor"],
            item["url"],
            TYPE_NUMBER[item["type"]],
            item["picture_url"],
            emoji.demojize(item["html_content"]),  # 去除文章中4字节的emoji表情
        )
        try:
            # 要插入的数据
            response = self.conn.exec_sql(
                "insert into news_collection(id,spider_source, title, abstract, content, pubtime, savetime, source, editor, url, type, picture_url, html_content) "
                "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                row,
            )
            if type(response) == int:  # 当插入成功时才更新数量
                # 获取当前最大的count
                data = self.conn.exec_sql_feach(
                    "select IFNULL(max(count),0) maxCount from news_collection"
                )
                maxCount = data[0]["maxCount"]
                # 更新所有记录的count字段为最大值
                self.conn.exec_sql(
                    "update news_collection set count = {}".format(
                        maxCount + 1
                    )
                )
                # 更新redis中的count值
                # 每插入一条自增1,如果数据库中没有News_Flash_Count,会从1开始.
                self.rconn.incr("News_Count")
            else:  # 插入不成功时 找出不成功的文章的url
                with open("errorlog.txt", "a+") as f:
                    f.write(item["url"] + "未被成功写入\n")
        except Exception as e:
            with open("errorlog.txt", "a+") as f:
                f.write(item["url"] + "未被成功写入\n")
        return item

    def close_spider(self, spider):
        self.conn.close_conn()
        self.rpool.disconnect()

