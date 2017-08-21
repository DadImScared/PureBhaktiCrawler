
import scrapy


class HK1996Spider(scrapy.Spider):
    """Crawler for 1996"""
    name = "1996"
    start_urls = ['https://bhaktabandhav.org/category/srila-gurudeva']
    custom_settings = {
        'ITEM_PIPELINES': {
            'tutorial.pipelines.HK1996Pipeline': 300,
        }
    }
