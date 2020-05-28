# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
"""异步存入MYSQL"""
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose


def get_First(values):
    if values is not None:
        return values[0]


class WeiBoItemLoader(ItemLoader):
    default_output_processor = Compose(get_First)


class WeibospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    message_id = scrapy.Field()
    content = scrapy.Field()
    content1 = scrapy.Field()
    content2 = scrapy.Field()
    text = scrapy.Field()
    textLength = scrapy.Field()
    create_time = scrapy.Field()
    spider_time = scrapy.Field()
    user1 = scrapy.Field()
    message_url = scrapy.Field()
    longText1 = scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    attitudes_count = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into  t_public_opinion_realtime_weibo(title,message_id,content,content1,content2,text,textLength,create_time,spider_time,user1,message_url,longText1,reposts_count,comments_count,attitudes_count)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        parms = (self["title"], self["message_id"], self["content"], self["content1"], self["content2"], self["text"], self["textLength"], self["create_time"], self["spider_time"], self["user1"], self["message_url"], self["longText1"], self["reposts_count"], self["comments_count"], self["attitudes_count"])
        return insert_sql, parms


class WeiboCommentItem(scrapy.Item):
    title = scrapy.Field()
    message_id = scrapy.Field()
    text1 = scrapy.Field()
    user1 = scrapy.Field()
    user_url = scrapy.Field()
    emotion = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into  t_public_opinion_realtime_weibo_comment(title,message_id,text1,user1,user_url,emotion)
        values (%s,%s,%s,%s,%s,%s)
        """
        parms = (self["title"], self["message_id"], self["text1"], self["user1"], self["user_url"], self["emotion"])
        return insert_sql, parms
