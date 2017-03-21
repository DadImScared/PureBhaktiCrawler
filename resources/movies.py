
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models

movie_field = {
    'id': fields.Integer,
    'link': fields.String,
    'title': fields.String,
    'hits': fields.Integer
}

class MovieList(Resource):
    def get(self):
        return {
            'movies': [
                marshal(movie, movie_field)
                for movie in models.Movie.select()
            ]
        }


class MovieSearch(Resource):
    def get(self, query):
        return {
            'movies': [
                marshal(movie, movie_field)
                for movie in models.Movie.select().where(
                    models.Movie.title.contains(query)
                )
            ]
        }

movie_api = Blueprint('resources.movies', __name__)
api = Api(movie_api)
api.add_resource(
    MovieList,
    '/movies',
    endpoint="movies"
)
api.add_resource(
    MovieSearch,
    '/search/movies/<query>',
    endpoint='search_movies'
)
