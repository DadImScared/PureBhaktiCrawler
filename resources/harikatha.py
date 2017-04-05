
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import requests
import models
from resources.api_fields import hk_field, magazine_search_field, magazine_snippet_field
import make_snippets


def add_magazine_info(magazine):
    magazine.title = magazine.harikatha.title
    magazine.link = magazine.harikatha.link
    return magazine


def add_snippets(magazine, query):
    magazine.title = magazine.harikatha.title
    magazine.link = magazine.harikatha.link
    magazine.content = make_snippets.make_snippets(magazine.content, query)
    return magazine


class HariKathaList(Resource):
    def get(self):
        return {
            'magazines': [
                marshal(magazine, hk_field)
                for magazine in models.HariKatha.select()
            ]
        }


class HariKathaSearch(Resource):
    def get(self, query):
        return {
            'magazines': [
                marshal(magazine, hk_field)
                for magazine in models.HariKatha.select().where(
                    models.HariKatha.title.contains(query)
                )
            ]
        }


class HariKathaContentSearch(Resource):
    def get(self, query):
        parser = reqparse.RequestParser()
        parser.add_argument('snippets')
        args = parser.parse_args()
        snippet = args.get('snippets')
        if snippet:
            return {
                'magazines': [
                    marshal(add_snippets(magazine, query), magazine_snippet_field)
                    for magazine in models.FTSHK.search_magazine(query)
                ]
            }
        else:
            return {
                'magazines': [
                    marshal(add_magazine_info(magazine), magazine_search_field)
                    for magazine in models.FTSHK.search_magazine(query)
                ]
            }

hk_api = Blueprint('resources.harikatha', __name__)
api = Api(hk_api)
api.add_resource(
    HariKathaList,
    '/harikatha',
    endpoint="harikathas"
)
api.add_resource(
    HariKathaSearch,
    '/search/harikatha/<query>',
    endpoint='search_hk'
)
api.add_resource(
    HariKathaContentSearch,
    '/hksearch/<query>',
    endpoint='hk_search_content'
)
