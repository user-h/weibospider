from scrapy import cmdline

# 执行book.py里的name
message = "剑网三"
cmdline.execute(f"scrapy crawl weibo -a message=${message}".split())
# scrapy crawl xxxSpider -a start_urls=xxxxxx -a number=number
# execute(['scrapy', 'crawl', 'xxxSpider',"-a","start_urls=xxxx","-a","number=666"])

# 保存Excel中（.csv格式）
# cmd命令直接保存（注意：必须进入scrapy虚拟环境中！保存后表格中有空行！）：
# scrapy crawl 项目名 -o 文件名.csv -s FEED_EXPORT_ENCIDING=utf-8
