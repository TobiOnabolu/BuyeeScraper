# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field 

class BuyeeItem(Item):
    productLink = Field()
    productImage = Field() 
    productPrice = Field()
    productName = Field()
    productPrice = Field()



