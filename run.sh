#!/bin/sh
alembic upgrade head
hypercorn "app.api.flask.factory:create_asgi_app()" -b 0.0.0.0:5000