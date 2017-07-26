
from flask import jsonify, Blueprint, abort, make_response, g

from flask_restful import (Resource, Api, reqparse,
                               inputs, fields, marshal,
                               marshal_with, url_for)

from models import User


class Login(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    def post(self):
        """Post method for Login resource. Email and password are required"""
        self.reqparse.add_argument("email", required=True, help="Email required")
        self.reqparse.add_argument("password", required=True, help="Password required")

        args = self.reqparse.parse_args()
        try:
            user = User.get_user(args["email"])
        except ValueError:
            return make_response(jsonify({"message": "Invalid email or password"}), 400)
        else:
            if user.verify_password(args["password"]):
                return make_response(jsonify({
                    "message": "Login successful!",
                    "token": user.generate_auth_token().decode('ascii')
                }), 200)
            else:
                return make_response(jsonify({"message": "Invalid email or password"}), 400)

user_api = Blueprint('resources.users', __name__)
api = Api(user_api)
api.add_resource(
    Login,
    '/login',
    endpoint="home_login"
)
