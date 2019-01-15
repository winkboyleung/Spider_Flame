# 利用init方法初始化其他组件对象，在内部使用
# 实现start方法，由外部调用，启动引擎
# 实现_start_engine方法，完成整个框架的运行逻辑
# 具体参考上一小节中雏形结构引擎的逻辑

# 引擎组件
import time

from .downloader import Downloader
from .pipeline import Pipeline
from .scheduler import Scheduler
from .spider import Spider

from scrapy_plus.middlewares.download_middlewares import DownloaderMiddleware
from scrapy_plus.middlewares.spider_middlewares import SpiderMiddleware

from ..http.request import Request
# 导入日志模块
from scrapy_plus.utils.log import logger
from datetime import datetime

from scrapy_plus.project_dir.spiders.douban_spider import DoubanSpider

# 为了解藕性、将原本放在main函数中的所有爬虫类、管道类、中间键类移到settings配置中、然后使用动态导入
from scrapy_plus.conf.settings import SPIDERS, SPIDER_MIDDLEWARES, PIPELINES, DOWNLOADER_MIDDLEWARES
# 动态导入包
import importlib


class Engine:

    def __init__(self, pipelines = {}, middlewares = {}):
        # self.spider = Spider()
        # self.spider = spider
        self.spider = self._auto_import_instances(SPIDERS)
        self.scheduler = Scheduler()
        # self.pipeline = Pipeline()
        self.pipelines = pipelines
        self.downloader = Downloader()
        self.spider_mid = SpiderMiddleware()  # 初始化爬虫中间件对象
        # self.downloader_mid = DownloaderMiddleware()  # 初始化下载器中间件对象
        self.downloader_mid = middlewares  # 初始化下载器中间件对象

        # 计算总响应数量
        self.total_response_nums = 0
        # 总请求数量
        self.total_request_nums = 0

    def _auto_import_instances(self, path = []):
        instance = {}
        # path为一个列表、存放着spider、middle、pipeline各功能的配置文件中配置的导入类的路径
        for each in path:
            # 该代码获取的是导入路径
            module_name = each.rsplit('.', 1)[0]
            # 获取类名
            class_name = each.rsplit('.', 1)[1]
            # 通过动态导入的方法通过module_name这个导入路径 获取到ret这个包 等价于import baidi_spider 所以这个ret还不是类对象
            ret = importlib.import_module(module_name)
            # 使用getattr方法 传入类对象ret 和 类名class_name 获取到爬虫的类对象
            spider = getattr(ret, class_name)
            instance[spider.name] = spider()

        return instance



    def start(self):
        start = datetime.now()
        logger.info("开始运行时间：%s" % start)  # 使用日志记录起始运行时间
        self._start_engine()
        stop = datetime.now()
        logger.info("运行结束时间：%s" % stop)  # 使用日志记录结束运行时间
        logger.info("耗时：%.2f" % (stop - start).total_seconds())  # 使用日志记录运行耗时
        logger.info("总的请求数量:{}".format(self.scheduler.total_request_nums))
        logger.info("总的响应数量:{}".format(self.total_response_nums))

    def get_request(self):
        for spider_name, spider in self.spider.items():
            # 第一步 通过上面for循环的遍历 获得某个爬虫的初始请求对象(可能是一个或者多个)
            # for start_request in self.spider.start_request():
            for start_request in spider.start_request():
                # 给每个request请求绑定爬虫名 (这里的每个request指的是使用start_request所生成的request而已)
                start_request.spider_name = spider_name
                # 第二步 将请求对象添加到schedule的缓存队列中
                # 利用爬虫中间件预处理请求对象（暂时注释掉、不知道爬虫中间键的用处）
                # start_request = self.spider_mid.process_request(start_request)
                self.scheduler.add_request(start_request)
                # 请求数+1
                self.total_request_nums += 1

    def process_request(self):

        # 第三步 从缓存队列中获取请求对象
        request = self.scheduler.get_request()
        # 利用下载器中间件预处理请求对象
        if request is None:
            return
        
        try:
            downloader_middleware = self.downloader_mid[request.execute_spider]
            request = downloader_middleware.process_request(request)
            # print(request.spider_name)
            # 第四步 拿到请求对象后、使用downlader下载器获取response对象
            response = self.downloader.get_response(request)

            # 当获取到response对象后、将request里的meta参数传递到response中
            response.meta = request.meta

            # 利用下载器中间件预处理响应对象
            downloader_middleware = self.downloader_mid[request.execute_spider]
            response = downloader_middleware.process_response(response)

            # 现在根据spider_name来获取到类对象
            try:
                spider = self.spider[request.spider_name]
            # 新增内容 由于上面的try语句只适合start_request函数的request对象、而下面这个语句则适合于多解析函数的情况
            except:
                spider = self.spider[request.execute_spider]
            print(self.total_response_nums, self.total_request_nums)
            # 获取请求对象中parse方法、并且调用这个parse方法解析这个response对象
            # 此处的request.callback来自上面几行的request 首次调用的request.callback基本是 == 'parse'这个解析函数
            # 所以下面这行代码意思从self.spider这个类对象中获取到request.callback的值 然后再赋值给parse这个变量
            # 然后在这个变量parse后面加上括号、就等同于调用self.spider类的解析函数
            # parse = getattr(self.spider, request.callback)
            parse = getattr(spider, request.callback)
            # 第五步 利用爬虫解析所得到的响应结果
            # result = self.spider.parse(response)
            # 由于这里使用了for循环、所以parse(response)的结果必须使用yield方法、否则会报错、如果只是想打印、则使用上面的代码
            for result in parse(response):
                # 第六步 判断如果获取到请求对象则继续添加到schdule中 如果不是则由pipeline进行处理
                if isinstance(result, Request):
                    # 利用爬虫中间件预处理请求对象（暂时注释掉、不知道爬虫中间键的用处）
                    # result = self.spider_mid.process_request(result)
                    self.scheduler.add_request(result)
                    # 请求数+1
                    self.total_request_nums += 1

                else:
                    # 课件上的方法、虽可用、但是每次都要将所有管道遍历一次、浪费资源
                    # for pipeline in self.pipelines:
                    #     pipeline.process_item(result, spider)

                    # 自己重写的方法、不用遍历所有管道、只需要根据请求对象的spider名获取到self.pipelines中对应的管道即可
                    pipeline = self.pipelines[spider.name]
                    pipeline.process_item(result, spider)
                    # self.pipeline.process_item(result)


        finally:
            self.total_response_nums += 1


    def _start_engine(self):
        self.get_request()

        while 1:
            time.sleep(0.001)
            self.process_request()

            if self.total_response_nums >= self.total_request_nums:
                logger.info("程序结束")
                break