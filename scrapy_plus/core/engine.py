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
import importlib
from scrapy_plus.project_dir.spiders.douban_spider import DoubanSpider
from scrapy_plus.conf.settings import SPIDERS, PIPELINES, DOWNLOADER_MIDDLEWARES, SPIDER_MIDDLEWARES, MAX_ASYNC_THREAD_NUMBER

from multiprocessing.dummy import Pool

# 运行获取字典函数的代码
from scrapy_plus.project_dir.city_data import get_city_dict

# 导入mysql
import pymysql


class Engine:

    # 这里的pipelines和middlewares并不是通过导包过来的而是通过参数传递过来的
    def __init__(self, pipelines, middlewares = {}):
        # self.spider = Spider()
        # self.spider = spiders
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

        # 线程池对象
        self.pool = Pool()
        # 递归函数关闭机制 默认为关闭false
        self.is_running = False

        # # 初始化链接mysql生成游标
        # self.conn = pymysql.connect(host='47.106.13.62',
        #                             user='root',
        #                             password='jiayou875',
        #                             database='test_demo',
        #                             port=3306,
        #                             charset='utf8')
        # self.cur = self.conn.cursor()


    def _auto_import_instances(self, path = []):
        instance = {}
        for each in path:
            module_name = each.rsplit('.', 1)[0]    # 取出模块名称
            class_name = each.rsplit('.', 1)[1]     # 取出类名称
            ret = importlib.import_module(module_name)  # 动态导入爬虫模块
            spider = getattr(ret, class_name)       # 根据类名称获取类对象
            instance[spider.name] = spider()        # 组装成爬虫字典{spider_name:spider(),}
        return instance                             # 返回类对象字典或列表


    def start(self):
        start = datetime.now()
        logger.info("开始运行时间：%s" % start)  # 使用日志记录起始运行时间
        get_city_dict()
        time.sleep(0.1)
        self._start_engine()
        stop = datetime.now()
        logger.info("运行结束时间：%s" % stop)  # 使用日志记录结束运行时间
        logger.info("耗时：%.2f" % (stop - start).total_seconds())  # 使用日志记录运行耗时
        logger.info("总的请求数量:{}".format(self.total_request_nums))
        logger.info("总的重复请求数量:{}".format(self.scheduler.repeat_request_nums))
        logger.info("去重容器内的url : {}".format(self.scheduler._filter_container))
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
                # request.spider_name是只有start_request生成的请求对象才有的属性
                spider = self.spider[request.spider_name]
            # 新增内容 由于上面的try语句只适合start_request函数的request对象、而下面这个语句则适合于多解析函数的情况
            except:
                spider = self.spider[request.execute_spider]
            # print(self.total_response_nums, self.total_request_nums)
            # 获取请求对象中parse方法、并且调用这个parse方法解析这个response对象
            # 此处的request.callback来自上面几行的request 首次调用的request.callback基本是 == 'parse'这个解析函数
            # 所以下面这行代码意思从self.spider这个类对象中获取到request.callback的值 然后再赋值给parse这个变量
            # 然后在这个变量parse后面加上括号、就等同于调用self.spider类的解析函数
            # parse = getattr(self.spider, request.callback)
            parse = getattr(spider, request.callback)
            # 当parse函数是通过yield处理、则是一个迭代器可以通过下面的for循环进行遍历,如果不是yield处理的、则会返回none、响应数自动加1、这样的好处是、即使是使用print也不会报错
            results = parse(response)
            # 第五步 利用爬虫解析所得到的响应结果
            # result = self.spider.parse(response)
            # 由于这里使用了for循环、所以parse(response)的结果必须使用yield方法、否则会报错、如果只是想打印、则使用上面的代码
            # for result in parse(response):
            if results is not None:
                for result in results:
                    # 第六步 判断如果获取到请求对象则继续添加到schdule中 如果不是则由pipeline进行处理
                    if isinstance(result, Request):
                        # 利用爬虫中间件预处理请求对象（暂时注释掉、不知道爬虫中间键的用处）
                        # result = self.spider_mid.process_request(result)
                        self.scheduler.add_request(result)
                        # 请求数+1
                        self.total_request_nums += 1

                    else:
                        # 初始化链接mysql生成游标
                        conn = pymysql.connect(host='47.106.13.62',
                                               user='root',
                                               password='jiayou875',
                                               database='test_demo',
                                               port=3306,
                                               charset='utf8')
                        cur = conn.cursor()
                        # 课件上的方法、虽可用、但是每次都要将所有管道遍历一次、浪费资源
                        # for pipeline in self.pipelines:
                        #     pipeline.process_item(result, spider)

                        # 自己重写的方法、不用遍历所有管道、只需要根据请求对象的spider名获取到self.pipelines中对应的管道即可
                        pipeline = self.pipelines
                        pipeline.process_item(result, cur, conn)
                        # self.pipeline.process_item(result)


        finally:
            self.total_response_nums += 1


    def _call_back(self, temp):
        if self.is_running:
            self.pool.apply_async(self.process_request, callback = self._call_back)


    def _start_engine(self):
        self.is_running = True
        # 处理strat_urls产生的request
        self.pool.apply_async(self.get_request)
        # 设置中配置的线程数量
        for loop in range(MAX_ASYNC_THREAD_NUMBER):
            self.pool.apply_async(self.process_request, callback = self._call_back)

        while 1:
            time.sleep(0.001)
            # 因为异步，需要增加判断，响应数不能为0
            if self.total_response_nums != 0:
                # 成功的响应数+重复的数量>=总的请求数量 程序结束
                if self.total_response_nums + self.scheduler.repeat_request_nums >= self.total_request_nums:
                    # logger.info("程序结束")
                    self.is_running = False
                    break

