
from flask import url_for
from flask_restful import Resource, reqparse
from functools import wraps
from playhouse.flask_utils import PaginatedQuery
from models import *
from remove_words import remove_stop_words


# resource_to_db_table = {
#     "booksearch": {"category": "books", "subCat": "title"},
#     "bookcontentsearch": {"category": "books", "subCat": "content"},
#     "songsearch": {"category": "songs", "subCat": "title"},
#     "moviesearch": {"category": "movies", "subCat": "title"},
#     "audiolecturesearch": {"category": "lectures", "subCat": "title"},
#     "bhagavatpatrikasearch": {"category": "bhagavatpatrika", "subCat": "title"},
#     "harmonistmagazinesearch": {"category": "harmonistmagazine", "subCat": "title"},
#     "harmonistmonthlysearch": {"category": "harmonistmonthly", "subCat": "title"},
#     "harmonistmonthlycontentsearch": {"category": "harmonistmonthly", "subCat": "content"},
#     "harikathasearch": {"category": "harikatha", "subCat": "title"},
#     "harikathacontentsearch": {"category": "harikatha", "subCat": "content"}
# }


def get_query(model, query):
    v_tables = ["ftshk", "ftshm", "ftsbookpage"]
    v_models = {"ftshk": FTSHK.search_magazine, "ftshm": FTSHM.search_magazine, "ftsbookpage": FTSBookPage.search_pages}
    if model.__name__.lower() in v_tables:
        search_query = v_models[model.__name__.lower()](query)
    else:
        if len(query.split(" ")) > 1:
            search_query = model.select().where(
                model.title.regexp(r"[-\s_]+".join(remove_stop_words(query.lower().split(" "))))
            )
        else:
            search_query = model.select().where(model.title.contains(query))
    return search_query


def paginate_query(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        print(args)
        print(kwargs)
        print("page decorator")
        result = f(self, *args, **kwargs)

        return result
    return wrapper



class BaseResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('page', type=int)
        self.reqparse.add_argument('page_amount', type=int)
        super().__init__()


def get_page(args):
    print(args)
    return args.get('page') if args["page"] and args["page"] > 0 else 1


def paginate_amount(num):
    def_num = 25
    if not num:
        page_by = def_num
    else:
        if num > 50 <= 1000:
            page_by = num
        else:
            page_by = def_num
    return page_by


def paginate(select_query, next_url, page, page_amount=50, **url_params):
    page_query = PaginatedQuery(select_query, paginate_by=paginate_amount(page_amount))
    next_page = False
    if not page:
        page = 1
    if page < page_query.get_page_count():
        next_page = url_for(
            'resources.{}'.format(next_url),
            page_amount=page_amount,
            page=page + 1 if page > 0 else 2, **url_params
        )
    return page_query, next_page
