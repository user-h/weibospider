# -*- coding: utf-8 -*-

# Scrapy settings for weibospider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'weibospider'

SPIDER_MODULES = ['weibospider.spiders']
NEWSPIDER_MODULE = 'weibospider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'weibospider (+http://www.yourdomain.com)'
# 设置 用户代理
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"

# Obey robots.txt rules
# 不遵守 君子协议
ROBOTSTXT_OBEY = False
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 批量延迟时间
DOWNLOAD_DELAY = 3
#DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
   # 'cookie': 'ALF=1590839772; SCF=ApWjXu94Gv1E5APKzI4ZHkWZ-gZ6Hc6IHRLdmtE0dhs1VOHcruehXgwAXhASWuYttuDDMy2Fok99WMZEo5zx9rg.; SUB=_2A25zrsyNDeRhGeBO7FoW8yjFyj6IHXVRUNTFrDV6PUNbktAKLUemkW1NRaNzmRqMlVKKrChuVnNgDMYRuOPk6X1m; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWId.p_JJbZo._Ejp2f38jK5JpX5KMhUgL.Foq7S0nNe0q4eKz2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcehMRS0ec1K2E; SUHB=06ZFjsLWpN2PhY; _WEIBO_UID=6078736912; MLOGIN=1; _T_WM=69322172342; XSRF-TOKEN=3e1f18; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E7%25BD%2597%25E5%25BF%2597%25E7%25A5%25A5',
   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'weibospider.middlewares.WeibospiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'weibospider.middlewares.WeibospiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 保存文件
    'weibospider.pipelines.WeiboPipeline': 300,
    # 保存到Mysql(但是很奇怪为什么不能同时保存)
    # 'weibospider.pipelines.WeibospiderPipeline': 300,
    # 数越小优先级越高
    # 'weibospider.pipelines.RemoveReDoPipline': 100,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# mysql数据库配置
MYSQL_HOST = '127.0.0.1'
MYSQL_DB_NAME = 'myweibo'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456789'
