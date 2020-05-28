# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
"""Pipline：异步插入"""
import pymysql
from twisted.enterprise import adbapi
# from scrapy.utils.project import get_project_settings
from weibospider import settings
import xlwt
from weibospider import items


class WeibospiderPipeline(object):
    def __init__(self):
        # settings = get_project_settings()
        dbparams = dict(
            host=settings.MYSQL_HOST,  # settings['MYSQL_HOST']
            db=settings.MYSQL_DB_NAME,  # settings['MYSQL_DBNAME']
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,  # settings['MYSQL_USER']
            passwd=settings.MYSQL_PASSWORD,  # settings['MYSQL_PASSWORD']
            charset='utf8mb4',  # 解决中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self.__dbpool = dbpool

    def connect(self):
        return self.__dbpool

    # mysql异步插入执行
    def process_item(self, item, spider):
        # print(str(item))
        query = self.__dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, parms = item.get_insert_sql()
        # print(parms)
        cursor.execute(insert_sql, parms)


class WeiboExcel(object):
    # def __init__(self):
    # self.row = 1
    def creat_excel(self):
        # 1.创建workbook对象
        book = xlwt.Workbook(encoding='utf-8')
        # 2.创建选项卡
        # 此处选项卡名字为：职位简介
        sheet = book.add_sheet('微博')
        # 3.添加头
        # 第一个参数是行，第二个参数是列，第三个参数是列的字段名
        sheet.write(0, 0, 'title')
        sheet.write(0, 1, 'message_id')
        sheet.write(0, 2, 'content')
        sheet.write(0, 3, 'content1')
        sheet.write(0, 4, 'content2')
        sheet.write(0, 5, 'textLength')
        sheet.write(0, 6, 'create_time')
        sheet.write(0, 7, 'spider_time')
        sheet.write(0, 8, 'user1')
        sheet.write(0, 9, 'message_url')
        sheet.write(0, 10, 'longText1')
        sheet.write(0, 11, 'reposts_count')
        sheet.write(0, 12, 'comments_count')
        sheet.write(0, 13, 'attitudes_count')
        return book, sheet


class Weibo1Excel(object):
    # def __init__(self):
    # self.row = 1
    def creat_excel(self):
        # 1.创建workbook对象
        book = xlwt.Workbook(encoding='utf-8')
        # 2.创建选项卡
        # 此处选项卡名字为：职位简介
        sheet = book.add_sheet('微博')
        # 3.添加头
        # 第一个参数是行，第二个参数是列，第三个参数是列的字段名
        sheet.write(0, 0, 'title')
        sheet.write(0, 1, 'message_id')
        sheet.write(0, 2, 'text1')
        sheet.write(0, 3, 'user1')
        sheet.write(0, 4, 'user_url')
        sheet.write(0, 5, 'emotion')
        return book, sheet


class WeiboPipeline(object):
    print("---------开始保存！！")

    def __init__(self):
        self.row = 1
        self.row1 = 1
        obj = WeiboExcel()
        obj1 = Weibo1Excel()
        self.weibo, self.sheet = obj.creat_excel()
        self.weibo1, self.sheet1 = obj1.creat_excel()

    def process_item(self, item, spider):
        print(str(item) + "啊" * 6)
        if isinstance(item, items.WeibospiderItem):
            self.sheet.write(self.row, 0, item['title'])
            self.sheet.write(self.row, 1, item['message_id'])
            self.sheet.write(self.row, 2, item['content'])
            self.sheet.write(self.row, 3, item['content1'])
            self.sheet.write(self.row, 4, item['content2'])
            self.sheet.write(self.row, 5, item['textLength'])
            self.sheet.write(self.row, 6, item['create_time'])
            self.sheet.write(self.row, 7, item['spider_time'])
            self.sheet.write(self.row, 8, item['user1'])
            self.sheet.write(self.row, 9, item['message_url'])
            self.sheet.write(self.row, 10, item['longText1'])
            self.sheet.write(self.row, 11, item['reposts_count'])
            self.sheet.write(self.row, 12, item['comments_count'])
            self.sheet.write(self.row, 13, item['attitudes_count'])
            self.row += 1
        elif isinstance(item, items.WeiboCommentItem):
            self.sheet1.write(self.row1, 0, item['title'])
            self.sheet1.write(self.row1, 1, item['message_id'])
            self.sheet1.write(self.row1, 2, item['text1'])
            self.sheet1.write(self.row1, 3, item['user1'])
            self.sheet1.write(self.row1, 4, item['user_url'])
            self.sheet1.write(self.row1, 5, item['emotion'])
            self.row1 += 1
        else:
            print("=============既不是微博也不是评论???(出问题了)==================")
        self.close_file(item)

    def close_file(self, item):
        self.weibo.save('data\\微博.xls')
        self.weibo1.save("data\\微博评论.xls")
        return item
