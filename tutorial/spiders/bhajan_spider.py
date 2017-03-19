
import scrapy

mp3_list = ['mp3', 'MP3', 'Mp3', 'mP3', 'WAV', 'wav']

class BookSpider(scrapy.Spider):
    name = 'bhajans'
    start_urls = ['http://sbnmcd.org/extradisk/bhajan/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'tutorial.pipelines.BhajansPipeline': 300,
        }
    }

    def parse(self, response):

        for directory in response.css('.folder_bg a'):
            yield scrapy.Request(
                response.urljoin(directory.css("::attr(href)").extract_first()),
                callback=self.parse_directory,
                meta={'category': directory.css("::text").extract_first()}
            )

        for item in response.css('tr a'):
            if item.css("::attr(href)").extract_first()[-3:] in mp3_list:
                yield {
                    'link': response.urljoin(item.css("::attr(href)").extract_first()),
                    'title': item.css("::text").extract_first(),
                    'category': 'general'
                }

    def parse_directory(self, response):
        category = response.meta['category']

        for item in response.css('tr a'):
            if item.css("::attr(href)").extract_first()[-3:] in mp3_list:
                yield {
                    'link': response.urljoin(item.css("::attr(href)").extract_first()),
                    'title': item.css("::text").extract_first(),
                    'category': category
                }
