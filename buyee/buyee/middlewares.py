# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
from scrapy.exceptions import IgnoreRequest

logger = logging.getLogger(__name__)

class OutputProxyMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        proxy = request.meta.get('proxy')
        if proxy:
            spider.logger.debug('Using proxy: %s' % proxy)
        else:
            raise IgnoreRequest('No proxy is being used')
        return None

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)