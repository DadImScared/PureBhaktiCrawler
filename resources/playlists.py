
from flask import jsonify, Blueprint, abort, make_response, g

from flask_restful import (Resource, Api, reqparse,
                               inputs, fields, marshal,
                               marshal_with, url_for)
from auth import auth

import models


class CustomDateTime(fields.Raw):
    def format(self, value):
        return value.strftime("%D %r")

item_field = {
    "title": fields.String,
    "link": fields.String,
    "item_order": fields.Integer,
    "type": fields.String
}

playlist_names = {
    "name": fields.String
}

playlist_field = {
    "name": fields.String,
    "items": fields.List(fields.Nested(item_field)),
    "playlistId": fields.String(attribute='playlist_id'),
    "createdAt": CustomDateTime(attribute="created_at"),
    "updatedAt": CustomDateTime(attribute="updated_at")
}

playlist_with_item = {
    "name": fields.String,
    'hasItem': fields.Boolean,
    'itemIndex': fields.Integer
}


def add_type(item):
    """Add type song or lecture to item object amd return PlaylistItem object"""
    if item.song:
        item.title = item.song.title
        item.link = item.song.link
        item.type = "song"
    else:
        item.title = item.lecture.title
        item.link = item.lecture.link
        item.type = "lecture"
    return item


def add_items(playlist):
    """Adds items to Playlist object and formats updated_at and created_at datetime fields and return Playlist object"""
    playlist.items = [marshal(add_type(item), item_field) for item in playlist.get_items()]
    return playlist


def get_item(title, item_type):
    """Return models.Song or models.Lecture object

    :param str title: Title of Song or Lecture object
    :param str item_type: Item type "lecture" or "song"
    :raise ValueError: Song or lecture does not exist
    :return: models.Song or models.Lecture object
    """

    if item_type == "song":
        try:
            return models.Song.get(title=title)
        except models.DoesNotExist:
            raise ValueError("Song does not exist")
    else:
        try:
            return models.AudioLecture.get(title=title)
        except models.DoesNotExist:
            raise ValueError("Lecture does not exist")


def has_item(playlist, title, item_type):
    playlist.hasItem, playlist.itemIndex = playlist.has_item(title, item_type)
    return playlist


