from scrapy_plus.core.engine import Engine
from spiders.baidu_spider import BaiduSpider
from spiders.douban_spider import DoubanSpider
# 多管道
from scrapy_plus.project_dir.pipelines import BaiduPipeline, DoubanPipeline
# 多中间键
from scrapy_plus.project_dir.spiders_middlewares import BaiduMiddleware, DoubanMiddleware

if __name__ == '__main__':
    # # 百度爬虫
    # bds = BaiduSpider()
    # # 豆瓣爬
    # dbs = DoubanSpider()
    # # 将所有爬虫写成字典
    # spiders = {
    #     BaiduSpider.name : bds,
    #     DoubanSpider.name : dbs
    # }

    # 课件选用列表
    # pipelines = [BaiduPipeline(), DoubanPipeline()]
    pipelines = {'baidu' : BaiduPipeline(), 'douban' : DoubanPipeline()}
    middlewares = {'baidu' : BaiduMiddleware(), 'douban' : DoubanMiddleware()}

    engine = Engine(pipelines = pipelines, middlewares = middlewares)
    engine.start()