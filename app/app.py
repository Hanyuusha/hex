import asyncio
import os
import socket
import time
from pathlib import Path

from alembic import command
from alembic.config import Config as AlembicConfig
from hypercorn.asyncio import serve
from hypercorn.config import Config as HypercornConfig

from app.api import fast_api, flask_api
from app.config.app import BIND_ADDRESS, BIND_PORT
from app.config.store import DB_HOST, DB_PORT, get_sync_db_url
from app.config.types import api_type


def run_migrations() -> None:
    path = Path(os.path.realpath(__file__))
    migrations_path = os.path.join(path.parent.parent, 'migrations')
    ini_path = os.path.join(path.parent.parent, 'alembic.ini')

    alembic_cfg = AlembicConfig(ini_path)
    alembic_cfg.set_main_option('script_location', migrations_path)
    alembic_cfg.set_main_option('sqlalchemy.url', get_sync_db_url())

    command.upgrade(alembic_cfg, 'head')


def get_app():
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
    config.bind = [f'{BIND_ADDRESS}:{BIND_PORT}']
    asyncio.run(serve(get_app(), config))


def run_app():
    wait_for_postgres()
    run_migrations()
    run_server()
