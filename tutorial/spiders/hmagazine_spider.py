
import scrapy
import time


class HarmonistMagazineSpider(scrapy.Spider):
    name = 'hmagazine'
    start_urls = [
        'http://www.purebhakti.com/resources/ebooks-a-magazines-mainmenu-63/harmonist-magazine.html'
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'tutorial.pipelines.HarmonistMagazinePipeline': 300,
        }
    }

    def parse(self, response):
        for book in response.css('.-koowa-grid .docman_document'):
            yield {
                'link': response.urljoin(book.css('.docman_download__button::attr(href)').extract_first().strip()),
                'title': book.css('.koowa_header__title_link span::text').extract_first().strip()
            }

        next_page = None
        built_links = []
        text_list = []
        links_list = []
        links = response.css('.-koowa-grid .pagination-list')
        for list_item in links.css('li'):
            links_list.append(list_item)
        for item in links_list:
            text_list.append(item.css('a::text').extract())
        for x in links:
            built_links.append(x.css('li a::attr(href)').extract())
        try:
            int(text_list[-1][0])
        except ValueError:
            next_page = built_links[0][-1]
        if next_page is not None:
            print("new page \n\n\n\n")
            yield scrapy.Request(next_page, callback=self.parse)
