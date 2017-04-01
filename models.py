
from peewee import *
from playhouse.sqlite_ext import *
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
DATABASE = SqliteExtDatabase('{}{}links.db'.format(dir_path, os.path.sep))


class Movie(Model):
    """Movie class for database

    Attributes:
        link  TextField unique
        title  TextField unique
        hits  IntegerField default 0

    Methods:
        create_movie

    """

    link = TextField(unique=True)
    title = TextField(unique=True, index=True)
    hits = IntegerField(default=0)

    class Meta:
        database = DATABASE
        order_by = ('title',)


    @classmethod
    def create_movie(cls, link, title, hits=0):
        """Return Movie object

        :param str link: Link to movie
        :param str title: Title to movie
        :param int hits: How many times a link has been clicked defaults to 0
        :return: <models.Movie object>

        :Example:

        >>>import models
        >>>movie = {'link': 'linkhere', 'title': 'titlehere'}
        >>>models.Movie.create_movie(**movie)

        """

        try:
            return cls.create(link=link, title=title, hits=hits)
        except IntegrityError:
            return None


class Book(Model):
    """Book class for database

    Attributes:
        link  TextField unique
        title  TextField unique
        language CharField
        hits  IntegerField default 0
        indexed = BooleanField default False

    Methods:
        create_book

    """

    link = TextField(unique=True)
    title = TextField(index=True)
    language = CharField()
    hits = IntegerField(default=0)
    indexed = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('language',)

    @classmethod
    def create_book(cls, link, title, language, hits=0):
        """

        Return Book object

        :param str link: Link to book
        :param str title: Title to book
        :param str language: Language of book
        :param int hits: How many times a link has been clicked defaults to 0
        :return: <models.Book object>

        :Example:

        >>>import models
        >>>book_info = {'link': 'linkhere', 'title': 'titlehere', 'language': 'languagehere'}
        >>>new_book = models.Book.create_book(**book_info)


        """
        try:
            return cls.create(link=link, title=title, language=language, hits=hits)
        except IntegrityError:
            return None

    @classmethod
    def get_book(cls, book_id):
        """Return Book object of the book_id used"""
        try:
            return cls.get(cls.id == book_id)
        except DoesNotExist:
            return None


class FTSBaseModel(FTSModel):
    item_id = IntegerField()
    content = TextField()

    class Meta:
        database = DATABASE


class FTSBook(FTSBaseModel):
    page = IntegerField()

    @classmethod
    def search_books(cls, query):
        search = (cls.select(Book, cls).join(Book, on=(cls.item_id == Book.id).alias('books')).where(
            cls.match(query)
        ))
        return search


class HarmonistMagazine(Model):
    """HarmonistMagazine class for database

    Attributes:
        link  TextField unique
        title  TextField unique
        hits  IntegerField default 0

    Methods:
        create_magazine

    """
    link = TextField(unique=True)
    title = TextField(unique=True)
    hits = IntegerField(default=0)

    class Meta:
        database = DATABASE
        order_by = ('title',)

    @classmethod
    def create_magazine(cls, link, title, hits=0):
        """

        Return HarmonistMagazine object

        :param str link: Link to magazine
        :param str title: Title to magazine
        :param int hits: How many times a link has been clicked defaults to 0
        :return: <models.HarmonistMagazine object>

        :Example:

        >>>import models
        >>>new_magazine = {'link': 'maglinkhere', 'title':}

        """
        try:
            return cls.create(link=link, title=title, hits=hits)
        except IntegrityError:
            return None


class BhagavatPatrika(Model):
    """BhagavatPatrika class for database

    Attributes:
        link  TextField
        title  TextField
        year  TextField
        issue  TextField
        hits  IntegerField default 0

    Methods:
        create_entry
        entry_exists


    """

    link = TextField()
    title = TextField(index=True)
    year = TextField()
    issue = TextField()
    hits = IntegerField(default=0)

    class Meta:
        database = DATABASE
        order_by = ('year', 'issue')

    @classmethod
    def entry_exists(cls, link, issue):
        try:
            return cls.get((cls.link == link) & (cls.issue == issue))
        except DoesNotExist:
            return None

    @classmethod
    def create_entry(cls, link, title, year, issue, hits=0):
        """Return BhagavatPatrika object


        :param str link: Link to magazine
        :param str title: Title of magazine
        :param str year: Year magazine was published
        :param str issue: Issue of magazine example Year 1955, Issue 2
        :param int hits: How many times a link has been clicked defaults to 0
        :return: <models.BhagavatPatrika object>

        :Example:

        >>>import models
        >>>mag_info = {'link': 'linkhere', 'title': 'titlehere', 'year': 1955, 'issue': '2'}
        >>>new_mag = BhagavatPatrika.create_entry(**mag_info)

        """
        if not BhagavatPatrika.entry_exists(link, issue):
            return cls.create(link=link, title=title, year=year, issue=issue, hits=hits)
        else:
            return None


