
import PyPDF2
import os
import requests

import models


dir_path = os.path.dirname(os.path.realpath(__file__))
base_pdf_dir = '{0}{1}pdfs{1}'.format(dir_path, os.path.sep)


def make_pdf(request):
    with open('{}mypdf.pdf'.format(base_pdf_dir), 'wb') as f:
        for chunk in request.iter_content(chunk_size=2000):
            f.write(chunk)


def get_text(file, book):
    pages = file.getNumPages()
    for num in range(pages):
        models.FTSBook.create(book_id=book.id, page=num+1, content=file.getPage(num).extractText())
    # make book.indexed = True don't forget book.save() after
    book.indexed = True
    book.save()


def read_pdf(file_path):
    file = PyPDF2.PdfFileReader(file_path)
    if file.isEncrypted:
        try:
            file.decrypt('')
        except NotImplementedError:
            return None
    return file


def delete_pdf(file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass


def main():
    books = models.Book.select().where((models.Book.language**'english') & (~(models.Book.indexed)))
    for book in books:
        url = book.link
        r = requests.get(url, stream=True)
        make_pdf(r)
        file = read_pdf(base_pdf_dir+'mypdf.pdf')
        if not file:
            delete_pdf(base_pdf_dir + 'mypdf.pdf')
            continue
        get_text(file, book)
        delete_pdf(base_pdf_dir+'mypdf.pdf')


if __name__ == '__main__':
    main()
