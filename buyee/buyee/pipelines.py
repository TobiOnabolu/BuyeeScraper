from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from deep_translator import GoogleTranslator
import logging
import csv
import requests
from re import sub

logger = logging.getLogger(__name__)

class TakeNewProductsPipeline:
    """
    A Scrapy pipeline that prevents duplicate product items from being scraped.

    Attributes
    ----------
    productIDs : set
        A set of product IDs that have already been scraped.

    Methods
    -------
    __init__()
        Initializes the pipeline by calling the getProducts method to retrieve previously scraped product IDs.
    process_item(item, spider)
        Processes each scraped product item, dropping it if its product ID has already been seen.
    getProducts()
        Retrieves previously scraped product IDs from a CSV file, returning them in a set.
    """
    def __init__(self):
        self.productIDs = self.getProducts()
    
    def process_item(self, item, spider):
        """
        Processes each scraped product item, dropping it if its product ID has already been seen.

        Parameters
        ----------
        item : scrapy.Item
            The product item being processed.
        spider : scrapy.Spider
            The spider that is doing the scraping.

        Returns
        -------
        item : scrapy.Item
            The original product item if it is new, otherwise raises a DropItem exception.
        """
        productID = item.get('productLink')
        
        # If not product id or we've seen this product before, drop it
        if productID is None or productID in self.productIDs:
            raise DropItem('Dropped product we have already seen')
        
        # Needed cause sometimes repeat products happen on further pages
        self.productIDs.add(productID)

        return item
            
    def getProducts(self):
        """
        Retrieves previously scraped product IDs from a CSV file, returning them in a set.

        Returns
        -------
        productIDs : set
            A set of product IDs that have already been scraped.
        """
        productIDs = set()

        try:
        # Try to load the CSV file into a Python set if it exists
            with open('auction.csv', 'r') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    productIDs.add(row['productLink'])

        except FileNotFoundError:
        # Handle the case where the file is missing
            print("Error: File 'auction.csv' not found.")

        return productIDs

class AddBaseUrlPipeline:
    """
    A Scrapy pipeline that adds the base URL to the 'productLink' field of scraped items.

    Attributes
    ----------
    None

    Methods
    -------
    process_item(item, spider)
        Adds the base URL to the 'productLink' field of the item and returns it.

    """
    def process_item(self, item, spider):
        """
        Adds the base URL to the 'productLink' field of the item and returns it.

        Parameters
        ----------
        item : scrapy.Item
            The scraped item.
        spider : scrapy.Spider
            The spider that scraped the item.

        Returns:
        --------
        scrapy.Item 
            The item with the base URL added to its 'productLink' field.

        """
        link = item.get('productLink')
        item['productLink'] = f'https://buyee.jp{link}'

        return item

class CleanPricePipeline:
    """
    A class used to clean product prices and convert them to USD

    Attributes
    ----------
    None

    Methods
    -------
    process_item(item, spider)
        A method that processes each item scraped and cleans the price field

    convertCurrency(value, currency)
        A method that converts a given value in a currency to USD using a currency conversion API
    """
    def process_item(self, item, spider):
        """
        A method that processes each item scraped and cleans the price field

        Parameters
        ----------
        item : scrapy.Item
            The item being scraped
        spider : scrapy.Spider
            The spider being used to scrape the item

        Returns
        -------
        scrapy.Item
            The item with the product price field cleaned and converted to USD
        """
        price = item.get('productPrice')

        value = ''
        currency = ''
        for char in price:
            if char.isalpha():
                currency += char
            elif char.isnumeric() or char in [',', '.']:
                value += char
        
        # Convert country code to currency code
        if currency == "CA": currency = "CAD"
        elif currency == "US": currency = "USD"

        item['productPrice'] = self.convertCurrency(value, currency)

        return item

    def convertCurrency(self, value, currency):
        """
        A method that converts a given value in a currency to USD using a currency conversion API

        Parameters
        ----------
        value : str
            The value of the product price in the given currency
        currency : str
            The currency of the product price

        Returns
        -------
        str
            The value of the product price converted to USD
        """
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
    """
    A Scrapy pipeline that translates the name of a product to English.

    Attributes
    ----------
    translator : GoogleTranslator
        A GoogleTranslator instance that is used for translating the product name.

    Methods
    -------
    process_item(item, spider):
        Processes the item, translating the product name to English.

    """
    def __init__(self):
        """
        Constructs a new TranslateNamePipeline object.

        """
        self.translator = GoogleTranslator(source='auto', target='en')
        
    def process_item(self, item, spider):
        """
        Processes the given item, translating the product name to English.

        Parameters
        ----------
        item : scrapy.Item
            A dictionary representing the item.
        spider : Scrapy Spider
            The Spider object that scraped the item.

        Returns
        -------
        scrapy.Item
            A dictionary representing the processed item.

        """
        name = item.get('productName')
        if name:
            try: 
                translated_name = self.translator.translate(name)
                item['productName'] = translated_name
            except:
                pass
            
        return item
