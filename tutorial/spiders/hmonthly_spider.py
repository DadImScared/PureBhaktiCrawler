
import scrapy


class HarmonistMonthlySpider(scrapy.Spider):
    name = 'hmonthly'
    start_urls = [
        'http://www.purebhakti.com/resources/harmonist-monthly.html'
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'tutorial.pipelines.HarmonistMonthlyPipeline': 300,
        }
    }

    def parse(self, response):
        for item in response.css('.bloghmonthly .items-row'):
            yield {
                'link': response.urljoin(item.css('h2 a::attr(href)').extract_first().strip()),
                'title': item.css('h2 a::text').extract_first().strip()
            }
        next_page = response.css('.pagination-next a::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
