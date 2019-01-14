from scrapy.cmdline import execute
import sys
import os
#直接运行execute.py的话，需要配置bztSpider爬虫项目的根路径(也就是本文件的父目录路径)加入sys.path
#因为调用了utils里的dbConnector.py模块，也需要把bztSpider\\bztSpider\\utils加入项目路径
sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("./utils"))
execute(['scrapy','crawl','XcongNews'])