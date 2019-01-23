from scrapy_plus.core.engine import Engine
from spiders.baidu_spider import BaiduSpider
from spiders.douban_spider import DoubanSpider
# 多管道
from scrapy_plus.project_dir.pipelines import UniversalPipeline
# 多中间键
from scrapy_plus.project_dir.spiders_middlewares import BaiduMiddleware, DoubanMiddleware

if __name__ == '__main__':
    # 百度爬虫
    bds = BaiduSpider()
    # 豆瓣爬虫
    dbs = DoubanSpider()
    # 将所有爬虫写成字典
    spiders = {
        BaiduSpider.name : bds,
        # DoubanSpider.name : dbs
    }

    # 课件选用列表
    # pipelines = [BaiduPipeline(), DoubanPipeline()]
    '''因为是通用爬虫、所有爬虫基本都是公用这个pipeline、所以不用设置多管道只需设置一个就行'''
    pipelines = UniversalPipeline()
    # pipelines = {'Universal' : UniversalPipeline()}
    middlewares = {'baidu' : BaiduMiddleware(), 'douban' : DoubanMiddleware()}

    # engine = Engine(spiders, pipelines = pipelines, middlewares = middlewares)
    # 使用动态导入后的修改
    engine = Engine(pipelines = pipelines, middlewares = middlewares)
    engine.start()