from scrapy_plus.conf.settings import redis_ip

def add_proxies_ip(request):
    # 从列表中获取ip
    ip_pool = redis_ip.lindex("ip_pool", 0)
    # ip_pool = '175.167.22.29:35771'

    # 获取请求的协议头是http还是https，根据该请求头使用相应的代理ip
    HTTP = request.url.split('://')[0]
    if HTTP == 'http':
        # ip = 'http://' + random.choice(ip_pool).decode('utf-8')
        ip = 'http://' + ip_pool.decode('utf-8')
        # request.meta['proxy'] = ip
        # print(ip)
        ip = {'http' : ip}
    else:
        # ip = 'https://' + random.choice(ip_pool).decode('utf-8')
        ip = 'https://' + ip_pool.decode('utf-8')
        # request.meta['proxy'] = ip
        ip = {'https' : ip}

    # print('===========================================')
    # print(request.url)
    # print(ip)
    # print('===========================================')
    return ip