
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from resources.api_fields import song_field


class SongList(Resource):
    def get(self):
        return {
            'songs': [
                marshal(song, song_field)
                for song in models.Song.select()
            ]
        }


class SongSearch(Resource):
    def get(self, query):
        return {
            'songs': [
                marshal(song, song_field)
                for song in models.Song.select().where(
                    models.Song.title.contains(query)
                )
            ]
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
