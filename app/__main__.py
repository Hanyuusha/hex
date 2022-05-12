import argparse
import asyncio
from argparse import RawTextHelpFormatter

from app.bus.bus import MessageBus
from app.bus.messages import GetUserMessage
from app.store.redis import RedisAdapter
from app.store.sql import SQLAlchemyAdapter


def get_store(store):
    match store:
        case 'sql':
            return SQLAlchemyAdapter()
        case 'redis':
            return RedisAdapter()
        case _:
            print('you mast define "--store" option "sql" or "redis"')
            exit()


async def print_cli(bus, uid):
    result = await bus.handle(GetUserMessage(id=uid))
    print(f'\n{result.to_json()}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HEX', formatter_class=RawTextHelpFormatter)
    parser.add_argument('--uid', help='uid for cli mode')
    parser.add_argument('--store', help='datastore sql or redis')
    args = parser.parse_args()

    bus = MessageBus(get_store(args.store))
    asyncio.run(print_cli(bus, args.uid))
