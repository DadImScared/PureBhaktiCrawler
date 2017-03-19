
import scrapy


class BhagavatPatrikaSpider(scrapy.Spider):
    name = 'bhagavatpatrika'
    start_urls = [
        # 'http://www.purebhakti.com/resources/ebooks-a-magazines-mainmenu-63/bhagavat-patrika.html'
        'http://www.purebhakti.com/resources/ebooks-a-magazines-mainmenu-63/bhagavat-patrika/year-1955-1959.html',
        'http://www.purebhakti.com/resources/ebooks-a-magazines-mainmenu-63/bhagavat-patrika/year-1960-1964.html',
        'http://www.purebhakti.com/resources/ebooks-a-magazines-mainmenu-63/bhagavat-patrika/year-1965-1969.html',
        'http://www.purebhakti.com/resources/ebooks-a-magazines-mainmenu-63/bhagavat-patrika/year-1970-1974.html',
        'http://www.purebhakti.com/resources/ebooks-a-magazines-mainmenu-63/bhagavat-patrika/year-1996-2000.html',
        'http://www.purebhakti.com/resources/ebooks-a-magazines-mainmenu-63/bhagavat-patrika/year-2001-2005.html',
        'http://www.purebhakti.com/resources/ebooks-a-magazines-mainmenu-63/bhagavat-patrika/year-2010-2015.html',

    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'tutorial.pipelines.BhagavatPatrikaPipeline': 300
        }
    }

    def parse(self, response):
        for item in response.css('form.-koowa-grid .docman_document'):
            yield {
                'link': response.urljoin(item.css('.docman_download__button::attr(href)').extract_first().strip()),
                'title': item.css('.koowa_header__item .koowa_header__title_link span::text').extract_first().strip()
            }
        pages = response.css('.pagination-list li')
        next_page = None
        if pages:
            last_item = pages[-1].css("a::text").extract_first()
            try:
                int(last_item)
            except ValueError:
                next_page = response.urljoin(pages[-1].css("a::attr(href)").extract_first())
                yield scrapy.Request(next_page, callback=self.parse)
