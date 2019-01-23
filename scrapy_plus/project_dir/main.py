from scrapy_plus.core.engine import Engine
from spiders.xiangxi_public_spider import Xiangxi_public_Spider
from spiders.douban_spider import DoubanSpider
# 多管道
from scrapy_plus.project_dir.pipelines import UniversalPipeline
# 多中间键
from scrapy_plus.project_dir.spiders_middlewares import Xiangxi_public_SpiderMiddleware, DoubanMiddleware

if __name__ == '__main__':

    # 由于爬虫部分被配置到了conf的settings文件中、所有每次增加爬虫只需要在settings添加就行、engine引擎将会动态导入
    '''
    # 百度爬虫
    xps = Xiangxi_public_Spider()
    # 豆瓣爬虫
    dbs = DoubanSpider()
    # 将所有爬虫写成字典
    spiders = {
        Xiangxi_public_Spider.name : xps,
        # DoubanSpider.name : dbs
    }
    '''

    # 课件选用列表
    # pipelines = [BaiduPipeline(), DoubanPipeline()]
    '''因为是通用爬虫、所有爬虫基本都是公用这个pipeline、所以不用设置多管道只需设置一个就行'''
    pipelines = UniversalPipeline()
    # pipelines = {'Universal' : UniversalPipeline()}
    # 键值对形式 键为爬虫名 值为中间件对象
    middlewares = {'xiangxi_public_spider' : Xiangxi_public_SpiderMiddleware(), 'douban' : DoubanMiddleware()}

    # engine = Engine(spiders, pipelines = pipelines, middlewares = middlewares)
    # 使用动态导入后的修改
    engine = Engine(pipelines = pipelines, middlewares = middlewares)
    engine.start()