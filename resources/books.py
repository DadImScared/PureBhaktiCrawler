
from flask import Blueprint, abort, request, url_for
import math
from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
from playhouse.flask_utils import PaginatedQuery
import models
from resources.api_fields import book_field, book_search_field, book_snippet_field
from resources.utils import paginate, BaseResource, get_query
from make_snippets import make_snippets, can_make_snippet, find_indexes
from remove_words import remove_stop_words


def add_book_info(book):
    book.title = book.books.title
    book.link = book.books.link
    return book


def add_snippet(book, query):
    book.id = book.item_id
    book.title = book.pages.title
    book.indexes = find_indexes(book.content, query)
    book.page = book.pages.page
    book.content = book.pages.display_content
    return book


class Books(BaseResource):
    def get(self):
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=models.Book.select(),
            next_url='books.books',
            **args
        )
        return {
            'data': [
                marshal(book, book_field)
                for book in page_query.get_object_list()
            ],
            'nextPage': next_page
        }


class BookSearch(BaseResource):
    def get(self, query):
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=get_query(models.Book, query),
            next_url='books.search',
            **args,
        )
        return {
            'data': [
                marshal(book, book_field)
                for book in page_query.get_object_list()
            ],
            'nextPage': next_page
        }


class BookContentSearch(BaseResource):
    def get(self, query):
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=get_query(models.FTSBookPage, query),
            next_url='books.content_search',
            query=query,
            **args
        )
        return {
            'data': [
                marshal(add_snippet(book, query), book_snippet_field)
                for book in page_query.get_object_list()
            ],
            "nextPage": next_page
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
    endpoint='search'
)
api.add_resource(
    BookContentSearch,
    '/booksearch/<query>',
    endpoint='content_search'
)
