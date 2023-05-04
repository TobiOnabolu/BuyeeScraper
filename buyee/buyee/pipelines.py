# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from deep_translator import GoogleTranslator
import logging
import csv
import requests
from re import sub
from decimal import Decimal

logger = logging.getLogger(__name__)

# Solves importing already seen products on the site
class TakeNewProductsPipeline:
    def __init__(self):
        self.productIDs = self.getProducts()
    def process_item(self, item, spider):
        productID = item.get('productLink')
        
        #If not product id or we've seen this product before, drop it
        if productID is None or productID in self.productIDs:
            raise DropItem('Dropped product we have already seen')
        
        # Needed cause sometimes repeat products happen on further pages
        self.productIDs.add(productID)

        return item
            
    
    def getProducts(self):
        productIDs = set()

        # Try to load the JSON file into a Python list if file has been created
        try:
            with open('auction.csv', 'r') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    productIDs.add(row['productLink'])

        except FileNotFoundError:
            # Handle the case where the file is missing
            print("Error: File 'auction.csv' not found.")

        return productIDs


class AddBaseUrlPipeline:
    def process_item(self, item, spider):
        link = item.get('productLink')
        item['productLink'] = f'https://buyee.jp{link}'

        return item
        

class CleanPricePipeline:
    def process_item(self, item, spider):
        price = item.get('productPrice')

        value = ''
        currency = ''
        for char in price:
            if char.isalpha():
                currency += char
            elif char.isnumeric() or char in [',', '.']:
                value += char
        if currency == "CA": currency = "CAD"
        elif currency == "US": currency = "USD"

        item['productPrice'] = self.convertCurrency(value, currency)

        return item
    
    def convertCurrency(self, value, currency):
        currency = currency.lower()
        url = f'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{currency}/usd.json'

        logger.debug(f'Getting price data for {currency}...')
        response = requests.get(url)

        if response.status_code != 200:
            logger.error(f'Failed to get price data from this url, {url}. \n Failed with status code {response.status_code}')
            raise DropItem
        
        decimalValue = float(sub(r'[^\d.]', '', value))
        data = response.json()
        rate = data['usd']
        price = '${:,.2f}'.format(decimalValue * rate)
        return price
        

        

        

        


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