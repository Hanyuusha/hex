import os

from app.api.fast.api import app as fast_api
from app.api.flask.api import asgi_app as flask_api


def app():
    api_type = os.getenv('API_TYPE', 'fast')
    match api_type:
        case 'flask':
            return flask_api
        case 'fast':
            return fast_api
