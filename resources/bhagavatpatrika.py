
from flask import Blueprint, abort

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from resources.api_fields import bp_list
from remove_words import remove_stop_words


def bp_or_404(bp_name):
    try:
        bp = models.BhagavatPatrika.get(models.BhagavatPatrika.title == bp_name)
    except models.DoesNotExist:
        abort(404)
    else:
        return bp


class BhagavatPatrikaList(Resource):

    def get(self):
        return {
            'magazines': [
                marshal(bp, bp_list)
                for bp in models.BhagavatPatrika.select().order_by(
                    models.BhagavatPatrika.year.desc(),
                    models.BhagavatPatrika.issue.asc()
                )
            ]
        }


class BhagavatPatrika(Resource):

    @marshal_with(bp_list)
    def get(self, title):
        print(title)
        return models.BhagavatPatrika.get(models.BhagavatPatrika.title==title)


class BhagavatPatrikaSearch(Resource):
    def get(self, query):
        if len(query.split(" ")) > 1:
            return {
                'magazines': [
                    marshal(bp, bp_list)
                    for bp in models.BhagavatPatrika.select().where(
                        models.BhagavatPatrika.title.regexp(
                            r"[-\s_]+".join(remove_stop_words(query.lower().split(" ")))
                        )
                    )
                ]
            }
        return {
            'magazines': [
                marshal(bp, bp_list)
                for bp in models.BhagavatPatrika.select().where(
                    models.BhagavatPatrika.title.contains(query)
                )
            ]
        }


bp_api = Blueprint('resources.bhagavapatrika', __name__)
api = Api(bp_api)
api.add_resource(
    BhagavatPatrikaList,
    '/bhagavatpatrika',
    endpoint='bhagavatpatrikas'
)
api.add_resource(
    BhagavatPatrika,
    '/bhagavatpatrika/<title>',
    endpoint='bhagavatpatrika'
)
api.add_resource(
    BhagavatPatrikaSearch,
    '/search/bhagavatpatrika/<query>',
    endpoint='searchbhagavatpatrika'
)
