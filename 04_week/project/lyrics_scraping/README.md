# Lyrics Scraper

Basic song lyrics scraper for https://www.lyrics.com/

## Usage

    scrapy crawl lyrics -L INFO -O lyrics_scraped.json -a artists="Elizabeth Shepherd, Zero 7"

Single Spider:

    scrapy runspider -L INFO -O lyrics.json lyrics_spider.py -a artists="Elizabeth Shepherd, Zero 7"