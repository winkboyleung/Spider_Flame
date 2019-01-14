from scrapy_plus.core.engine import Engine
from spiders.baidu_spider import BaiduSpider
from spiders.douban_spider import DoubanSpider

from scrapy_plus.project_dir.pipelines import BaiduPipeline, DoubanPipeline

if __name__ == '__main__':
    # 百度爬虫
    bds = BaiduSpider()
    # 豆瓣爬
    dbs = DoubanSpider()
    # 将所有爬虫写成字典
    spiders = {
        BaiduSpider.name : bds,
        DoubanSpider.name : dbs
    }

    # 课件选用列表
    # pipelines = [BaiduPipeline(), DoubanPipeline()]
    pipelines = {'baidu': BaiduPipeline(), 'douban': DoubanPipeline()}

    engine = Engine(spiders, pipelines = pipelines)
    engine.start()