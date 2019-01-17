from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request


class DoubanSpider(Spider):

    # start_urls = []
    name = 'douban'

    def start_request(self):
        base_url = 'http://movie.douban.com/top250?start='
        for page in range(0, 50, 25):
            url = base_url + str(page)
            yield Request(url, execute_spide = self.name)

    def parse(self, response):
        # title_list = []
        # 获取每页所有的li标签、每页25个
        for each_li in response.xpath('//ol[@class="grid_view"]/li')[:3]:
            items = {}
            items['title'] = each_li.xpath('.//span[@class="title"]/text()')[0]
            # title_list.append(items)
            items['url'] = each_li.xpath('.//div[@class="hd"]/a/@href')[0]
            yield Request(url = items['url'], callback = 'parse_article', meta = {'items' : items}, execute_spide = self.name)
        # yield title_list


    def parse_article(self, response):
        items = response.meta['items']
        # items['content'] = response.xpath('//div[@class="indent"]//text()')[0]
        print("详情内容为 : {}".format(items))