# 下载模块 负责下载页面
import requests
from ..http.response import Response


class Downloader:
    # 处理request请求、获取response并返回
    def get_response(self, request):

        if request.method.upper() == 'GET':
            resp = requests.get(request.url,
                                headers = request.headers,
                                params = request.params)

        elif request.method.upper() == 'POST':
            resp = requests.post(request.url,
                                headers=request.headers,
                                data=request.data,
                                params=request.params)

        else:
            raise Exception('only get and post method are available')

        return Response(resp.url,
                        resp.status_code,
                        resp.headers,
                        resp.content.decode())