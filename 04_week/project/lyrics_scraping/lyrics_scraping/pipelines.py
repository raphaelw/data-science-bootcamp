# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from hashlib import md5
import re

def normalize_song_title(title):
    "In the Waiting Line [Live] -> In the Waiting Line"
    return re.sub(r"\[[^\]]*\]", '', title).strip()

class DuplicateSongsPipeline:
    def __init__(self):
        self.hashes_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        song_title_normalized = normalize_song_title(adapter['song_title'])
        text = adapter['artist_found'].lower().strip() + song_title_normalized.lower().strip()
        hash_sum = md5(text.encode("utf-16")).hexdigest()

        if hash_sum in self.hashes_seen:
            raise DropItem( 'Duplicate item found: "{}" "{}"'.format(adapter['artist_found'], adapter['song_title']) )
        else:
            self.hashes_seen.add(hash_sum)
            return item