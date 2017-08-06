
from flask import jsonify, Blueprint, abort, make_response, g

from flask_restful import (Resource, Api, reqparse,
                               inputs, fields, marshal,
                               marshal_with, url_for)
from oauth2client import client, crypt
from models import User
from config import CLIENT_ID


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


class GoogleLogin(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id_token', required=True, help="Token required", location="json")
        super().__init__()

    def post(self):
        """Post method for GoogleLogin resource"""
        args = self.reqparse.parse_args()
        token = args['id_token']
        print("token")
        print(token)
        try:
            idinfo = client.verify_id_token(token, CLIENT_ID)

            # Or, if multiple clients access the backend server:
            # idinfo = client.verify_id_token(token, None)
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #    raise crypt.AppIdentityError("Unrecognized client.")

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")

                # If auth request is from a G Suite domain:
                # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
                #    raise crypt.AppIdentityError("Wrong hosted domain.")
        except crypt.AppIdentityError:
            # Invalid token
            pass
        else:
            userid = idinfo['sub']
            user, created = User.get_or_create(user_id=userid, user_type='google')
            return make_response(jsonify({
                "message": "Login successful!",
                "token": user.generate_auth_token().decode('ascii')
            }), 200)


user_api = Blueprint('resources.users', __name__)
api = Api(user_api)
api.add_resource(
    Login,
    '/login',
    endpoint="home_login"
)
api.add_resource(
    GoogleLogin,
    '/login/google',
    endpoint='google_login'
)
