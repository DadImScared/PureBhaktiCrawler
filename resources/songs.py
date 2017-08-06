
from flask import Blueprint, url_for
from functools import wraps

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from playhouse.flask_utils import PaginatedQuery
from resources.api_fields import song_field
from resources.utils import paginate, BaseResource, get_query
from remove_words import remove_stop_words


# def paginate_query(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         parser = reqparse.RequestParser()
#         parser.add_argument('page', type=int)
#         params = parser.parse_args()
#         kwargs["args"] = params
#         return f(*args, **kwargs)
#
#     return wrapper

def add_type(song):
    song.type = "song"
    return song


class SongList(BaseResource):
    def get(self, query=None):
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=models.Song.select(),
            next_url='songs.songs',
            **args
        )
        return {
            'data': [
                marshal(add_type(song), song_field)
                for song in page_query.get_object_list()
            ],
            "nextPage": next_page
        }


class SongSearch(BaseResource):
    def get(self, query):
        parse_copy = self.reqparse.copy()
        parse_copy.add_argument('snippets')
        args = parse_copy.parse_args()

        search_query = get_query(models.Song, query)

        page_query, next_page = paginate(
            select_query=search_query,
            next_url='songs.search_songs',
            query=query,
            **args
        )

        return {
            'data': [
                marshal(add_type(song), song_field)
                for song in page_query.get_object_list()
            ],
            "nextPage": next_page
        }


song_api = Blueprint('resources.songs', __name__)
api = Api(song_api)
api.add_resource(
    SongList,
    '/songs',
    endpoint="songs"
)
api.add_resource(
    SongSearch,
    '/search/songs/<query>',
    endpoint='search_songs'
)
