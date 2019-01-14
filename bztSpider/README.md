## 爬虫
XcongNews:爬小葱的要闻
XcongNewsFlash:爬小葱的快讯
## DEBUG入口
execute.py 

pycharm中启动参数Parameters:"crawl XcongNews(XcongFlash)"

## settings.py设置
END_TIMESTAMP = 1546272000 #爬取截至时间戳 现在是2019.1.1 00 00 00

ISINCREMENTAL = False #是否增量模式 开始时为Flase 爬取历史文章 第一次爬取完成后设定为True 每隔几分钟爬取一次 只爬取最新的若干条

## 虚拟环境
使用了venv，如果要使用命令行启动，需要先在venv/Scripts中先启动activate

再运行execute.py，其中execute()函数的参数是类似['scrapy','crawl','XcongNews']

list中第三个元素填要启动的Spider(XcongNews或XcongFlash)

## 运行多个爬虫
暂时的想法是复制两个项目，分别设置启动参数为'XcongNews'和'XcongFlash'

分别运行execute.py文件

## 定时运行
Linux使用cron命令分别运行两个项目

可以设定为每5分钟爬取最新要闻，每2分钟爬取最新快讯