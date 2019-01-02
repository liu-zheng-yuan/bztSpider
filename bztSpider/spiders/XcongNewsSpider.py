from scrapy import Spider, Request, http
import settings
import json
from items import NewsItem
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from enum import Enum


class XcongNewsSpider(Spider):
    name = "XcongNews"
    END_TIMESTAMP = settings.END_TIMESTAMP  # 结束爬取的时间戳
    ISINCREMENTAL = settings.ISINCREMENTAL  # 是否是增量爬取模式。如果为True，则每次只从最新的时间点爬取5条
    custom_settings = {
        'ITEM_PIPELINES': {
            'bztSpider.pipelines.NewsPipeline': 301,
        }
    }

    def start_requests(self):
        url = "https://cong-api.xcong.com/apiv1/dashboard/chosen_page?limit={limit}&cursor="  # 开始时cursor为空即当前时间
        params = {}
        if self.ISINCREMENTAL == False:
            params["limit"] = 20  # 非增量模式 一次爬20条 会往后爬
        else:
            params["limit"] = 5  # 增量模式 一次爬5条 不会往后爬
        yield Request(url.format(**params), callback=self.parse)

    def parse(self, response: http.response.Response):
        if response.status == 200:
            data_json = json.loads(response.text)

            datas = data_json["data"]["items"]
            for data in datas:
                if data["resource_type"] == "article":  # 可能出现不是文章而是推荐列表的情况
                    item = NewsItem()
                    item["id"] = data["resource"]["id"]
                    item["spider_source"] = "小葱"
                    item["title"] = data["resource"]["title"]
                    item["abstract"] = data["resource"]["content_short"]
                    item["pubtime"] = datetime.fromtimestamp(
                        data["resource"]["display_time"]
                    ).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )  # 转成datetime 再转成字符串
                    item["savetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    item["source"] = data["resource"]["source_name"]
                    item["editor"] = data["resource"]["author"]["display_name"]
                    item["url"] = data["resource"]["uri"]
                    item["type"] = self.get_article_type(data)
                    item["picture_url"] = data["resource"][
                        "image_uri"
                    ]  # 只存小葱文章列表的缩略图 不存实际文章里的图
                    # 以上都是能直接从请求到的json里获得的数据，以下的（如文章内容和html）需要进一步请求文章实际地址获取
                    if (
                            data["resource"]["uri"].find("https://wallstreetcn.com/") != -1
                    ):  # 该文章来自华尔街见闻本站
                        # api里的url是华尔街主站的，这里要手动把小葱的域名拼上抓来的文章id，真正抓取的文章内容来自小葱对应的网页
                        item["content"], item[
                            "html_content"
                        ] = self.parse_wallstreet("https://xcong.com/articles/" + data["resource"]["uri"][34:])
                        yield item
                    elif (
                            data["resource"]["uri"].find(
                                "https://api-prod.wallstreetcn.com"
                            )
                            != -1
                            and data["resource"]["uri"].find("weixin") != -1
                    ):  # 文章来自微信
                        item["content"], item[
                            "html_content"
                        ] = self.parse_weixin(data["resource"]["uri"])
                        yield item
                    else:
                        continue  # 来自其他网站的文章 忽略
            #寻找下一次爬取的url
            next_cursor = data_json["data"]["next_cursor"]
            next_url = "https://cong-api.xcong.com/apiv1/dashboard/chosen_page?limit=20&cursor={}".format(
                next_cursor
            )
            # 只有当非增量模式时 才需要往后爬
            if int(next_cursor) > self.END_TIMESTAMP and self.ISINCREMENTAL == False:
                yield Request(next_url, callback=self.parse)

    def parse_wallstreet(self, uri: str):
        # 这里之所以不直接请求华尔街主站的url，因为网页加载慢，可能抓不到
        response = requests.get(uri)
        soup = BeautifulSoup(response.text, features="lxml")
        content = ""
        try:
            content = soup.find("div", class_="article-detail").text
        except Exception as e:
            with open("errorlog.txt", "a+") as f:
                f.write("小葱页面解析出错,URL=" + uri + "\n")
        html_content = soup.find("div", class_="article-detail").prettify()
        return (content, html_content)

    def parse_weixin(self, uri: str):
        response = requests.get(uri)
        soup = BeautifulSoup(response.text, features="lxml")
        content = ""
        try:
            content = soup.find("div", id="js_content").text
        except Exception as e:
            with open("errorlog.txt", "a+") as f:
                f.write("微信页面解析出错,URL=" + uri + "\n")
        html_content = response.text
        return (content, html_content)

    def get_article_type(self, data: dict):
        # 根据json里的themes属性 确定该文章的类型
        # 按优先级依次为：龙虎榜、早晚报、行情分析、好文精选
        # 定义枚举类
        Type = Enum("Type", ("龙虎榜", "早晚报", "行情分析", "好文精选"))
        type_candidates = [x["property_name"] for x in data["resource"]["themes"]]
        if "小葱龙虎榜" in type_candidates:
            return Type.龙虎榜.name
        elif "小葱早晚报" in type_candidates:
            return Type.早晚报.name
        elif "数字货币行情分析" in type_candidates:
            return Type.行情分析.name
        else:
            return Type.好文精选.name
