
from flask_restful import fields

book_field = {
    'id': fields.Integer,
    'link': fields.String,
    'title': fields.String,
    'language': fields.String,
    'hits': fields.Integer
}

book_search_field = {
    'link': fields.String,
    'title': fields.String,
    'page': fields.Integer,
    'content': fields.String
}

hk_field = {
    'id': fields.Integer,
    'link': fields.String,
    'title': fields.String,
    'hits': fields.Integer
}

bp_list = {
    'id': fields.Integer,
    'link': fields.String,
    'title': fields.String,
    'year': fields.String,
    'issue': fields.String,
    'hits': fields.Integer
}

movie_field = {
    'id': fields.Integer,
    'link': fields.String,
    'title': fields.String,
    'hits': fields.Integer
}

song_field = {
    'id': fields.Integer,
    'link': fields.String,
    'title': fields.String,
    'category': fields.String,
    'hits': fields.Integer
}

hmag_field = {
    'id': fields.Integer,
    'link': fields.String,
    'title': fields.String,
    'hits': fields.Integer
}

hmonthly_field = {
    'id': fields.Integer,
    'link': fields.String,
    'title': fields.String,
    'hits': fields.Integer
}

lecture_field = {
    'id': fields.Integer,
    'link': fields.String,
    'title': fields.String,
    'category': fields.String,
    'hits': fields.Integer
}
