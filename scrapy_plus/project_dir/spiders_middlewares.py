from scrapy_plus.conf.settings import USER_AGENT_LIST
import random
from scrapy_plus.project_dir.proxies_ip import add_proxies_ip


class BaiduMiddleware:

    def process_request(self, request):
        '''处理请求头，添加默认的user-agent'''
        proxies_ip = add_proxies_ip(request)
        request.proxies = proxies_ip
        request.headers['User-Agent'] = random.choice(USER_AGENT_LIST)
        request.headers['Host'] = 'ggzyjy.xxz.gov.cn'
        request.headers['Referer'] = 'http://ggzyjy.xxz.gov.cn/jyxx/aboutjyxxsearch.html'
        request.headers['Connection'] = 'keep-alive'
        request.headers['Origin'] = 'http://ggzyjy.xxz.gov.cn'
        # print("BaiduMiddleware: process_request")
        return request

    def process_response(self, response):
        '''处理数据对象'''
        # print("BaiduMiddleware: process_response")
        return response


class DoubanMiddleware:

    def process_request(self, request):
        '''处理请求头，添加默认的user-agent'''
        proxies_ip = add_proxies_ip(request)
        request.proxies = proxies_ip
        request.headers['User-Agent'] = random.choice(USER_AGENT_LIST)
        # print("DoubanMiddleware: process_request")
        return request

    def process_response(self, response):
        '''处理数据对象'''
        # print("DoubanMiddleware: process_response")
        return response