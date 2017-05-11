
from flask import Blueprint, abort

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from resources.api_fields import book_field, book_search_field, book_snippet_field
from make_snippets import make_snippets, can_make_snippet, find_indexes


def add_book_info(book):
    book.title = book.books.title
    book.link = book.books.link
    return book


def add_snippet(book, query):
    book.title = book.fullbook.title
    book.content, x = make_snippets(book.content, query, display_content=book.display_content)
    indexes = []
    for snippet in x:
        indexes.append(find_indexes(snippet, query))
    book.displayContent = [i for i in indexes]
    return book


class Books(Resource):
    def get(self):
        return {
            'books': [
                marshal(book, book_field)
                for book in models.Book.select()
            ]
        }


class BookSearch(Resource):
    def get(self, query):
        return {
            'books': [
                marshal(book, book_field)
                for book in models.Book.select().where(models.Book.title.contains(query))
            ]
        }


class BookContentSearch(Resource):
    def get(self, query):
        return {
            'books': [
                marshal(add_snippet(book, query), book_snippet_field)
                for book in models.FTSFullBook.search_books(query) if can_make_snippet(book.content, query)
            ]
        }

book_api = Blueprint('resources.books', __name__)
api = Api(book_api)
api.add_resource(
    Books,
    '/books',
    endpoint='books'
)
api.add_resource(
    BookSearch,
    '/search/books/<query>',
    endpoint='booksearch'
)
api.add_resource(
    BookContentSearch,
    '/booksearch/<query>',
    endpoint='book_content_search'
)