class HariKatha(Model):
    """HariKatha class for database

    Attributes:
        link  TextField unique
        title  TextField unique
        hits  IntegerField default 0
        indexed  BooleanField default 0

    Methods:
        create_entry

    """
    link = TextField(unique=True)
    title = TextField(unique=True)
    hits = IntegerField(default=0)
    indexed = BooleanField(default=0)

    class Meta:
        database = DATABASE
        order_by = ('title',)

    @classmethod
    def create_entry(cls, link, title, hits=0):
        """Return HariKatha object

        :param str link: Link to magazine
        :param str title: Title to magazine
        :param int hits: How many times a link has been clicked defaults to 0
        :return: <models.HariKatha object>

        :Example:
        >>>import models
        >>>mag_info = {'link': 'linkhere', 'title': 'titlehere'}
        >>>new_mag = HariKatha.create_entry(**mag_info)

        """
        try:
            return cls.create(link=link, title=title, hits=hits)
        except IntegrityError:
            return None


class FTSHK(FTSBaseModel):
    @classmethod
    def search_magazine(cls, query):
        search = (cls.select(HariKatha, cls).join(HariKatha, on=(cls.item_id == HariKatha.id).alias('harikatha')).where(
            cls.match(query)
        ))
        return search



class HarmonistMonthly(Model):
    """HarmonistMonthly class for database

    Attributes:
        link  TextField unique
        title  TextField unique
        hits  IntegerField default 0

    Methods:
        create_entry

    """
    link = TextField(unique=True)
    title = TextField(unique=True)
    hits = IntegerField(default=0)
    indexed = BooleanField(default=0)

    class Meta:
        database = DATABASE
        order_by = ('title',)

    @classmethod
    def create_entry(cls, link, title, hits=0):
        """Return HarmonistMonthly object

        :param str link: Link to magazine
        :param str title: Title to magazine
        :param int hits: How many times a link has been clicked defaults to 0
        :return: <models.HarmonistMonthly object>
        """

        try:
            return cls.create(link=link, title=title, hits=hits)
        except IntegrityError:
            return None


class FTSHM(FTSBaseModel):
    @classmethod
    def search_magazine(cls, query):
        search = (cls.select(HarmonistMonthly, cls).join(
            HarmonistMonthly, on=(cls.item_id == HarmonistMonthly.id).alias('hmonthly')).where(
            cls.match(query)
        ))
        return search


class AudioLecture(Model):
    """AudioLecture class for database

    Attributes:
        link  TextField unique
        title  TextField unique
        category  TextField
        hits  IntegerField default 0

    Methods:
        create_entry

    """

    link = TextField(unique=True)
    title = TextField(unique=True)
    category = TextField()
    hits = IntegerField(default=0)

    class Meta:
        database = DATABASE

    @classmethod
    def create_entry(cls, link, title, category, hits=0):
        try:
            return cls.create(link=link, title=title, category=category, hits=hits)
        except IntegrityError:
            return None


class Song(Model):
    """Songs/Bhajans class for database

    Attributes:
        link  TextField unique
        title  TextField unique
        category  TextField
        hits  IntegerField default 0

    Methods:
        create_entry

    """

    link = TextField(unique=True)
    title = TextField(unique=True)
    category = TextField()
    hits = IntegerField(default=0)

    class Meta:
        database = DATABASE

    @classmethod
    def create_entry(cls, link, title, category, hits=0):
        try:
            return cls.create(link=link, title=title, category=category, hits=hits)
        except IntegrityError:
            return None


def all_records():
    records = {}
    books = Book.select()
    movies = Movie.select()
    bp = BhagavatPatrika.select()
    harikatha = HariKatha.select()
    hmonthly = HarmonistMonthly.select()
    hmagazine = HarmonistMagazine.select()
    songs = Song.select()
    lectures = AudioLecture.select()
    # union = (books | movies | bp | harikatha | hmonthly | hmagazine | songs | lectures)
    # books = union.lhs.lhs.lhs.lhs.lhs.lhs.lhs
    # movies = union.lhs.lhs.lhs.lhs.lhs.lhs.rhs
    # bp = union.lhs.lhs.lhs.lhs.lhs.rhs
    # harikatha = union.lhs.lhs.lhs.lhs.rhs
    # hmonthly = union.lhs.lhs.lhs.rhs
    # hmagazine = union.lhs.lhs.rhs
    # songs = union.lhs.rhs
    # lectures = union.rhs
    records['books'] = books
    records['movies'] = movies
    records['bp'] = bp
    records['harikatha'] = harikatha
    records['hmonthly'] = hmonthly
    records['hmagazine'] = hmagazine
    records['songs'] = songs
    records['lectures'] = lectures
    return records


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Movie, Book, HarmonistMagazine, BhagavatPatrika, HariKatha, HarmonistMonthly,
                            AudioLecture, Song, FTSBook, FTSHK, FTSHM], safe=True)
    DATABASE.close()
