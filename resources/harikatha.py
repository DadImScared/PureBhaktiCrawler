
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import requests
import models
from resources.api_fields import hk_field, magazine_search_field, magazine_snippet_field
from make_snippets import make_snippets, can_make_snippet
from resources.utils import paginate, BaseResource, get_query, paginate_amount, get_page
from remove_words import remove_stop_words


def add_magazine_info(magazine):
    magazine.title = magazine.harikatha.title
    magazine.link = magazine.harikatha.link
    magazine.id = magazine.item_id
    return magazine


def add_snippets(magazine, query):
    magazine.title = magazine.harikatha.title
    magazine.link = magazine.harikatha.link
    snippets1, snippets2 = make_snippets(magazine.content, query)
    magazine.content = snippets1
    # magazine.content = magazine.content.split(" ")
    magazine.id = magazine.item_id
    return magazine


class HariKathaList(BaseResource):
    def get(self):
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=models.HariKatha,
            next_url='harikatha.harikathas',
            **args
        )
        return {
            'data': [
                marshal(magazine, hk_field)
                for magazine in page_query.get_object_list()
            ],
            'nextPage': next_page
        }


class HariKathaSearch(BaseResource):
    def get(self, query):
        print(query)
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=get_query(models.HariKatha, query),
            next_url='harikatha.search_hk',
            query=query,
            **args
        )
        return {
            'data': [
                marshal(magazine, hk_field)
                for magazine in page_query.get_object_list()
            ],
            "nextPage": next_page
        }
        # if len(query.split(" ")) > 1:
        #     return {
        #         'magazines': [
        #             marshal(magazine, hk_field)
        #             for magazine in models.HariKatha.select().where(
        #                 models.HariKatha.title.regexp(
        #                     r"[-\s_]+".join(remove_stop_words(query.lower().split(" ")))
        #                 )
        #             )
        #         ]
        #     }
        # return {
        #     'magazines': [
        #         marshal(magazine, hk_field)
        #         for magazine in models.HariKatha.select().where(
        #             models.HariKatha.title.contains(query)
        #         )
        #     ]
        # }


class HariKathaContentSearch(BaseResource):
    def get(self, query):
        parse_copy = self.reqparse.copy()
        parse_copy.add_argument('snippets')
        args = parse_copy.parse_args()
        snippet = args.get('snippets')
        page_query, next_page = paginate(
            select_query=get_query(models.FTSHK, query),
            next_url='harikatha.hk_search_content',
            query=query,
            **args
        )
        return {
            'data': [
                # marshal(
                #     add_snippets(magazine, query) if snippet else add_magazine_info(magazine),
                #     magazine_snippet_field if snippet else magazine_search_field)
                marshal(add_snippets(magazine, query), magazine_snippet_field) if snippet
                else marshal(add_magazine_info(magazine), magazine_search_field)
                for magazine in page_query.get_object_list()
            ],
            "nextPage": next_page
        }
        if snippet:
            return {
                'data': [
                    marshal(add_snippets(magazine, query), magazine_snippet_field)
                    for magazine in page_query.get_object_list()
                ],
                "nextPage": next_page
            }
        # else:
        #     return {
        #         'data': [
        #             marshal(add_magazine_info(magazine), magazine_search_field)
        #             for magazine in page_query.get_object_list()
        #         ],
        #         "nextPage": next_page
        #     }
        # parser = reqparse.RequestParser()
        # parser.add_argument('snippets')
        # args = parser.parse_args()
        # snippet = args.get('snippets')
        # if snippet:
        #     return {
        #         'magazines': [
        #             marshal(add_snippets(magazine, query), magazine_snippet_field)
        #             for magazine in models.FTSHK.search_magazine(query)
        #         ]
        #     }
        # else:
        #     return {
        #         'magazines': [
        #             marshal(add_magazine_info(magazine), magazine_search_field)
        #             for magazine in models.FTSHK.search_magazine(query)
        #         ]
        #     }

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
