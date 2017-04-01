
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs

import models

# url = models.HariKatha.get(models.HariKatha.id == 5).link
# print(url)


def index_content():
    magazines = models.HarmonistMonthly.select().where(~models.HarmonistMonthly.indexed)
    for item in magazines:
        url = item.link
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            soup = bs(urlopen(req), 'html.parser')
        except UnicodeEncodeError:
            continue
        article = soup.find('article', class_='item-pagehmonthly')
        content = article.find_all('p')
        models.FTSHM.create(item_id=item.id, content=" ".join([x.get_text() for x in content]))
        item.indexed = True
        item.save()


if __name__ == '__main__':
    index_content()
