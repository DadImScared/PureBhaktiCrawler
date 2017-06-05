
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from resources.api_fields import hmag_field
from remove_words import remove_stop_words


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
        if len(query.split(" ")) > 1:
            return {
                'magazines': [
                    marshal(magazine, hmag_field)
                    for magazine in models.HarmonistMagazine.select().where(
                        models.HarmonistMagazine.title.regexp(
                            r"[-\s_]+".join(remove_stop_words(query.lower().split(" ")))
                        )
                    )
                ]
            }
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
