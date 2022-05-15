import argparse
import asyncio
import os
from argparse import RawTextHelpFormatter

from app.bus import GetUserMessage, MessageBus
from app.domain import get_domain_app


async def print_cli(message_bus, uid):
    result = await message_bus.handle(GetUserMessage(id=uid))
    print(f'\n{result.to_json()}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HEX', formatter_class=RawTextHelpFormatter)
    parser.add_argument('--uid', help='uid for cli mode')
    parser.add_argument('--store', help='datastore sql or redis')
    args = parser.parse_args()

    os.environ['STORE_TYPE'] = args.store
    bus = MessageBus(get_domain_app())
    asyncio.run(print_cli(bus, args.uid))
