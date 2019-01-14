from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request


class BaiduSpider(Spider):

    name = 'baidu'

    start_urls = ['https://www.baidu.com']

    def start_request(self):
        for start_reuqest in self.start_urls:
            # print(start_reuqest)
            yield Request(start_reuqest, execute_spide = self.name)