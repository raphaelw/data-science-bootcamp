import scrapy

# run: scrapy runspider -L INFO -O scraped_data.json lyrics_spider.py

class LyricsSpider(scrapy.Spider):
    name = "lyrics"

    def start_requests(self):
        urls = [
            'https://www.lyrics.com/artist/Zero-7/476853',
            'https://www.lyrics.com/artist/Stevie-Wonder/139462',
            'https://www.lyrics.com/artist/Melody-Gardot/865096'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_artist_page)

    def parse_artist_page(self, response):
        item = {}

        artist_name = response.css('p.artist a::text').get()
        song_urls = response.css('div.tdata-ext table a::attr(href)').getall()

        item['artist'] = artist_name

        self.logger.info('Parsed page of ' + artist_name)
        for relative_url in song_urls:
            yield response.follow(relative_url, self.parse_song_lyrics_page, meta={'item':item})

    def parse_song_lyrics_page(self, response):
        item = response.meta['item']

        item['title'] = response.css('#lyric-title-text::text').get()
        item['lyrics'] = ''.join( response.css('#lyric-body-text *::text').getall() )

        self.logger.info('Parsed lyrics "{}" "{}"'.format(item['artist'], item['title']))
        yield item