# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class BooksPipeline:
    def process_item(self, item, spider):
        # Check if all items have BookTitle, BookPrice, BookDetailsPageUrl and BookImageUrl
        expected_fields = [
            "BookTitle",
            "BookPrice",
            "BookDetailsPageUrl",
            "BookImageUrl",
        ]
        for field in expected_fields:
            if not field in item:
                message = f"Missing field '{field}' in item: {item}"
                raise DropItem(message)
        return item
