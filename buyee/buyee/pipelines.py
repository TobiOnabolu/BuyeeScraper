# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from googletrans import Translator


class BuyeePipeline:
    def process_item(self, item, spider):
        return item



class TranslateNamePipeline:
    def __init__(self):
        self.translator = Translator()
        
    def process_item(self, item, spider):
        name = item.get('productName')
        if name:
            translated_name = self.translator.translate(name, dest='en').text
            item['productName'] = translated_name
        return item