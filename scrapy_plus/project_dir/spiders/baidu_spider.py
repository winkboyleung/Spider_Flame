from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request


class BaiduSpider(Spider):

    name = 'baidu'

    start_urls = ['https://www.baidu.com']

    def start_request(self):
        for nums in range(1, 5):
            url = 'https://www.baidu.com'
            yield Request(url, execute_spide = self.name)