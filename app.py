
from flask import Flask

import os
import config
import models
from resources.bhagavatpatrika import bp_api
from resources.books import book_api

app = Flask(__name__)
app.register_blueprint(bp_api, url_prefix='/api/v1')
app.register_blueprint(book_api, url_prefix='/api/v1')
app.secret_key = config.SECRET_KEY

if __name__ == '__main__':
    app.run(debug=True)
