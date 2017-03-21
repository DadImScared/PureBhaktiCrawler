
from flask import Blueprint, abort

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models

book_field = {
    'id': fields.Integer,
    'link': fields.String,
    'title': fields.String,
    'language': fields.String,
    'hits': fields.Integer
}


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
