
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from resources.api_fields import lecture_field
from resources.utils import paginate, BaseResource, get_query
from remove_words import remove_stop_words


class AudioLectureList(BaseResource):
    def get(self):
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=models.AudioLecture.select(),
            next_url='lectures.lectures',
            **args
        )
        return {
            'data': [
                marshal(lecture, lecture_field)
                for lecture in page_query.get_object_list()
            ],
            "nextPage": next_page
        }


class AudioLectureSearch(BaseResource):
    def get(self, query):
        args = self.reqparse.parse_args()
        page_query, next_page = paginate(
            select_query=get_query(models.AudioLecture, query),
            next_url='lectures.search',
            query=query,
            **args
        )
        return {
            'nextPage': next_page,
            'data': [
                marshal(lecture, lecture_field)
                for lecture in page_query.get_object_list()
            ]
        }
        # if len(query.split(" ")) > 1:
        #     return {
        #         'lectures': [
        #             marshal(lecture, lecture_field)
        #             for lecture in models.AudioLecture.select().where(
        #                 models.AudioLecture.title.regexp(
        #                     r"[-\s_]+".join(remove_stop_words(query.lower().split(" ")))
        #                 )
        #             )
        #         ]
        #     }
        # return {
        #     'lectures': [
        #         marshal(lecture, lecture_field)
        #         for lecture in models.AudioLecture.select().where(
        #             models.AudioLecture.title.contains(query)
        #         )
        #     ]
        # }


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
    endpoint='search'
)
