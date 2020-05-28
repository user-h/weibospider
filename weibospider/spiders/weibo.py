# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
import snownlp
from weibospider.items import WeiBoItemLoader, WeiboCommentItem, WeibospiderItem


class WeiboSpider(scrapy.Spider):
    # message = "范冰冰"
    print("-----------------------start---------------------------------------")
    name = 'weibo'
    allowed_domains = ['m.weibo.cn']
    start_urls = ['https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E8%8C%83%E5%86%B0%E5%86%B0&page_type=searchall']
    # Referer= {"Referer": "https://m.weibo.cn/p/searchall?containerid=100103type%3D1%26q%3D" + scrapy.quote("范冰冰")}

    def __init__(self, message,  *args, **kwargs):
        super(WeiboSpider, self).__init__(*args, **kwargs)
        self.message = message
        self.Referer = {"Referer": "https://m.weibo.cn/p/searchall?containerid=100103type%3D1%26q%3D"+str(self.message)}

    def start_requests(self):
        # print("-----------------------start_requests---------------------------------------")
        yield scrapy.Request(
            url="https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D"+str(self.message)+"&page_type=searchall&page=1",
            headers=self.Referer,
            meta={"page": 1, "keyword": self.message}
        )

    # 微博爬取parse函数：
    def parse(self, response):
        # print("-----------------------微博爬取parse函数---------------------------------------")
        base_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D"+str(self.message)+"&page_type=searchall&page="
        results = json.loads(response.text, encoding="utf-8")
        page = response.meta.get("page")
        keyword = response.meta.get("keyword")
        # 下一页
        next_page = results.get("data").get("cardlistInfo").get("page")
        if page != next_page:
            yield scrapy.Request(
                url=base_url+str(next_page),
                headers=self.Referer,
                meta={"page": next_page, "keyword": keyword}
            )
        result = results.get("data").get("cards")
        # 获取微博
        for i in result:
            card_type = i.get("card_type")
            show_type = i.get("show_type")
            # print(str(card_type) + " and " + str(show_type))
            # print(j)
            # 过滤
            if show_type == 1 and card_type == 9:
                # for i in j.get("card_group"):
                    # print(i)
                    reposts_count = i.get("mblog").get("reposts_count")
                    comments_count = i.get("mblog").get("comments_count")
                    attitudes_count = i.get("mblog").get("attitudes_count")
                    # 过滤到评论 转发 喜欢都为0 的微博
                    if reposts_count and comments_count and attitudes_count:
                        message_id = i.get("mblog").get("id")
                        status_url = "https://m.weibo.cn/comments/hotflow?id=%s&mid=%s&max_id_type=0"
                        # 返回微博评论爬取
                        yield scrapy.Request(
                            url=status_url % (message_id, message_id),
                            callback=self.commentparse,
                            meta={"keyword": keyword, "message_id": message_id}
                        )
                        title = keyword
                        status_url = "https://m.weibo.cn/status/%s"
                        # response1 = requests.get(status_url%message_id)
                        if i.get("mblog").get("page_info"):
                            content = i.get("mblog").get("page_info").get("page_title")
                            content1 = i.get("mblog").get("page_info").get("content1")
                            content2 = i.get("mblog").get("page_info").get("content2")
                        else:
                            content = ""
                            content1 = ""
                            content2 = ""
                        text = i.get("mblog").get("text").encode(encoding="utf-8")
                        textLength = i.get("mblog").get("textLength")
                        isLongText = i.get("mblog").get("isLongText")
                        create_time = i.get("mblog").get("created_at")
                        spider_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        user = i.get("mblog").get("user").get("screen_name")
                        message_url = i.get("scheme")
                        longText = i.get("mblog").get("longText").get("longTextContent") if isLongText else ""
                        reposts_count = reposts_count
                        comments_count = comments_count
                        attitudes_count = attitudes_count
                        weiboitemloader = WeiBoItemLoader(item=WeibospiderItem())
                        weiboitemloader.add_value("title", title)
                        weiboitemloader.add_value("message_id", message_id)
                        weiboitemloader.add_value("content", content)
                        weiboitemloader.add_value("content1", content1)
                        weiboitemloader.add_value("content2", content2)
                        weiboitemloader.add_value("text", text)
                        weiboitemloader.add_value("textLength", textLength)
                        weiboitemloader.add_value("create_time", create_time)
                        weiboitemloader.add_value("spider_time", spider_time)
                        weiboitemloader.add_value("user1", user)
                        weiboitemloader.add_value("message_url", message_url)
                        weiboitemloader.add_value("longText1", longText)
                        weiboitemloader.add_value("reposts_count", reposts_count)
                        weiboitemloader.add_value("comments_count", comments_count)
                        weiboitemloader.add_value("attitudes_count", attitudes_count)
                        print(weiboitemloader)
                        yield weiboitemloader.load_item()

    # scrapy爬取微博评论
    # 评论在微博正文中往下拉鼠标可以获得URL规律,下面是微博评论解析函数：
    def commentparse(self, response):
        # print("-----------------------scrapy爬取微博评论---------------------------------------")
        status_after_url = "https://m.weibo.cn/comments/hotflow?id=%s&mid=%s&max_id=%s&max_id_type=%s"
        message_id = response.meta.get("message_id")
        keyword = response.meta.get("keyword")
        results = json.loads(response.text, encoding="utf-8")
        if results.get("ok"):
            max_id = results.get("data").get("max_id")
            max_id_type = results.get("data").get("max_id_type")
            if max_id:
                # 评论10 个为一段，下一段在上一段JSON中定义：
                yield scrapy.Request(
                    url=status_after_url % (message_id, message_id, str(max_id), str(max_id_type)),
                    callback=self.commentparse,
                    meta={"keyword": keyword, "message_id": message_id})
            datas = results.get("data").get("data")
            for data in datas:
                text1 = data.get("text")
                like_count = data.get("like_count")
                user1 = data.get("user").get("screen_name")
                user_url = data.get("user").get("profile_url")
                emotion = snownlp.SnowNLP(text1).sentiments  # #利用SnowNLP函数进行情感分析
                weibocommentitem = WeiboCommentItem()
                weibocommentitem["title"] = keyword
                weibocommentitem["message_id"] = message_id
                weibocommentitem["text1"] = text1
                weibocommentitem["user1"] = user1
                weibocommentitem["user_url"] = user_url
                weibocommentitem["emotion"] = emotion
                yield weibocommentitem
