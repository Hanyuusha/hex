#!/bin/sh
alembic upgrade head
hypercorn "app.api.factory:app()" -b 0.0.0.0:5000