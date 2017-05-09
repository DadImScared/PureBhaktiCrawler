
import re
import models

chapter_match = 'Chapter [a-zA-Z0-9]{1,2}\s'

with open("combined3.txt", "r", encoding='utf-8') as f:
    books = re.split(r'c:\\[a-zA-Z]+\\[a-zA-Z]+\\[a-zA-Z]+\\[a-zA-Z]+\\', f.read())

with open("combined3a.txt", "r", encoding='utf-8') as f2:
    search_books = re.split(r'c:\\[a-zA-Z]+\\[a-zA-Z]+\\[a-zA-Z]+\\[a-zA-Z]+\\', f2.read())


for uni_book, non_uni_book in zip(books, search_books):
    try:
        book = models.BookContent.create_book(title=re.match(r'^[a-zA-Z-_0-9\s&]+', non_uni_book).group(0))
    except IndexError:
        pass
    except AttributeError:
        pass
    else:
        models.FTSFullBook.create(item_id=book.id, content=non_uni_book, display_content=uni_book)
