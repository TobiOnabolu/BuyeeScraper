import scrapy
from buyee.items import BuyeeItem

class AuctionSpider(scrapy.Spider):
    """
    A Scrapy spider that crawls Buyee's auction site and extracts information about products.

    Attributes
    ----------
    name : str
        The name of the spider.
    allowed_domains : list of str
        The domains that the spider is allowed to crawl.
    start_urls : list of str
        The URLs that the spider starts crawling from.

    Methods
    -------
    parse(response):
        Parses the HTML response to extract information about products and yields items.
    
    """
    name = "auction"
    allowed_domains = ["buyee.jp"]
    start_urls = ["https://buyee.jp/item/search/category/2084005358?page=1"]

    def parse(self, response):
        """
        Parses the HTML response to extract information about products and yields items.

        Parameters
        ----------
        response : scrapy.http.Response
            The HTML response to parse.

        Returns
        -------
        BuyeeItem
            An instance of BuyeeItem representing a product.

        """
        # Extract information about each product and yield an item for each one.
        for product in response.css('li.itemCard'):
            item = BuyeeItem()
            item['productName'] = product.css('div.itemCard__itemName a::text').get().strip()
            item['productLink'] = product.css('a::attr(href)').get()
            item['productImage'] = product.css('img.g-thumbnail__image::attr(data-src)').get() 
            item['productPrice'] = product.css('span.g-priceFx::text').get()
            yield item

        # Find the URL of the next page of search results, if it exists, and make a new request.
        nextPageNum = response.css('a.arrow:contains(">")::attr("data-bind")').re_first(r'page":(\d+)')
        if nextPageNum:
            nextPageUrl = f'https://buyee.jp/item/search/category/2084005358?page={nextPageNum}'
            self.logger.debug(f'URL WE ARE VISITING: {nextPageUrl}')
            yield scrapy.Request(nextPageUrl, callback=self.parse)
        else:
            self.logger.info("NO MORE PAGES")
