# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import xlwt


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


class WeiboPipeline(object):
    print("---------开始保存！！")

    def __init__(self):
        self.row = 1
        obj = WeiboExcel()
        self.book, self.sheet = obj.creat_excel()

    def process_item(self, item, spider):
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
        self.close_file(item)

    def close_file(self, item):
        self.book.save('微博.csv')
        return item
