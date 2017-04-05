
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from resources.api_fields import hmonthly_field, magazine_search_field, magazine_snippet_field
import make_snippets


def add_magazine_info(magazine):
    magazine.title = magazine.hmonthly.title
    magazine.link = magazine.hmonthly.link
    return magazine


def add_snippets(magazine, query):
    magazine.title = magazine.hmonthly.title
    magazine.link = magazine.hmonthly.link
    magazine.content = make_snippets.make_snippets(magazine.content, query)
    return magazine


class HarmonistMonthlyList(Resource):
    def get(self):
        return {
            'magazines': [
                marshal(magazine, hmonthly_field)
                for magazine in models.HarmonistMonthly.select()
            ]
        }


class HarmonistMonthlySearch(Resource):
    def get(self, query):
        return {
            'magazines': [
                marshal(magazine, hmonthly_field)
                for magazine in models.HarmonistMonthly.select().where(
                    models.HarmonistMonthly.title.contains(query)
                )
            ]
        }


class HarmonistMonthlyContentSearch(Resource):
    def get(self, query):
        parser = reqparse.RequestParser()
        parser.add_argument('snippets')
        args = parser.parse_args()
        snippet = args.get('snippets')
        if snippet:
            return {
                'magazines': [
                    marshal(add_snippets(magazine, query), magazine_snippet_field)
                    for magazine in models.FTSHM.search_magazine(query)
                    ]
            }
        else:
            return {
                'magazines': [
                    marshal(add_magazine_info(magazine), magazine_search_field)
                    for magazine in models.FTSHM.search_magazine(query)
                ]
            }

hmonthly_api = Blueprint('resources.hmonthly', __name__)
api = Api(hmonthly_api)
api.add_resource(
    HarmonistMonthlyList,
    '/harmonistmonthly',
    endpoint="hmonthlys"
)
api.add_resource(
    HarmonistMonthlySearch,
    '/search/harmonistmonthly/<query>',
    endpoint='search_hmonthly'
)
api.add_resource(
    HarmonistMonthlyContentSearch,
    '/hmsearch/<query>',
    endpoint='search_hmonthly_content'
)
