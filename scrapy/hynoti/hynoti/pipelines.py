from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class HynotiPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db 

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        collection_name = type(item).__name__.lower().replace('item', '') + '_notice'
        collection = self.db[collection_name]
        collection.create_index('title', name='unique_title', unique=True)
        
        try:
            collection.insert_one(ItemAdapter(item).asdict())
        except DuplicateKeyError:
            pass

        return item

    def close_spider(self, spider):
        self.client.close()