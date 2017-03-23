
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from resources.api_fields import hmonthly_field


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
