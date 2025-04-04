# pipelines.py
import csv
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AlltimePipeline:
    def process_item(self, item, spider):
        return item



class CsvCustomPipeline:
    def open_spider(self, spider):
        self.file = open('output/chokolat.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file, fieldnames=['product', 'price', 'link', 'img'], delimiter=';')
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item