
import scrapy
import re
import urllib.request


class BookSpider(scrapy.Spider):
    name = 'audiolectures'
    start_urls = ['http://sbnmcd.org/All_mp3/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'tutorial.pipelines.AudioLecturesPipeline': 300,
        }
    }

    def parse(self, response):
        for item in response.css('td a'):
            if '.' not in item.css('::attr(href)').extract_first():
                directory = item.css("::attr(href)").extract_first()
                yield scrapy.Request(response.urljoin(directory), callback=self.parse_directories)
            elif '.mp3' in item.css('::attr(href)').extract_first():
                yield {
                    'link': response.urljoin(item.css("::attr(href)").extract_first()),
                    'title': item.css('::text').extract_first(),
                    'category': 'general'
                }

    def parse_directories(self, response):
        mp3_list = ['mp3', 'MP3', 'Mp3', 'mP3', 'WAV', 'wav']
        category = response.url.rsplit('/', 1)[0].rsplit('/', 1)[1]
        if re.match(r'^[0-9]{4}-?[0-9]{0,4}$', category):
            category = 'general'
        category = urllib.request.unquote(category)
        category = re.sub(r'^[0-9]{1,}', '', category)
        for item in response.css('a'):
            if item.css('::attr(href)').extract_first()[-3:] in mp3_list:
                yield {
                    'link': response.urljoin(item.css("::attr(href)").extract_first()),
                    'title': item.css("::text").extract_first(),
                    'category': category.strip()
                }
