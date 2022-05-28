from app.config.types import store_type

from .adapter import DataBaseAdapter
from .redis import RedisAdapter
from .sql import SQLAlchemyAdapter


def get_store() -> DataBaseAdapter:

    match store_type:
        case 'redis':
            return RedisAdapter()
        case 'sql':
            return SQLAlchemyAdapter()
        case _:
            print(f'Unknown {store_type} use "redis" or "sql')
            exit()
