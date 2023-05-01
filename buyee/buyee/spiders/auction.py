import scrapy


class AuctionSpider(scrapy.Spider):
    name = "auction"
    allowed_domains = ["buyee.jp"]
    start_urls = ["http://buyee.jp/?page=1"]

    def parse(self, response):
        pass
