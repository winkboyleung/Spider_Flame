class SpiderMiddleware:

    def process_request(self, request):
        print("这是爬虫中间件：process_request方法")
        return request

    def process_response(self, response):
        print("这是爬虫中间件：process_response方法")
        return response