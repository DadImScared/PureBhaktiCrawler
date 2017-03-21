
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models

lecture_field = {
    'id': fields.Integer,
    'link': fields.String,
    'title': fields.String,
    'category': fields.String,
    'hits': fields.Integer
}


class AudioLectureList(Resource):
    def get(self):
        return {
            'lectures': [
                marshal(lecture, lecture_field)
                for lecture in models.AudioLecture.select()
            ]
        }


class AudioLectureSearch(Resource):
    def get(self, query):
        return {
            'lectures': [
                marshal(lecture, lecture_field)
                for lecture in models.AudioLecture.select().where(
                    models.AudioLecture.title.contains(query)
                )
            ]
        }


lectures_api = Blueprint('resources.lectures', __name__)
api = Api(lectures_api)
api.add_resource(
    AudioLectureList,
    '/lectures',
    endpoint="lectures"
)
api.add_resource(
    AudioLectureSearch,
    '/search/lectures/<query>',
    endpoint='search_lectures'
)
