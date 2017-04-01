
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from resources.api_fields import hk_field, magazine_search_field


def add_magazine_info(magazine):
    magazine.title = magazine.harikatha.title
    magazine.link = magazine.harikatha.link
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
