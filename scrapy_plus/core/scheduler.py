# 调度器模块：缓存请求、请求去重
from queue import Queue


class Scheduler:

    def __init__(self):
        # 创建队列 用来缓存请求对象
        self.queue = Queue()
        self.total_request_nums = 0

    def add_request(self, request):
        self.queue.put(request)
        self.total_request_nums += 1

    def get_request(self):
        try:
            request = self.queue.get(False)
        except:
            return None
        else:
            return request

    def filter_request(self, request):
        # 实现请求去重 如果该请求需要被过滤就返回true，否则返回false
        pass