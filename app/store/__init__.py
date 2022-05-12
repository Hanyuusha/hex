import os

from .redis import RedisAdapter
from .sql import SQLAlchemyAdapter


def get_store():
    store = os.getenv('STORE_MODE', 'redis')
    match store:
        case 'redis':
            return RedisAdapter()
        case 'sql':
            return SQLAlchemyAdapter()
        case _:
            print(f'Unknown {store} use "redis" or "sql')
            exit()
