
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from resources.api_fields import hmonthly_field, magazine_search_field, magazine_snippet_field
from resources.utils import paginate, BaseResource, get_query
from make_snippets import make_snippets, can_make_snippet
from remove_words import remove_stop_words


def add_magazine_info(magazine):
    magazine.title = magazine.hmonthly.title
    magazine.link = magazine.hmonthly.link
    magazine.id = magazine.item_id
    return magazine


def add_snippets(magazine, query):
    magazine.id = magazine.item_id
    magazine.title = magazine.hmonthly.title
    magazine.link = magazine.hmonthly.link
    magazine.content, x = make_snippets(magazine.content, query)
    return magazine


class HarmonistMonthlyList(BaseResource):
    def get(self):
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=models.HarmonistMonthly.select(),
            next_url='hmonthly.hmonthlys',
            **args
        )
        return {
            'data': [
                marshal(magazine, hmonthly_field)
                for magazine in page_query.get_object_list()
            ],
            "nextPage": next_page
        }


class HarmonistMonthlySearch(BaseResource):
    def get(self, query):
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=get_query(models.HarmonistMonthly, query),
            next_url='hmonthly.search',
            query=query,
            **args
        )
        return {
            'data': [
                marshal(magazine, hmonthly_field)
                for magazine in page_query.get_object_list()
                ],
            "nextPage": next_page
        }
        # if len(query.split(" ")) > 1:
        #     return {
        #         'magazines': [
        #             marshal(magazine, hmonthly_field)
        #             for magazine in models.HarmonistMonthly.select().where(
        #                 models.HarmonistMonthly.title.regexp(
        #                     r"[-\s_]+".join(remove_stop_words(query.lower().split(" ")))
        #                 )
        #             )
        #         ]
        #     }
        # return {
        #     'magazines': [
        #         marshal(magazine, hmonthly_field)
        #         for magazine in models.HarmonistMonthly.select().where(
        #             models.HarmonistMonthly.title.contains(query)
        #         )
        #     ]
        # }


class HarmonistMonthlyContentSearch(BaseResource):
    def get(self, query):
        parse_copy = self.reqparse.copy()
        parse_copy.add_argument('snippets')
        args = parse_copy.parse_args()
        snippet = args.get('snippets')
        page_query, next_page = paginate(
            select_query=get_query(models.FTSHM, query),
            next_url='hmonthly.content_search',
            query=query,
            **args
        )
        return {
            'data': [
                marshal(add_snippets(magazine, query), magazine_snippet_field) if snippet else
                marshal(add_magazine_info(magazine), magazine_search_field)
                for magazine in page_query.get_object_list()
            ],
            "nextPage": next_page
        }
        # if snippet:
        #     add_mag = add_snippets
        #     return {
        #         'magazines': [
        #             marshal(add_snippets(magazine, query), magazine_snippet_field)
        #             for magazine in models.FTSHM.search_magazine(query)
        #         ]
        #     }
        # else:
        #     return {
        #         'magazines': [
        #             marshal(add_magazine_info(magazine), magazine_search_field)
        #             for magazine in models.FTSHM.search_magazine(query)
        #         ]
        #     }

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
    endpoint='search'
)
api.add_resource(
    HarmonistMonthlyContentSearch,
    '/hmsearch/<query>',
    endpoint='content_search'
)
