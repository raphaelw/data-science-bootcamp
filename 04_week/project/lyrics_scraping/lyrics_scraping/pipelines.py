# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from hashlib import md5

class DuplicateSongsPipeline:
    def __init__(self):
        self.hashes_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        text = adapter['artist_found'].lower().strip() + adapter['song_title'].lower().strip()
        hash_sum = md5(text.encode("utf-16")).hexdigest()

        if hash_sum in self.hashes_seen:
            raise DropItem( 'Duplicate item found: "{}" "{}"'.format(adapter['artist_found'], adapter['song_title']) )
        else:
            self.hashes_seen.add(hash_sum)
            return item