# Scrapy settings for buyee project
import copy
from colorlog import ColoredFormatter
import scrapy.utils.log
import os

# Define relative paths to be used 
FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER_PATH = os.path.dirname(FOLDER_PATH)
GRANDPARENT_FOLDER_PATH = os.path.dirname(PARENT_FOLDER_PATH)

# Scrapy settings
BOT_NAME = "buyee"
SPIDER_MODULES = ["buyee.spiders"]
NEWSPIDER_MODULE = "buyee.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"

# Set up fake user agents
FAKEUSERAGENT_PROVIDERS = [
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # this is the first provider we'll try
    'scrapy_fake_useragent.providers.FakerProvider',  # if FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # fall back to USER_AGENT value
]

RANDOM_UA_PER_PROXY = True # Allows switch of header per proxy

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware' : 600,
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None, # Disabling to allow downloaded user agent to handle
    'scrapy.downloadermiddleware.retry.RetryMiddleware': None, # Disabling to allow downloaded user agent to handle
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 700, # Handles generating random useragent
    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 701, # Retrying user agents
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610, # Rotate proxy
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620 # Check not working proxies
}

# Set download timeout and retry options
DOWNLOAD_TIMEOUT = 4
RETRY_ENABLED = False
ROTATING_PROXY_PAGE_RETRY_TIMES = 100

# Specify path to the list of working proxies
ROTATING_PROXY_LIST_PATH = f'{GRANDPARENT_FOLDER_PATH}/ProxyScrapers/workingProxies.txt'

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

# Set up CSV feed export
FEEDS = {
    # location where to save results
    f'{PARENT_FOLDER_PATH}/auction.csv': {
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
        # Include headers in the CSV file if the file doesn't already exist
        'item_export_kwargs': {
           'include_headers_line': not os.path.exists(f'{PARENT_FOLDER_PATH}/auction.csv'),
        },
    },
}

# Enable autothrottle to automatically adjust the request rate based on server response time
AUTOTHROTTLE_ENABLED = True

#Disable the HTTP cache to ensure that the spider always fetches fresh data
HTTPCACHE_ENABLED = False

# Define the log formatter
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

# Apply the log formatter to Scrapy's log handler
_get_handler = copy.copy(scrapy.utils.log._get_handler)

def _get_handler_custom(*args, **kwargs):
    handler = _get_handler(*args, **kwargs)
    handler.setFormatter(color_formatter)
    return handler

scrapy.utils.log._get_handler = _get_handler_custom
