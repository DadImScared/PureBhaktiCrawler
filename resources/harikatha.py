
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models

hk_field = {
    'id': fields.Integer,
    'link': fields.String,
    'title': fields.String,
    'hits': fields.Integer
}

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
