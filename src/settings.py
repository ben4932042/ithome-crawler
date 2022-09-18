# Scrapy settings
from fake_useragent import UserAgent


BOT_NAME = 'src'

SPIDER_MODULES = ['src.spiders']
NEWSPIDER_MODULE = 'src.spiders'

ROBOTSTXT_OBEY = False
LOG_LEVEL = 'INFO'


CONCURRENT_REQUESTS = 3

DOWNLOAD_DELAY = 0

CONCURRENT_REQUESTS_PER_DOMAIN = 3
CONCURRENT_REQUESTS_PER_IP = 3

COOKIES_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": UserAgent().random,
}

ITEM_PIPELINES = {
    'src.pipelines.IthomePipeline': 300,
}

DOWNLOADER_MIDDLEWARES = {
    "scrapy_poet.InjectionMiddleware": 543,
}
SPIDER_MIDDLEWARES = {
    "scrapy_poet.RetryMiddleware": 275,
}

SPIDERMON_ENABLED = True

EXTENSIONS = {
    'spidermon.contrib.scrapy.extensions.Spidermon': 500,
}

SPIDERMON_SPIDER_CLOSE_MONITORS = (
    'src.monitors.SpiderCloseMonitorSuite',
)
