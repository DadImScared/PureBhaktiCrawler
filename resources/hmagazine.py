
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from resources.api_fields import hmag_field
from resources.utils import paginate, BaseResource, get_query
from remove_words import remove_stop_words


class HarmonistMagazineList(BaseResource):
    def get(self):
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=models.HarmonistMagazine.select(),
            next_url='hmagazine.hmagazines',
            **args
        )
        return {
            'data': [
                marshal(magazine, hmag_field)
                for magazine in page_query.get_object_list()
            ],
            "nextPage": next_page
        }


class HarmonistMagazineSearch(BaseResource):
    def get(self, query):
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=get_query(models.HarmonistMagazine, query),
            next_url='hmagazine.search',
            query=query,
            **args
        )
        return {
            'data': [
                marshal(magazine, hmag_field)
                for magazine in page_query.get_object_list()
                ],
            "nextPage": next_page
        }
        # if len(query.split(" ")) > 1:
        #     return {
        #         'magazines': [
        #             marshal(magazine, hmag_field)
        #             for magazine in models.HarmonistMagazine.select().where(
        #                 models.HarmonistMagazine.title.regexp(
        #                     r"[-\s_]+".join(remove_stop_words(query.lower().split(" ")))
        #                 )
        #             )
        #         ]
        #     }
        # return {
        #     'magazines': [
        #         marshal(magazine, hmag_field)
        #         for magazine in models.HarmonistMagazine.select().where(
        #             models.HarmonistMagazine.title.contains(query)
        #         )
        #     ]
        # }

hmag_api = Blueprint('resources.hmagazine', __name__)
api = Api(hmag_api)
api.add_resource(
    HarmonistMagazineList,
    '/harmonistmagazine',
    endpoint="hmagazines"
)
api.add_resource(
    HarmonistMagazineSearch,
    '/search/harmonistmagazine/<query>',
    endpoint='search'
)
