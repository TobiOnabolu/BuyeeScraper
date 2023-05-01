# Scrapy commands

scrapy shell -s USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'  https://buyee.jp/item/search/category/2084005358

## Create project
scrapy startproject projectfoldername

## Run spider option 1 if spider not part of project
scrapy runspider spiderfile.py -O jsonfilename.json

## Run spider (from buyee directory)
scrapy crawl spidername -O jsonfilename.json

## css select href
a::attr(href)

## css select text from a element
div::text

## Make spider template
scrapy genspider example