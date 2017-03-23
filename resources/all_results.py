
from flask import Blueprint, abort, jsonify

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with, marshal_with_field)
import models
import resources.api_fields as api_fields


class AllRecords(Resource):
    def get(self):
        return {
            'results': {
                'books': [
                    marshal(book, api_fields.book_field)
                    for book in models.Book.select()
                ],
                'movies': [
                    marshal(movie, api_fields.movie_field)
                    for movie in models.Movie.select()
                ],
                'lectures': [
                    marshal(lecture, api_fields.lecture_field)
                    for lecture in models.AudioLecture.select()
                ],
                'bhagavatpatrika': [
                    marshal(magazine, api_fields.bp_list)
                    for magazine in models.BhagavatPatrika.select()
                ],
                'harikatha': [
                    marshal(magazine, api_fields.hk_field)
                    for magazine in models.HariKatha.select()
                ],
                'harmonistmonthly': [
                    marshal(magazine, api_fields.hmonthly_field)
                    for magazine in models.HarmonistMonthly.select()
                ],
                'harmonistmagazine': [
                    marshal(magazine, api_fields.hmag_field)
                    for magazine in models.HarmonistMagazine.select()
                ],
                'songs': [
                    marshal(song, api_fields.song_field)
                    for song in models.Song.select()
                ]
            }
        }


class AllRecordsSearch(Resource):
    def get(self, query):
        return {
            'results': {
                'books': [
                    marshal(book, api_fields.book_field)
                    for book in models.Book.select().where(models.Book.title.contains(query))
                ],
                'movies': [
                    marshal(movie, api_fields.movie_field)
                    for movie in models.Movie.select().where(models.Movie.title.contains(query))
                ],
                'lectures': [
                    marshal(lecture, api_fields.lecture_field)
                    for lecture in models.AudioLecture.select().where(models.AudioLecture.title.contains(query))
                ],
                'bhagavatpatrika': [
                    marshal(magazine, api_fields.bp_list)
                    for magazine in models.BhagavatPatrika.select().where(models.BhagavatPatrika.title.contains(query))
                ],
                'harikatha': [
                    marshal(magazine, api_fields.hk_field)
                    for magazine in models.HariKatha.select().where(models.HariKatha.title.contains(query))
                ],
                'harmonistmonthly': [
                    marshal(magazine, api_fields.hmonthly_field)
                    for magazine in models.HarmonistMonthly.select().where(models.HarmonistMonthly.title.contains(query))
                ],
                'harmonistmagazine': [
                    marshal(magazine, api_fields.hmag_field)
                    for magazine in models.HarmonistMagazine.select().where(models.HarmonistMagazine.title.contains(query))
                ],
                'songs': [
                    marshal(song, api_fields.song_field)
                    for song in models.Song.select().where(models.Song.title.contains(query))
                ]
            }
        }


all_api = Blueprint('resources.all_results', __name__)
api = Api(all_api)
api.add_resource(
    AllRecords,
    '/all',
    endpoint='all_records'
)
api.add_resource(
    AllRecordsSearch,
    '/search/all/<query>',
    endpoint='search_all_records'
)
