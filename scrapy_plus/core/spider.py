# 爬虫模块：构造请求、解析响应数据
from ..http.request import Request
from ..item import Item

class Spider:

    name = ''

    start_urls = []

    # 将该start_url实例化为一个请求对象并且返回
    # def start_request(self):
    #     return Request(self.start_url)

    def start_request(self):
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        # print(response.url)
        # return Item(response.body)
        yield response.body