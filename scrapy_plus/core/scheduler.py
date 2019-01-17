# 调度器模块：缓存请求、请求去重
from _sha1 import sha1
from queue import Queue
import six
import w3lib.url
from scrapy_plus.utils.log import logger


class Scheduler:

    def __init__(self):
        # 创建队列 用来缓存请求对象
        self.queue = Queue()
        self.request_repeat_nums = 0
        self._filter_container = set()

    def add_request(self, request):
        if self._filter_request(request):
            self.queue.put(request)

    def get_request(self):
        try:
            # 将获取队列设置为非阻塞、否则的话程序就出不去了
            request = self.queue.get(False)
        except:
            return None
        else:
            return request

    def _filter_request(self, request):
        # 实现请求去重 如果该请求需要被过滤就返回true，否则返回false
        request.fp = self._gen_fp(request)
        if request.fp not in self._filter_container:
            self._filter_container.add(request.fp)
            return True

        else:
            self.request_repeat_nums += 1
            logger.info("发现重复的请求：<{} {}>".format(request.method, request.url))
            return False

    def _gen_fp(self, request):
        """生成并返回request对象的指纹
        用来判断请求是否重复的属性：url，method，params(在url中)，data
        为保持唯一性，需要对他们按照同样的排序规则进行排序
        """
        # 1. url排序：借助w3lib.url模块中的canonicalize_url方法
        url = w3lib.url.canonicalize_url(request.url)
        # 2. method不需要排序，只要保持大小写一致就可以 upper()方法全部转换为大写
        method = request.method.upper()
        # 3. data排序：如果有提供则是一个字典，如果没有则是空字典
        data = request.data if request.data is not None else {}
        data = sorted(data.items(), key=lambda x: x[0])  # 用sorted()方法 按data字典的key进行排序
        # items()返回元祖 key参数表示按什么进行排序 x表示data.items() x[0]表示元祖第一个值,也就是data的键

        # 4. 利用sha1计算获取指纹
        s1 = sha1()
        s1.update(self._to_bytes(url))  # sha1计算的对象必须是字节类型
        s1.update(self._to_bytes(method))
        s1.update(self._to_bytes(str(data)))

        fp = s1.hexdigest()
        return fp


    def _to_bytes(self, string):
        if six.PY3:
            if isinstance(string, str):
                return string.encode('utf8')
            else:
                return string

        elif six.PY2:
            if isinstance(string, str):
                return string
            else:
                return string.encode('utf8')

