

class BaiduMiddleware:

    def process_request(self, request):
        '''处理请求头，添加默认的user-agent'''
        print("BaiduMiddleware: process_request")
        return request

    def process_response(self, response):
        '''处理数据对象'''
        print("BaiduMiddleware: process_response")
        return response


class DoubanMiddleware:

    def process_request(self, request):
        '''处理请求头，添加默认的user-agent'''
        print("DoubanMiddleware: process_request")
        return request

    def process_response(self, response):
        '''处理数据对象'''
        print("DoubanMiddleware: process_response")
        return response