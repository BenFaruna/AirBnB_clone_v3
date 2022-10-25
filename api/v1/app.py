#!/usr/bin/python3
"""api routing for various route"""
import os

from flask import Flask, jsonify, make_response

from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(dbsession):
    """close up storage system"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """returns a json response if path is not valid"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True, debug=True)
