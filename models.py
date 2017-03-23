
from peewee import *
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
DATABASE = SqliteDatabase('{}{}links.db'.format(dir_path, os.path.sep))


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
    title = TextField(unique=True)
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

    Methods:
        create_book

    """

    link = TextField(unique=True)
    title = TextField()
    language = CharField()
    hits = IntegerField(default=0)

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
    title = TextField()
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

    Methods:
        create_entry

    """
    link = TextField(unique=True)
    title = TextField(unique=True)
    hits = IntegerField(default=0)

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


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Movie, Book, HarmonistMagazine, BhagavatPatrika, HariKatha, HarmonistMonthly,
                            AudioLecture, Song], safe=True)
    DATABASE.close()
