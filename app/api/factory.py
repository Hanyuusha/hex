import os

from app.api.fast.api import app as fast_api
from app.api.flask.api import api
from app.bus import IMessageBus, get_message_bus
from asgiref.wsgi import WsgiToAsgi
from flask import Flask


def create_flask_app(bus: IMessageBus):
    app = Flask(__name__)
    app.bus = bus
    app.register_blueprint(api, url_prefix='/api/v1')
    return app


def create_asgi_flask_app():
    return WsgiToAsgi(create_flask_app(get_message_bus()))


def app():
    match os.getenv('API_TYPE', 'fast'):
        case 'flask':
            return create_asgi_flask_app()
        case 'fast':
            return fast_api
