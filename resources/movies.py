
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from resources.api_fields import movie_field
from resources.utils import paginate, BaseResource, get_query
from remove_words import remove_stop_words


class MovieList(BaseResource):
    def get(self):
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=models.Movie.select(),
            next_url='movies.movies',
            **args
        )
        return {
            'data': [
                marshal(movie, movie_field)
                for movie in page_query.get_object_list()
            ],
            "nextPage": next_page
        }


class MovieSearch(BaseResource):
    def get(self, query):
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=get_query(models.Movie, query),
            next_url='movies.search',
            query=query,
            **args
        )
        return {
            'data': [
                marshal(movie, movie_field)
                for movie in page_query.get_object_list()
                ],
            "nextPage": next_page
        }
        # if len(query.split(" ")) > 1:
        #     return {
        #         'movies': [
        #             marshal(movie, movie_field)
        #             for movie in models.Movie.select().where(
        #                 models.Movie.title.regexp(
        #                     r"[-\s_]+".join(remove_stop_words(query.lower().split(" ")))
        #                 )
        #             )
        #         ]
        #     }
        # return {
        #     'movies': [
        #         marshal(movie, movie_field)
        #         for movie in models.Movie.select().where(
        #             models.Movie.title.contains(query)
        #         )
        #     ]
        # }

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
    endpoint='search'
)
