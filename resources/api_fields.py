
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

book_content_field = {
    'snippet': fields.String,
    'indexes': fields.Integer
}

book_snippet_field = {
    'id': fields.Integer,
    'title': fields.String,
    'page': fields.Integer,
    'content': fields.String,
    'indexes': fields.List(fields.Integer)
}

magazine_search_field = {
    'id': fields.Integer,
    'link': fields.String,
    'title': fields.String,
    'content': fields.String
}

magazine_snippet_field = {
    'id': fields.Integer,
    'link': fields.String,
    'title': fields.String,
    'content': fields.List(fields.String)
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
