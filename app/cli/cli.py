'''
    Изначально не самая умная затея юзать интерактивный шелл в асинхронном приложении.
    EventLoop будет виснуть на вводе пользователя и приложение встанет.
    С другой стороны -
        интерактивный шелл запущен в отдельном процессе от всего остального, поэтому у него свой EventLoop.
    Пользователь с ним работает монопольно, поэтому помешать ему или он кому-то просто не могут.
    В любом случае шелл добавлен только для демонстрации.
'''
import functools
import uuid
from enum import Enum
from typing import Callable

import cli_ui

from app.bus import IMessageBus
from app.messages import (
    CreateUserMessage, DeleteUserMessage, GetUserMessage, UpdateUserMessage,
    ValidateException,
)


class Command(Enum):
    ADD = 'ADD'
    SHOW = 'SHOW'
    DELETE = 'DELETE'
    EXIT = 'EXIT'
    UPDATE = 'UPDATE'


class ExceptionHandler:

    errors: tuple = ()
    retries: int = 0

    def __init__(self, errors: tuple, retries: int):
        self.errors = errors
        self.retries = retries + 1

    def __call__(self, fn: Callable) -> Callable:
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            for i in range(1, self.retries):
                try:
                    await fn(*args, **kwargs)
                except self.errors as e:
                    if i == self.retries:
                        raise e
                    cli_ui.warning(e)
        return wrapper


class Cli:

    COMMANDS = [
        Command.ADD.name,
        Command.SHOW.name,
        Command.DELETE.name,
        Command.EXIT.name,
        Command.UPDATE.name,
    ]

    bus: IMessageBus = None

    def __init__(self, bus: IMessageBus):
        self.bus = bus

    async def ask_user(self):
        command = cli_ui.ask_choice('Enter command:', choices=self.COMMANDS)
        await self.match_command(Command(command))

    async def match_command(self, command: Command):
        match command:
            case Command.ADD:
                await self.add_user()
            case Command.SHOW:
                await self.show_user()
            case Command.DELETE:
                await self.delete_user()
            case Command.UPDATE:
                await self.update_user()

    @ExceptionHandler((ValidateException, ValueError), 3)
    async def add_user(self):
        first_name = cli_ui.ask_string('Enter first name:', 'Zero')
        second_name = cli_ui.ask_string('Enter second name:', 'Two')

        result = await self.bus.handle(
            CreateUserMessage(
                first_name=first_name,
                second_name=second_name,
            )
        )

        cli_ui.info(f'Created user: {result}')
        await self.ask_user()

    @ExceptionHandler((ValidateException, ValueError), 3)
    async def show_user(self):
        uid = uuid.UUID(cli_ui.ask_string('Enter User ID to show:'))
        result = await self.bus.handle(
            GetUserMessage(
                id=uid
            )
        )

        cli_ui.info(f'User: {result}')
        await self.ask_user()

    @ExceptionHandler((ValidateException, ValueError), 3)
    async def delete_user(self):
        uid = uuid.UUID(cli_ui.ask_string('Enter User ID to delete:'))
        result = await self.bus.handle(
            DeleteUserMessage(
                id=uid
            )
        )

        cli_ui.info(f'User: {result}')
        await self.ask_user()

    @ExceptionHandler((ValidateException, ValueError), 3)
    async def update_user(self):
        uid = uuid.UUID(cli_ui.ask_string('Enter User ID:'))
        first_name = cli_ui.ask_string('Enter new first name:')
        second_name = cli_ui.ask_string('Enter new second name:')

        await self.bus.handle(
            UpdateUserMessage(
                first_name=first_name,
                second_name=second_name,
                id=uid,
            )
        )

        cli_ui.info('User updated')
        await self.ask_user()
