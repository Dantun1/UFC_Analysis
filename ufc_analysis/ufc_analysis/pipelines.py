import pymongo
import re
from itemadapter import ItemAdapter


class MongoPipeline:
    COLLECTION_NAME = "fighters"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        collection = self.db[self.COLLECTION_NAME]

        record = adapter.get("record")
        if record:
            valid_string = re.search(r"(\d+)-(\d+)-(\d+)", record)
            if valid_string:
                adapter["wins"] = int(valid_string.group(1))
                adapter["losses"] = int(valid_string.group(2))
                adapter["draws"] = int(valid_string.group(3))
            else:
                spider.logger.warning(f"Could not parse record: {record}")



        name = adapter.get("name")
        collection.update_one({"name": name},
                              {"$set": adapter.asdict()},
                              upsert=True)

        spider.logger.info(f"Upserted fighter: {name}")
        return item
