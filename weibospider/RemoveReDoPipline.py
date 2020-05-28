
class RemoveReDoPipline(object):
    def __init__(self, host):
        self.conn = MySQLdb.connect(host, 'root', 'root', 'meltmedia', charset="utf8", use_unicode=True)
        self.redis_db = redis.Redis(host='127.0.0.1', port=6379, db=0)
        sql = "SELECT message_id FROM t_public_opinion_realtime_weibo"
        # 获取全部的message_id,这是区分是不是同一条微博的标识
        df = pd.read_sql(sql, self.conn)
        # 全部放入Redis中
        for mid in df['message_id'].get_values():
            self.redis_db.sadd("weiboset", mid)

    # 获取setting文件配置
    @classmethod
    def from_settings(cls,setting):
        host=setting["MYSQL_HOST"]
        return cls(host)

    def process_item(self, item, spider):
        # 只对微博的Item过滤，微博评论不需要过滤直接return：
        if isinstance(item, WeibopachongItem):
            if self.redis_db.sadd("weiboset",item["message_id"]):
                return item
            else:
                print("重复内容：", item['text'])
                raise DropItem("same title in %s" % item['text'])
        else:
            return item
