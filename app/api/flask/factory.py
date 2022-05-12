from flask import Flask

from app.api.flask.api import api
from app.bus.bus import IMessageBus


def create_app(bus: IMessageBus):
    app = Flask(__name__)
    app.bus = bus
    app.register_blueprint(api, url_prefix='/api/v1')

    return app