class Playlists(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    @auth.login_required
    def get(self):
        """Return list of Playlist objects"""
        self.reqparse.add_argument('names', type=str)
        args = self.reqparse.parse_args()

        if args["names"]:
            return make_response(jsonify({
                "playlists": [playlist.name for playlist in g.user.get_playlists()]
            }), 200)
        return {
            "playlists": [marshal(add_items(playlist), playlist_field) for playlist in g.user.get_playlists()]
        }, 200


class Playlist(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    @auth.login_required
    def get(self, list_id):
        """Return Playlist object"""
        try:
            playlist = g.user.get_playlist(list_id)
        except ValueError as e:
            return make_response(jsonify({"message": str(e)}), 404)
        else:
            return marshal(add_items(playlist), playlist_field), 200

    @auth.login_required
    def post(self):
        """Return Playlist object"""
        self.reqparse.add_argument(
            "name",
            required=True,
            help="Playlist name required",
            location=['json']
        )
        args = self.reqparse.parse_args()
        playlist, created = models.Playlist.get_or_create(user=g.user, name=args["name"].strip())
        if created:
            return marshal(add_items(playlist), playlist_field), 201
        else:
            return make_response(jsonify({"message": "{} already exists".format(playlist.name)}), 409)

    @auth.login_required
    def patch(self, list_id):
        """Return Playlist object with new name"""
        self.reqparse.add_argument(
            "name",
            required=True,
            help="Playlist name required",
            location=['json']
        )
        args = self.reqparse.parse_args()
        # check if user has playlist already
        try:
            g.user.get_playlist_with_name(args['name'])
        except ValueError:
            # else rename playlist
            try:
                playlist = g.user.get_playlist(list_id)
            except ValueError as e:
                return make_response(jsonify({"message": "Playlist does not exist"}), 404)
            else:
                playlist.name = args['name']
                playlist.save()
                return marshal(add_items(playlist), playlist_field), 200
        else:
            # if they do return 403
            return make_response(jsonify({"message": "You already have a playlist with this name"}), 409)

    @auth.login_required
    def delete(self, list_id=None):
        """Delete Playlist instance"""
        # self.reqparse.add_argument(
        #     "name",
        #     required=True,
        #     help="Playlist name required",
        #     location=['json']
        # )
        # args = self.reqparse.parse_args()
        if not list_id:
            return make_response(jsonify({"message": "Playlist uuid required"}), 400)
        try:
            playlist = g.user.get_playlist(list_id)
        except ValueError as e:
            return make_response(jsonify({"message": str(e)}), 404)
        else:
            playlist.delete_instance(recursive=True)
            return 200


class PlaylistItems(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "playlist",
            required=True,
            help="Playlist name required",
            location=['json']
        )
        super().__init__()

    @auth.login_required
    def post(self):
        """Return new PlaylistItem object"""
        self.reqparse.add_argument(
            "itemName",
            required=True,
            help="Item name required",
            location=['json']
        )
        self.reqparse.add_argument(
            'itemType',
            required=True,
            help="Item type required",
            location=['json']
        )
        args = self.reqparse.parse_args()
        item_types = ["song", "lecture"]
        if args["itemType"].lower() not in item_types:
            return make_response(jsonify({"message": "Bad item type"}), 400)
        playlist, _ = models.Playlist.get_or_create(user=g.user, name=args["playlist"])
        playlist_has_item, _ = playlist.has_item(title=args['itemName'], item_type=args['itemType'])
        if playlist_has_item:
            return make_response(jsonify({"message": "Item already on playlist"}), 400)
        try:
            item = get_item(args["itemName"], args["itemType"])
        except ValueError as e:
            return make_response(jsonify({"message": str(e)}), 404)
        else:
            new_item = playlist.add_item(item=item, item_type=args["itemType"])
            return marshal(add_type(new_item), item_field), 200

    @auth.login_required
    def patch(self):
        """Update item_order in PlaylistItem object and return PlaylistItem"""

        self.reqparse.add_argument(
            "oldIndex",
            required=True,
            type=int,
            help="Old index required",
            location=['json']
        )
        self.reqparse.add_argument(
            "newIndex",
            type=int,
            required=True,
            help="New index required",
            location=['json']
        )
        args = self.reqparse.parse_args()
        try:
            playlist = g.user.get_playlist_with_name(args["playlist"])
        except ValueError:
            return make_response(jsonify({"message": "Playlist does not exist"}), 404)
        else:
            try:
                new_item = playlist.move_item(old_index=args["oldIndex"], new_index=args["newIndex"])
            except ValueError as e:
                return make_response(jsonify({"message": str(e)}), 404)
            else:
                return marshal(add_type(new_item), item_field), 200

    @auth.login_required
    def delete(self):
        """Delete a PlaylistItem object"""
        self.reqparse.add_argument(
            'currentIndex',
            required=True,
            type=int,
            help="Index of item required"
        )
        args = self.reqparse.parse_args()
        try:
            playlist = g.user.get_playlist_with_name(name=args["playlist"])
        except ValueError as e:
            return make_response(jsonify({"message": str(e)}), 404)
        else:
            try:
                playlist.delete_item(args["currentIndex"])
            except ValueError as e:
                return make_response(jsonify({"message": str(e)}), 404)
            else:
                print(playlist.name)
                print("deleted")
                return jsonify({"message": "Item deleted from {} ".format(playlist.name)})


class PlaylistsWithItem(Resource):
    @auth.login_required
    def get(self, title, item_type):
        """Return list of objects

        :param str title: Title of Song object or Lecture object
        :param str item_type: Type of song or lecture
        :return: List of objects. Example {'name': 'my_playlist', 'hasItem': 'false'}
        """
        item_types = ['song', 'lecture']
        if item_type not in item_types:
            return make_response(jsonify({"message": "Bad item type"}), 400)
        return {
            'playlists': [
                marshal(has_item(playlist, title, item_type), playlist_with_item)
                for playlist in g.user.get_playlists()
            ]
        }, 200


playlist_api = Blueprint('resources.playlists', __name__)
api = Api(playlist_api)
api.add_resource(
    Playlists,
    '/playlists',
    endpoint='playlists'
)
api.add_resource(
    Playlist,
    '/playlist',
    '/playlists/<list_id>',
    endpoint="playlist"
)
api.add_resource(
    PlaylistItems,
    '/playlist/item',
    endpoint='playlist_item'
)
api.add_resource(
    PlaylistsWithItem,
    '/playlists/includes/<title>/<item_type>',
    endpoint='playlist_with_item'
)
