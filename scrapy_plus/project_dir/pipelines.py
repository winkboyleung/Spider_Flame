# from scrapy_plus.project_dir.spiders.xiangxi_public_spider import xiangxi_public_spider
# from scrapy_plus.project_dir.spiders.douban_spider import DoubanSpider
import time
import pymysql


class UniversalPipeline:

    # 这里有所不同的是，需要增加一个参数，也就是传入爬虫对象
    # 以此来判断当前item是属于那个爬虫对象的
    def process_item(self, item, cur, conn):
        try:
            if item['addr_id'] != '' and item['title'] != '' and item['url'] != '' and item['intro'] != '' and item['web_time'] != '' :
                item['web_time'] = int(time.mktime(time.strptime(item['web_time'], "%Y-%m-%d")))
            #     # 正式上传到服务器
            #     sql = "INSERT INTO ztb_info_25 (itemid,catid,title,style,addtime,adddate,areaid,status,linkurl,content) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
            #     'NULL', item['type_id'], item['title'], item['source_name'], item['time'], item['web_time'],
            #     item['addr_id'], 3, item['url'], pymysql.escape_string(item['intro']))

                # 单机测试
                sql = "INSERT INTO demo (catid,title,style,addtime,adddate,areaid,status,linkurl,content) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
                    item['type_id'], item['title'], item['source_name'], item['time'], item['web_time'],
                item['addr_id'], 3, item['url'], pymysql.escape_string(item['intro']))

                cur.execute(sql)
                cur.fetchall()
                conn.commit()

            else:
                try:
                    item['web_time'] = int(time.mktime(time.strptime(item['web_time'], "%Y-%m-%d")))
                except:
                    pass

                sql = "INSERT INTO ztb_error_infos (catid,title,style,addtime,adddate,areaid,status,linkurl,content) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
                    item['type_id'], item['title'], item['source_name'], item['time'], item['web_time'],
                    item['addr_id'], 3, item['url'], pymysql.escape_string(item['intro']))

                cur.execute(sql)
                cur.fetchall()
                conn.commit()

        except Exception as e:
            print("数据上传失败")
            print(item['title'])
            print(item['url'])
            print(e)


# class DoubanPipeline:
#     # 这里有所不同的是，需要增加一个参数，也就是传入爬虫对象
#     # 以此来判断当前item是属于那个爬虫对象的
#     def process_item(self, item, spider):
#         if spider.name == DoubanSpider.name:
#             print("豆瓣爬虫数据:", item)
#         return item


