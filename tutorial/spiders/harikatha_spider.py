
import scrapy


class HariKathaSpider(scrapy.Spider):
    name = "hknewsletter"

    custom_settings = {
        'ITEM_PIPELINES': {
            'tutorial.pipelines.HariKathaPipeline': 300,
        }
    }

    def start_requests(self):
        urls = [
            'http://www.purebhakti.com/'
            # 'http://quotes.toscrape.com/page/1/',
            # 'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('.blog-featured .items-row .item h2'):
            yield {
                'link': response.urljoin(quote.css('a::attr(href)').extract_first().strip()),
                'title': quote.css('a::text').extract_first().strip(),

            }

        next_page = response.css('.blog-featured .pagination-next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
