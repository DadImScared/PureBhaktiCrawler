
from flask import Blueprint, abort

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from resources.api_fields import bp_list
from resources.utils import paginate, BaseResource, get_query
from remove_words import remove_stop_words


def bp_or_404(bp_name):
    try:
        bp = models.BhagavatPatrika.get(models.BhagavatPatrika.title == bp_name)
    except models.DoesNotExist:
        abort(404)
    else:
        return bp


class BhagavatPatrikaList(BaseResource):
    def get(self):
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=models.BhagavatPatrika,
            next_url='bhagavatpatrika.bhagavatpatrikas',
            **args
        )
        return {
            'nextPage': next_page,
            'data': [
                marshal(bp, bp_list)
                for bp in page_query.get_object_list()
            ]
        }


class BhagavatPatrika(Resource):

    @marshal_with(bp_list)
    def get(self, title):
        print(title)
        return models.BhagavatPatrika.get(models.BhagavatPatrika.title==title)


class BhagavatPatrikaSearch(BaseResource):
    def get(self, query):
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=get_query(models.BhagavatPatrika, query),
            next_url='bhagavatpatrika.search',
            query=query,
            **args
        )
        return {
            'nextPage': next_page,
            'data': [
                marshal(bp, bp_list)
                for bp in page_query.get_object_list()
            ]
        }


bp_api = Blueprint('resources.bhagavatpatrika', __name__)
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
    endpoint='search'
)
