
import scrapy


class MovieSpider(scrapy.Spider):
    name = 'movies'
    start_urls = [
        'http://purebhakti.tv/movies.htm'
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'tutorial.pipelines.MoviePipeline': 300,
        }
    }

    def parse(self, response):
        for item in response.css('div a'):
            yield {
                'link': item.css('::attr(href)').extract_first().strip(),
                'title': item.css('::text').extract_first().strip().replace('\t', '').replace('\n', '')
            }
