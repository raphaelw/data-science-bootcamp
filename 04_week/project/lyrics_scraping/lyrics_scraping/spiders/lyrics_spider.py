import scrapy
from lyrics_scraping.items import LyricsScrapingItem

# Use of meta param: https://stackoverflow.com/questions/20663162/scrapy-passing-item-between-methods/20663659

class LyricsSpider(scrapy.Spider):
    name = "lyrics"

    def start_requests(self):
        artists = getattr(self, 'artists', None)
        if artists is not None:
            self.logger.info(f'Input artists "{artists}"')
            parsed_artists = ( artist.strip() for artist in artists.split(',') )
            for artist in parsed_artists:
                self.logger.info(f'Searching for artist "{artist}"')
                item = LyricsScrapingItem()
                item['artist_searched'] = artist

                # Example search type "Artist" with term "James Brown"
                # https://www.lyrics.com/serp.php?st=james+brown&qtype=2
                yield scrapy.FormRequest(url="https://www.lyrics.com/serp.php"
                                        ,formdata={'st': artist, 'qtype': '2'}
                                        ,method='GET'
                                        ,meta={'item': item}
                                        ,callback=self.parse_search_results)

    def parse_search_results(self, response):
        item = response.meta['item']

        element = response.css('a.name')
        if len(element) == 0:
            self.logger.info('No artist found for "{}"'.format(item['artist_searched']))
            return

        artist = element.css('::text').get()
        relative_artist_url = element.css('::attr(href)').get()

        self.logger.info(f'Found artist "{artist}"')
        item['artist_found'] = artist

        yield response.follow(relative_artist_url, self.parse_artist_page, meta={'item':item})

    def parse_artist_page(self, response):
        item = response.meta['item']

        for relative_song_url in response.css('div.tdata-ext table a::attr(href)').getall():
            yield response.follow(relative_song_url, self.parse_song_lyrics_page, meta={'item':item})

    def parse_song_lyrics_page(self, response):
        item = response.meta['item']

        if 'no-lyrics' in response.url: # check for 'https://www.lyrics.com/no-lyrics.php'
            self.logger.info(f'Invalid link led to "{response.url}"')
            return

        item['song_title'] = response.css('#lyric-title-text::text').get()
        #item['song_artists'] = response.css('hgroup .lyric-artist a::text').getall()[:-1]
        item['lyrics'] = ''.join( response.css('#lyric-body-text *::text').getall() )

        self.logger.info('Parsed lyrics "{}" "{}"'.format(item['artist_found'], item['song_title']))
        yield item