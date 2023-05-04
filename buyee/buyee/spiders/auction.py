import scrapy
from buyee.items import BuyeeItem

class AuctionSpider(scrapy.Spider):
    name = "auction"
    allowed_domains = ["buyee.jp"]
    start_urls = ["https://buyee.jp/item/search/category/2084005358?page=1"]

    def parse(self, response):
        for product in response.css('li.itemCard'):
            item = BuyeeItem()
            item['productName'] = product.css('img.g-thumbnail__image::attr(alt)').get()
            item['productLink'] = product.css('a::attr(href)').get()
            item['productImage'] = product.css('img.g-thumbnail__image::attr(data-src)').get() 
            item['productPrice'] = product.css('span.g-priceFx::text').get()
            
            yield item

        nextPageNum = response.css('a.arrow:contains(">")::attr("data-bind")').re_first(r'page":(\d+)')
        
        if (nextPageNum):
            nextPageUrl = f'https://buyee.jp/item/search/category/2084005358?page={nextPageNum}'
            self.logger.debug(f'URL WE ARE VISITING: {nextPageUrl}')
            yield scrapy.Request(nextPageUrl, callback=self.parse)
        else:
            self.logger.info("NO MORE PAGES")
        

