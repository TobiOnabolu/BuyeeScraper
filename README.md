# BuyeeScraper

A webscraper that collects product information from Buyees Auction site for Male Jewlery.

## Installation
* Fork and clone the repo onto your computer using ```bash git clone --recurse-submodules <git url to project> ```
* From the command line cd into root project folder and use this command to install dependencies. ```bash pip3 install -r requirements.txt ```

## Usage
### Step 1: Gather Proxies
* Before using the spider a list of proxies need to be gathered first. This can be done by running the Submodule ProxyScrapers
* To run the submodule cd into the ProxyScrapers directory and follow the usage steps outlined here: [ProxyScrapers](https://github.com/TobiOnabolu/ProxyScrapers)
    * Upon completion, a list of proxies will be created and stored in a .txt file in the BuyeeScraper directory

### Step 2: Run Spider
* From the command line cd into the root buyee folder. 
* Run ```bash scrapy crawl auction ```
* This command will start the spider and begin scraping the buyee Mens jewlery auction site. The spider will rotate proxies with each request and retry requests that failed due to failing proxies. The final result will be outputted to ```bash auction.csv ```

## Additional Comments
* On each new spider run, the list of already seen products from ```bash auction.csv ``` will be loaded to a set to ensure that we only collect new products that have not been seen
* In the settings file these are some important configs:
    *  ```bash DOWNLOAD_TIMEOUT ``` has been configured to 4 seconds. Meaning the spider will wait 4 seconds for attempting to retrieve a response from buyee.jp with a proxy. This ensure failing proxies do not waste alot of time and are quickly disposed if they aren't working.
    * ```bash RETRY_ENABLED ``` has been set to ```bash FALSE ``` becuase ```bash     scrapy_fake_useragent.middleware.RetryUserAgentMiddleware ``` is responsible for handling the retry logic.
    * ```bash ROTATING_PROXY_PAGE_RETRY_TIMES ``` has been set to 100 to allow multiple retries, since free proxies tend to fail alot, especially if we have a short timeout. Tip: It's better to have a small list of really good free proxies.

## Future Extensions

* Handle currency types with symbols and no letters i.e. '(928.45฿)'

* Extend BuyeeItem class to have source field where its either auction, shop, or mercari

* Add a new expiry field for all item so auction items can have an expiry date

* Make spiders for shopping - their output should go to its own csv

* Make spider for mercari - their output should go to its own csv

* Make script to combine all 3 csvs under one

### Extend to these websites

#### Auction site
* [Womens Jewlery](https://buyee.jp/item/search/category/2084005359?page=1&vic=service_page_search)
* [Mens Jewlery](https://buyee.jp/item/search/category/2084005358?page=1&vic=service_page_search) DONE

#### Shopping Site
* [Womens Jewlery](https://buyee.jp/category/yahoo/shopping/1591)
* [Mens Jewlery](https://buyee.jp/category/yahoo/shopping/1605)

#### Mercari Site
* [Jewlery](https://buyee.jp/mercari/search?category_id=914)