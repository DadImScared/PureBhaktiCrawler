
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from resources.api_fields import lecture_field
from remove_words import remove_stop_words


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
        if len(query.split(" ")) > 1:
            return {
                'lectures': [
                    marshal(lecture, lecture_field)
                    for lecture in models.AudioLecture.select().where(
                        models.AudioLecture.title.regexp(
                            r"[-\s_]+".join(remove_stop_words(query.lower().split(" ")))
                        )
                    )
                ]
            }
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
