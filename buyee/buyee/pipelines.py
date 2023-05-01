# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from deep_translator import GoogleTranslator
import json

# Solves importing already seen products on the site
class TakeNewProductsPipeline:
    def __init__(self):
        self.productIDs = self.getProducts()

    def process_item(self, item, spider):
        productID = item.get('productLink')
        
        #If not product id or we've seen this product before, drop it
        if productID is None or productID in self.productIDs:
            raise DropItem('Dropped product we have already seen')
        
        # Not really needed since scrapy will add this id to json file at end of execution but good countermeasure
        self.productIDs.add(productID)

        return item
            
    
    def getProducts(self):
        productIDs = set()

        # Try to load the JSON file into a Python list if file has been created
        try:
            with open('auction.jsonl', 'r') as f:
                for line in f:
                    item = json.loads(line)
                    productIDs.add(item['productLink'])

        except FileNotFoundError:
            # Handle the case where the file is missing
            print("Error: File 'auction.jsonl' not found.")

        return productIDs






        

class CleanPricePipeline:
    def process_item(self, item, spider):
        price = item.get('productPrice')
        if price:
            item['productPrice'] = price[1:-1]

        return item

class TranslateNamePipeline:
    def __init__(self):
        self.translator = GoogleTranslator(source='auto', target='en')
        
    def process_item(self, item, spider):
        name = item.get('productName')
        if name:
            try: 
                translated_name = self.translator.translate(name)
                item['productName'] = translated_name
            except:
                pass
            

        return item