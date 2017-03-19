
# from scrapy.crawler import CrawlerProcess

import os
import time

dir_path = os.path.dirname(os.path.realpath(__file__))

from tutorial.spiders.bhagavat_patrika_spider import BhagavatPatrikaSpider
from tutorial.spiders.book_spider import BookSpider
from tutorial.spiders.hmonthly_spider import HarmonistMonthlySpider
from tutorial.spiders.hmagazine_spider import HarmonistMagazineSpider
from tutorial.spiders.harikatha_spider import HariKathaSpider


# process = CrawlerProcess()
#
# # process.crawl(HarmonistMagazineSpider)
# # process.crawl(HarmonistMonthlySpider)
# process.crawl(BookSpider)
# # process.crawl(BhagavatPatrikaSpider)
# # process.crawl(HariKathaSpider)
# process.start()


spiders = ['hmagazine', 'purebhakti', 'hmonthly', 'bhagavatpatrika', 'hknewsletter',
           'movies', 'audiolectures', 'bhajans']

for spider in spiders:
    os.system("scrapy crawl {}".format(spider))

# os.system('scrapy crawl hmonthly')
# print(dir_path)


# def run_spiders():
#     for spider in test_spiders:
#         process = CrawlerProcess()
#         process.crawl(spider)
#         process.start()
#
#         time.sleep(30)

# if __name__ == '__main__':
#     run_spiders()
