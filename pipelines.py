# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.utils.project import get_project_settings
from scrapy import logformatter as log
import pymongo


class MongoDBPipeline(object):
    def __init__(self, mongo_server, mongo_db, mongo_port, mongo_coll):
        self.mongo_server = mongo_server
        self.mongo_db = mongo_db
        self.mongo_port = mongo_port
        self.mongo_coll = mongo_coll

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_server=crawler.settings.get('MONGODB_SERVER'),
            mongo_db=crawler.settings.get('MONGODB_DB'),
            mongo_port=crawler.settings.get('MONGODB_PORT'),
            mongo_coll=crawler.settings.get('MONGODB_COLLECTION')
        )

    def process_item(self, item, spider):
        self.collection = self.db[self.mongo_coll]
        self.collection.insert_one(dict(item))
        return item

    def open_spider(self, spider):
        print(self.mongo_server, self.mongo_port, self.mongo_coll, str(self.mongo_db))
        self.client = pymongo.MongoClient(self.mongo_server, self.mongo_port)
        self.db = self.client.get_database(self.mongo_db)

    def close_spider(self, spider):
        self.client.close()
