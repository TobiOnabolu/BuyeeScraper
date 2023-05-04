# Scrapy settings for buyee project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import copy
from colorlog import ColoredFormatter
import scrapy.utils.log
import os

color_formatter = ColoredFormatter(
    (
        '%(log_color)s%(levelname)-5s%(reset)s '
        '%(green)s[%(asctime)s]%(reset)s'
        '%(white)s %(name)s %(funcName)s %(bold_purple)s:%(lineno)d%(reset)s '
        '%(log_color)s%(message)s%(reset)s'
    ),
    datefmt='%y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'blue',
        'INFO': 'bold_cyan',
        'WARNING': 'yellow',
        'ERROR': 'bg_bold_red',
        'CRITICAL': 'red,bg_white',
    }
)

_get_handler = copy.copy(scrapy.utils.log._get_handler)

def _get_handler_custom(*args, **kwargs):
    handler = _get_handler(*args, **kwargs)
    handler.setFormatter(color_formatter)
    return handler
scrapy.utils.log._get_handler = _get_handler_custom

BOT_NAME = "buyee"

SPIDER_MODULES = ["buyee.spiders"]
NEWSPIDER_MODULE = "buyee.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"

FAKEUSERAGENT_PROVIDERS = [
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # this is the first provider we'll try
    'scrapy_fake_useragent.providers.FakerProvider',  # if FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # fall back to USER_AGENT value
]

RANDOM_UA_PER_PROXY = True # Allows switch of header per proxy


# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware' : 600,
    'buyee.middlewares.OutputProxyMiddleware': 630, # Checking if we are using a different proxy
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None, # Disabling to allow downloaded user agent to handle
    'scrapy.downloadermiddleware.retry.RetryMiddleware': None, # Disabling to allow downloaded user agent to handle
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 700, # Handles generating random useragent
    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 701, # Retrying user agents
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610, # Rotate proxy
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620 # Check not working proxies
}

DOWNLOAD_TIMEOUT = 4
RETRY_ENABLED = False
ROTATING_PROXY_PAGE_RETRY_TIMES = 100
# Proxies to use
ROTATING_PROXY_LIST_PATH = 'proxies.txt'

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "buyee.pipelines.TakeNewProductsPipeline": 290, # Add only new products to our db
    'buyee.pipelines.TranslateNamePipeline': 297, # Translate japanese names to english
    'buyee.pipelines.CleanPricePipeline' : 295, # Sanitizing price data
    'buyee.pipelines.AddBaseUrlPipeline' : 293, # Adding base url to productlinks
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

FEEDS = {
    # location where to save results
    'auction.csv': {
        # file format like json, jsonlines, xml and csv
        'format': 'csv',
        # use unicode text encoding:
        'encoding': 'utf8',
        # whether to export empty fields
        'store_empty': False,
        # we can also restrict to export only specific fields like: title and votes:
        #'fields': ["title", "votes"],
        # every run will create new file, if False is set every run will append results to the existing ones
        'overwrite': False,
        'item_export_kwargs': {
           'include_headers_line': not os.path.exists('auction.csv'),
        },
    },
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
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
HTTPCACHE_ENABLED = False
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
    #"buyee.middlewares.BuyeeSpiderMiddleware": 543,
    #'scrapy_auto_trans.spidermiddlewares.autotrans.GoogleAutoTranslationMiddleware': 701,
    #'scrapy_deltafetch.DeltaFetch': 100 Not needed because each request to a url is not unique for the products displayed on that url
#}
#DELTAFETCH_ENABLED = True