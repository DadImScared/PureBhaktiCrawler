
from peewee import *
from playhouse.sqlite_ext import FTSModel, SqliteExtDatabase
from playhouse.flask_utils import PaginatedQuery
from flask_bcrypt import check_password_hash, generate_password_hash
import os
import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
import config

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

    @classmethod
    def get_english_book(cls, name):
        try:
            return cls.get((cls.title == name) & (cls.language == 'english'))
        except DoesNotExist:
            return None


class BookPage(Model):
    book = ForeignKeyField(rel_model=Book, related_name='full_book', null=True)
    title = TextField()
    page = IntegerField()
    display_content = TextField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_page(cls, title, page, display_content, book=None):
        try:
            if book:
                return cls.create(book=book, title=title, page=page, display_content=display_content)
            return cls.create(title=title, page=page, display_content=display_content)
        except IntegrityError:
            return None


class BookContent(Model):
    title = TextField(unique=True)

    class Meta:
        database = DATABASE

    @classmethod
    def create_book(cls, title):
        try:
            return cls.create(title=title)
        except IntegrityError:
            return None


class FTSBaseModel(FTSModel):
    item_id = IntegerField()
    content = TextField(index=True)

    class Meta:
        database = DATABASE


class FTSFullBook(FTSBaseModel):
    display_content = TextField(index=True)

    @classmethod
    def search_books(cls, query):
        search = (cls.select(
            BookContent, cls
        ).join(
            BookContent, on=(cls.item_id == BookContent.id).alias("fullbook")
        ).where(cls.match(query)))
        return search


class FTSBook(FTSBaseModel):
    page = IntegerField()

    @classmethod
    def search_books(cls, query):
        search = (cls.select(Book, cls).join(Book, on=(cls.item_id == Book.id).alias('books')).where(
            cls.match(query)
        ))
        return search


class FTSBookPage(FTSBaseModel):

    @classmethod
    def search_pages(cls, query):
        search = (cls.select(BookPage, cls).join(BookPage, on=(cls.item_id == BookPage.id).alias('pages')).where(
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


class User(Model):
    """User class for database"""

    #: CharField unique email for user
    email = CharField(unique=True, null=True)

    #: CharField password for user
    password = CharField(null=True)

    #: DateTimeField joined_at
    joined_at = DateTimeField(default=datetime.datetime.now)

    #: BooleanField email_confirmed default set to False
    email_confirmed = BooleanField(default=False)

    #: CharField user_id for google or facebook user
    user_id = CharField(null=True)

    #: CharField user_type indicating where the user registered from
    #: Default to ("home", which means they registered through us)
    #: Other options include "facebook", and "google"
    user_type = CharField(default="home")

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, email, password):
        """Creates User object and returns created object

        :param str email: Unique email for user
        :param str password: Password for user
        :raise ValueError: User already exists
        :return: return User object
        """
        try:
            return cls.create(
                email=email,
                password=generate_password_hash(password)
            )
        except IntegrityError:
            raise ValueError("User already exists")

    @classmethod
    def get_user(cls, email):
        """Return User object if User exists

        :param str email: Email to user
        :return: User object if match else None
        """
        try:
            return cls.get(cls.email == email)
        except DoesNotExist:
            return None

    def verify_password(self, password):
        """Return True if password matches else False"""
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expires=3600):
        """Return auth token"""
        serializer = Serializer(config.SECRET_KEY, expires_in=expires)
        return serializer.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """Verify token and return User object

        :param token: Token to identify user
        :except SignatureExpired, BadSignature: return None
        :return: User object if verified else None
        """
        serializer = Serializer(config.SECRET_KEY)
        try:
            data = serializer.loads(token)
        except (SignatureExpired, BadSignature):
            return None
        else:
            user = User.get(User.id == data['id'])
            return user

    def get_playlists(self):
        """Return list of Playlist objects related to User instance"""
        return Playlist.select().where(Playlist.user == self)

    def get_playlist(self, name):
        """return Playlist object that matches name"""
        try:
            return Playlist.get(user=self, name=name)
        except DoesNotExist:
            raise ValueError("Playlist does not exist")


