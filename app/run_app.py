import asyncio
import os
import socket
import time
from pathlib import Path

from alembic import command
from alembic.config import Config as AlembicConfig
from hypercorn.asyncio import serve
from hypercorn.config import Config as HypercornConfig

from app.api.fast.api import app as fast_api
from app.api.flask.api import asgi_app as flask_api

from .config import DB_HOST, DB_PORT, get_sync_db_url


def run_migrations() -> None:
    path = Path(os.path.realpath(__file__))
    migrations_path = os.path.join(path.parent.parent, 'migrations')
    ini_path = os.path.join(path.parent.parent, 'alembic.ini')

    alembic_cfg = AlembicConfig(ini_path)
    alembic_cfg.set_main_option('script_location', migrations_path)
    alembic_cfg.set_main_option('sqlalchemy.url', get_sync_db_url())

    command.upgrade(alembic_cfg, 'head')


def get_app():
    api_type = os.getenv('API_TYPE', 'fast')
    match api_type:
        case 'flask':
            return flask_api
        case 'fast':
            return fast_api


def wait_for_postgres():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((DB_PORT, DB_HOST))
            s.close()
            break
        except socket.error:
            print('Wait postgres...')
            time.sleep(0.5)


def run_server():
    config = HypercornConfig()
    bind_address = os.getenv('BIND_ADDRESS', 'localhost')
    bind_port = os.getenv('BIND_PORT', '5000')
    config.bind = [f'{bind_address}:{bind_port}']
    asyncio.run(serve(get_app(), config))


def run_app():
    wait_for_postgres()
    run_migrations()
    run_server()
