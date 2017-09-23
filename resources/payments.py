
from flask import Blueprint, make_response, jsonify
from flask_restful import (Resource, Api, reqparse,
                               inputs, fields, marshal,
                               marshal_with, url_for)

import stripe

import config

stripe.api_key = config.SSK


class Donation(Resource):
    """end point to accept donations"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'token',
            required=True,
            location='json'
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            location='json'
        )
        self.reqparse.add_argument(
            'amount',
            required=True,
            type=inputs.positive,
            location='json'
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        token = args['token']
        email = args['email']
        amount = args['amount']
        if amount < 50:
            return make_response(jsonify({"Amount must be at least 50 cents"}), 400)
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                source=token,
                receipt_email=email,
                description="Donation to krsna.us"
            )
        except stripe.InvalidRequestError as e:
            return make_response(jsonify({"Invalid charge"}), 400)
        return make_response(jsonify({"message": "success"}), 200)

donate_api = Blueprint('resources.payments', __name__)
api = Api(donate_api)
api.add_resource(
    Donation,
    '/donation',
    endpoint='donation'
)
