# 全部导入默认配置文件的属性
from scrapy_plus.conf.default_settings import *
from scrapy_plus.project_dir.settings import *


# 启用的爬虫类
SPIDERS = [
    'spiders.baidu_spider.BaiduSpider',
    'spiders.douban_spider.DoubanSpider'
]

# PIPELINES = [
#     'pipelines.BaiduPipeline',
#     'pipelines.DoubanPipeline'
# ]
PIPELINES = {'baidu' : 'pipelines.BaiduPipeline', 'douban' : 'pipelines.DoubanPipeline'}


# 启用的爬虫中间件类
SPIDER_MIDDLEWARES = []

# 启用的下载器中间件类
DOWNLOADER_MIDDLEWARES = []

MAX_ASYNC_THREAD_NUMBER = 5
