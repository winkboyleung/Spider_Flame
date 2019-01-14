# 响应类、构造响应请求
# 在下载器中构造response请求
import json
import re

from lxml import etree

class Response:

    def __init__(self, url, status_code, headers = {}, body = None, meta = {}):

        self.url = url
        self.status_code = status_code
        self.headers = headers
        self.body = body        # resp.content

        self.meta = meta

    def xpath(self, rule):
        html = etree.HTML(self.body)
        return html.xpath(rule)

    @property
    def json(self):
        return json.loads(self.body)

    def re_findall(self, pattern, data = None):
        if data is None:
            data = self.body
        return re.findall(pattern, data)