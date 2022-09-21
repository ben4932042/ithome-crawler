# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import pymongo


class IthomePipeline:
    def __init__(self):
        mongo_host = os.getenv("MONGO_HOST", "mongodb://localhost:27017")
        database = os.getenv("MONGO_COLLECTION", "ithome_ironman")
        self.db_client = pymongo.MongoClient(mongo_host)
        self.db = self.db_client[database]

    def process_item(self, item, spider):
        item = dict(item)
        source = item.pop('source')
        if source == "ithome_iron_man_item":
            item['_id'] = f"{item['user_id']}-{item['ironman_id']}-{item['article_id']}"
            self.db.devops_group.insert_one(item)
        elif source == "ithome_user_info_item":
            item['_id'] = item['user_id']
            self.db.user.insert_one(item)
        return item

    def close_spider(self, spider):
        self.db_client.close()
