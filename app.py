
from flask import Flask, current_app, abort
from flask_cors import CORS

import os
import config
import models
from resources.bhagavatpatrika import bp_api
from resources.books import book_api
from resources.harikatha import hk_api
from resources.hmagazine import hmag_api
from resources.hmonthly import hmonthly_api
from resources.lectures import lectures_api
from resources.movies import movie_api
from resources.songs import song_api
from resources.all_results import all_api

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(bp_api, url_prefix='/api/v1')
app.register_blueprint(book_api, url_prefix='/api/v1')
app.register_blueprint(hk_api, url_prefix='/api/v1')
app.register_blueprint(hmag_api, url_prefix='/api/v1')
app.register_blueprint(hmonthly_api, url_prefix='/api/v1')
app.register_blueprint(lectures_api, url_prefix='/api/v1')
app.register_blueprint(movie_api, url_prefix='/api/v1')
app.register_blueprint(song_api, url_prefix='/api/v1')
app.register_blueprint(all_api, url_prefix='/api/v1')
app.secret_key = config.SECRET_KEY

@app.errorhandler(404)
def page_not_found(e):
    return current_app.send_static_file('index.html')

@app.route('/')
@app.route('/<resource>')
def hello_world(resource=None):
    if os.path.isfile('static/{}'.format(resource)):
        return current_app.send_static_file('{}'.format(resource))
    return current_app.send_static_file('index.html')

if __name__ == '__main__':
    app.run()
