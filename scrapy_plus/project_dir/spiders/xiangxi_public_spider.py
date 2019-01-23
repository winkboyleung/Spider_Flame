import re
import time
from copy import deepcopy
import json

from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request

# 导入城市字典
from scrapy_plus.project_dir.city_data import city_dict

# 导入程序退出函数
from scrapy_plus.project_dir.quit_spider import quit
# 导入邮箱功能用于xpath提取规则出错时使用
from scrapy_plus.utils.STMP import send_mail_when_error

'''http://ggzyjy.xxz.gov.cn/jyxx/aboutjyxxsearch.html@湘西公共资源交易网'''

class Xiangxi_public_Spider(Spider):

    name = 'xiangxi_public_spider'

    start_urls = ['https://httpbin.org/get']

    def __init__(self):
        self.base_url = 'http://ggzyjy.xxz.gov.cn'

        # xpath提取错误计数
        self.error_count = 0

        with open('./RegularExpression.txt', 'r')as f:
            self.regularExpression = f.read()

    def start_request(self):
        # 采购信息 （汇总了所有分类） 共227页 每天更新数据跨度1页
        url = 'http://ggzyjy.xxz.gov.cn/EpointWebBuilderXiang/moreinfojyxxlistAction.action?cmd=getInfolist'
        for page in range(0, 2):
            data = {
                'CatgoryNum': '005',
                # 该网页从第一页从0开始
                'pageIndex': str(page),
                'pageSize': '15'
            }
            yield Request(url, execute_spide = self.name, callback = 'parse', method='post', data = data)

    def parse(self, response):
        response = json.loads(response.body)
        each_page_infos = json.loads(response['custom'])['data']

        for each_info in each_page_infos:

            items = {}
            items['title'] = ''
            items['url'] = ''
            items['web_time'] = ''
            items['intro'] = ''
            items['addr_id'] = ''

            try:
                items['title'] = each_info['title']
            except:
                pass

            try:
                items['url'] = self.base_url + each_info['href']
            except:
                msg = self.name + ', 该爬虫详情页获取url失败'
                send_mail_when_error(msg)
                self.error_count += 1
                if self.error_count > 3:
                    quit()
                    msg = self.name + ', 该爬虫因详情页获取失败被暂停'
                    send_mail_when_error(msg)
                    pass

            try:
                items['web_time'] = each_info['date']
            except:
                pass

            if '成交' in items['title'] or '中标' in items['title']:
                items['type_id'] = '38257'

            elif '更正' in items['title'] or '变更' in items['title']:
                items['type_id'] = '38256'

            else:
                items['type_id'] = '38255'

            yield Request(url = items['url'], callback = 'parse_article', meta = {'items':deepcopy(items)}, execute_spide = self.name)

    def parse_article(self, response):
        items = response.meta['items']

        try:
            article_text = re.search(r'class="ewb-article".*?>(.*?)<!-- footer -->', response.body, re.S).group(1)
            clean_text = re.sub(eval(self.regularExpression), ' ', article_text)
            items['intro'] = clean_text
        except:
            pass

        # 地方名称编号
        items["addr_id"] = '431'
        # 系统时间，时间戳
        items["time"] = '%.0f' % time.time()
        # 分类id
        items["sheet_id"] = '29'
        # 文章来源
        items["source_name"] = '湘西公共资源交易网'

        yield items


