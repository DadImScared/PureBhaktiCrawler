
import re
import os
import models
from fix_text import replace_unicode

dir_path = os.path.dirname(os.path.realpath(__file__))
book_dir = '{0}{1}allbooks{1}'.format(dir_path, os.path.sep)
files = os.listdir(book_dir)

# chapter_match = 'Chapter [a-zA-Z0-9]{1,2}\s'
#
# with open("combined3.txt", "r", encoding='utf-8') as f:
#     books = re.split(r'c:\\[a-zA-Z]+\\[a-zA-Z]+\\[a-zA-Z]+\\[a-zA-Z]+\\', f.read())
#
# with open("combined3a.txt", "r", encoding='utf-8') as f2:
#     search_books = re.split(r'c:\\[a-zA-Z]+\\[a-zA-Z]+\\[a-zA-Z]+\\[a-zA-Z]+\\', f2.read())
#
#
# for uni_book, non_uni_book in zip(books, search_books):
#     try:
#         book = models.BookContent.create_book(title=re.match(r'^[a-zA-Z-_0-9\s&]+', non_uni_book).group(0))
#     except IndexError:
#         pass
#     except AttributeError:
#         pass
#     else:
#         models.FTSFullBook.create(item_id=book.id, content=non_uni_book, display_content=uni_book)


page_split = r'[\s]{26}[0-9]{1,4}[^0-9/.-_\\|()\[\]]'

# with open("{}{}".format(book_dir, files[1]), "r", encoding='utf-8') as f:
#     book = f.read()
    # book = replace_unicode(book)
    # print(re.split(page_split, book)[2])


def get_book(path):
    try:
        with open(path, "r", encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(path)
        print("path not found")


def main():
    for file in files:
        uni_book = get_book("{}{}".format(book_dir, file))
        book = replace_unicode(uni_book)
        title = re.match(r'^[a-zA-Z-_0-9\s&]+', book).group(0)
        uni_book = re.split(page_split, uni_book)
        book = re.split(page_split, book)
        for i, (a, b) in enumerate(zip(uni_book, book)):
            new_page = models.BookPage.create_page(title=title, page=i+1, display_content=a)
            models.FTSBookPage.create(item_id=new_page.id, content=b)

#
#
# def split_pages(file):
#     with open(file, "r", encoding='utf-8') as f:
#         books = re.split(page_split, f.read())
#         return books
#
# for i, x in enumerate(split_pages("test1.txt")):
#     print("-----------------")
#     print(i + 1)
#     print(x)

if __name__ == '__main__':
    main()
