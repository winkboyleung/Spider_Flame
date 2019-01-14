# item类用于封装爬虫提取出来的数据

class Item:

    def __init__(self, data):
        self.__data = data

    @property   # 让这个方法变成一个只读属性、用于保护数据
    def data(self):
        return self.__data