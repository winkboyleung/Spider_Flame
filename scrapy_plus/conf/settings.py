# 全部导入默认配置文件的属性
from scrapy_plus.conf.default_settings import *
from scrapy_plus.project_dir.settings import *
import redis


SPIDERS = ['spiders.baidu_spider.BaiduSpider', 'spiders.douban_spider.DoubanSpider']

# 这个并没有用到
PIPELINES = ['pipelines.BaiduPipeline', 'pipelines.DoubanPipeline']

# 启用的爬虫中间件类
SPIDER_MIDDLEWARES = []

# 启用的下载器中间件类
DOWNLOADER_MIDDLEWARES = []

# 默认异步线程最大并发数，此参数可以在项目的settings.py中重新设置自动覆盖
MAX_ASYNC_THREAD_NUMBER = 4

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
]

# 链接ip池的redis
pool = redis.ConnectionPool(host='120.77.159.174', port=6379, db=6)
redis_ip = redis.Redis(connection_pool = pool)


