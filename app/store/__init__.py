import os

from .adapter import DataBaseAdapter
from .redis import RedisAdapter
from .sql import SQLAlchemyAdapter


def get_store() -> DataBaseAdapter:
    store = os.getenv('STORE_TYPE', 'redis')
    match store:
        case 'redis':
            return RedisAdapter()
        case 'sql':
            return SQLAlchemyAdapter()
        case _:
            print(f'Unknown {store} use "redis" or "sql')
            exit()
