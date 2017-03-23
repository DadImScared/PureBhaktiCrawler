
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from resources.api_fields import hmag_field


class HarmonistMagazineList(Resource):
    def get(self):
        return {
            'magazines': [
                marshal(magazine, hmag_field)
                for magazine in models.HarmonistMagazine.select()
            ]
        }


class HarmonistMagazineSearch(Resource):
    def get(self, query):
        return {
            'magazines': [
                marshal(magazine, hmag_field)
                for magazine in models.HarmonistMagazine.select().where(
                    models.HarmonistMagazine.title.contains(query)
                )
            ]
        }

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
    endpoint='search_hmag'
)
