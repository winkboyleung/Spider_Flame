# 请求类、用于构造请求对象

class Request:

    def __init__(self, url, method='GET', headers={}, params={}, data={}, callback='parse', meta = {}, execute_spide = ''):
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data

        # 指明默认使用parse作为解析函数
        self.callback = callback
        self.meta = meta

        # 新增内容 多解析函数需要传参来确定爬虫名、进而通过爬虫名获取到对应的爬虫对象、再进而调用该爬虫对象的解析函数
        self.execute_spider = execute_spide