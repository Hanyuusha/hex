from app.api.flask.api import api
from app.bus.bus import IMessageBus, MessageBus
from app.store import get_store
from asgiref.wsgi import WsgiToAsgi
from flask import Flask


def create_app(bus: IMessageBus):
    app = Flask(__name__)
    app.bus = bus
    app.register_blueprint(api, url_prefix='/api/v1')
    return app


def create_asgi_app():
    return WsgiToAsgi(
        create_app(
            MessageBus(
                get_store()
            )
        )
    )