class Playlist(Model):
    """Playlist class for database"""
    user = ForeignKeyField(rel_model=User, related_name="to_user")
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

    @classmethod
    def create_playlist(cls, user, name):
        """Creates and returns Playlist object

        :param user: User object
        :param str name: Name of Playlist object
        :return: Playlist object
        """
        return cls.create(user=user, name=name)

    def add_item(self, item, item_type):
        """Add and return PlaylistItem object

        :param item: Song or Lecture object to add to Playlist
        :param item_type: Item type song or lecture
        :return: PlaylistItem object
        """
        if item_type == "song":
            return PlaylistItem.create_item(playlist=self, song=item)
        else:
            return PlaylistItem.create_item(playlist=self, lecture=item)

    def get_items(self):
        """Return list of PlaylistItem objects related to Playlist instance"""
        return PlaylistItem.select().where(PlaylistItem.playlist == self).order_by(PlaylistItem.item_order.asc())

    def get_item(self, index):
        """Return PlaylistItem where item_order is equal to index"""
        try:
            return PlaylistItem.get(
                (PlaylistItem.playlist == self) &
                (PlaylistItem.item_order == index)
            )
        except DoesNotExist:
            raise ValueError("Item does not exist")

    def move_item(self, old_index, new_index):
        """Changes item_order of PlaylistItem from old_index to new_index

        :param int old_index: Current item_order of item on playlist
        :param int new_index: New item_order of playlist item
        :return: PlaylistItem object with new item_order
        """
        if new_index > self.get_items().count():
            raise ValueError("New index out of range")
        try:
            current_item = self.get_item(old_index)
        except ValueError as e:
            raise e
        else:
            if new_index < old_index:
                # move item up list example old_index = 7 and new_index = 2
                PlaylistItem.update(item_order=PlaylistItem.item_order+1).where(
                    (PlaylistItem.item_order < old_index) &
                    (PlaylistItem.item_order >= new_index)
                ).execute()
            else:
                # move item down list
                PlaylistItem.update(item_order=PlaylistItem.item_order-1).where(
                    (PlaylistItem.item_order > old_index) &
                    (PlaylistItem.item_order <= new_index)
                ).execute()
            current_item.item_order = new_index
            current_item.save()
            return current_item

    def delete_item(self, index):
        """Delete item from Playlist where PlaylistItem.item_order == index"""
        try:
            return self.get_item(index).delete_instance()
        except ValueError as e:
            raise e


class PlaylistItem(Model):
    """PlaylistItem class for database"""
    playlist = ForeignKeyField(rel_model=Playlist, related_name="to_playlist")

    #: Song object to add to playlist not required if Lecture is assigned
    song = ForeignKeyField(rel_model=Song, related_name="song_item", null=True)

    #: Lecture object to add to playlist not required if Song is assigned
    lecture = ForeignKeyField(rel_model=AudioLecture, related_name="lecture_item", null=True)

    item_order = IntegerField()

    class Meta:
        database = DATABASE
        order_by = ('item_order',)

    @classmethod
    def create_item(cls, playlist, song=None, lecture=None):
        """Creates and returns PlayListItem

        Only create_item with a song or a lecture not both.
        if you create_item with both a song and object a PlaylistItem will be created with the song and not the lecture
        :param playlist: Playlist to add song or lecture to
        :param song: Song to add to playlist. Required if Lecture is not assigned
        :param lecture: Lecture to add to playlist. Required if Song is not assigned
        :raise ValueError: If song or lecture is not included. Always include one or the other
        :return: PlayListItem object
        """
        if not song and not lecture:
            raise ValueError("song or lecture required")
        else:
            if song:
                return cls.create(playlist=playlist, song=song, item_order=playlist.get_items().count())
            else:
                return cls.create(playlist=playlist, lecture=lecture, item_order=playlist.get_items().count())


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
                            AudioLecture, Song, FTSBook, FTSHK, FTSHM, BookPage, FTSBookPage,
                            BookContent, FTSFullBook, User, Playlist, PlaylistItem], safe=True)
    DATABASE.close()
