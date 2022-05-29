from app.config.types import StoreType, store_type

from .adapter import DataBaseAdapter
from .redis import RedisAdapter
from .sql import SQLAlchemyAdapter


def get_store() -> DataBaseAdapter:

    match store_type:
        case StoreType.REDIS:
            return RedisAdapter()
        case StoreType.SQL:
            return SQLAlchemyAdapter()
        case _:
            print(f'Unknown STORE_TYPE {store_type} use "redis" or "sql"')
            exit()
