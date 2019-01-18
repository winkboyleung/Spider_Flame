# 全部导入默认配置文件的属性
from scrapy_plus.conf.default_settings import *
from scrapy_plus.project_dir.settings import *


SPIDERS = ['spiders.baidu_spider.BaiduSpider', 'spiders.douban_spider.DoubanSpider']

PIPELINES = ['pipelines.BaiduPipeline', 'pipelines.DoubanPipeline']

# 启用的爬虫中间件类
SPIDER_MIDDLEWARES = []

# 启用的下载器中间件类
DOWNLOADER_MIDDLEWARES = []

# 默认异步线程最大并发数，此参数可以在项目的settings.py中重新设置自动覆盖
MAX_ASYNC_THREAD_NUMBER = 4