import argparse
import asyncio
import os
from argparse import RawTextHelpFormatter

from app.bus import MessageBus
from app.domain import get_domain_app
from app.messages import GetUserMessage

from .app import run_app


async def print_cli(message_bus, uid):
    result = await message_bus.handle(GetUserMessage(id=uid))
    print(f'\n{result.to_json()}')


def run_cli(store_type, uid):
    os.environ['STORE_TYPE'] = store_type
    bus = MessageBus(get_domain_app())
    asyncio.run(print_cli(bus, uid))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HEX', formatter_class=RawTextHelpFormatter)
    parser.add_argument('type', help='run type')
    parser.add_argument('--uid', help='uid for cli mode')
    parser.add_argument('--store', help='datastore sql or redis')
    args = parser.parse_args()

    match args.type:
        case 'cli':
            run_cli(args.store, args.uid)
        case 'web':
            run_app()
