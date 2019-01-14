from scrapy_plus.project_dir.spiders.baidu_spider import BaiduSpider
from scrapy_plus.project_dir.spiders.douban_spider import DoubanSpider


class BaiduPipeline:
    # 这里有所不同的是，需要增加一个参数，也就是传入爬虫对象
    # 以此来判断当前item是属于那个爬虫对象的
    def process_item(self, item, spider):
        if spider.name == BaiduSpider.name:
            print("百度爬虫的数据:", item)
        return item


class DoubanPipeline:
    # 这里有所不同的是，需要增加一个参数，也就是传入爬虫对象
    # 以此来判断当前item是属于那个爬虫对象的
    def process_item(self, item, spider):
        if spider.name == DoubanSpider.name:
            print("豆瓣爬虫数据:", item)
        return item


