## 爬虫
XcongNews:爬小葱的要闻
XcongNewsFlash:爬小葱的快讯
## DEBUG入口
execute.py 

pycharm中启动参数Parameters:"crawl XcongNews(XcongFlash)"

## settings.py设置
END_TIMESTAMP = 1546272000 #爬取截至时间戳 现在是2019.1.1 00 00 00

ISINCREMENTAL = False #是否增量模式 开始时为Flase 爬取历史文章 后面设定为True 每隔几分钟爬取一次 只爬取最新的若干条

## 虚拟环境
使用了venv，如果要使用命令行启动，需要先在venv/Scripts中先启动active.bat

再使用scrapy crawl XcongNews(XcongFlash)爬取新闻或者要闻

