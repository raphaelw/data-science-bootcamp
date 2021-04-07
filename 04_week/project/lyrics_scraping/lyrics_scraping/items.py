# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LyricsScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    artist_searched = scrapy.Field()
    artist_found = scrapy.Field()
    song_title = scrapy.Field()
    lyrics = scrapy.Field()

    def __repr__(self):
        "https://stackoverflow.com/a/60622056"
        return '<LyricsScrapingItem "{}" "{}">'.format(self.get('artist_found'), self.get('song_title'))